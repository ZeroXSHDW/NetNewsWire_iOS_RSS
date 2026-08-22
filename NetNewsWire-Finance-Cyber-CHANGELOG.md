# NetNewsWire Finance + Cyber Changelog

Checked: 22 August 2026 (Europe/Dublin)

## Latest expansion — Federal Register sanctions, financial-crime and banking notices

- Added notification-off, Master-only **Federal Register — OFAC Sanctions Notices** from the official [OFAC press-release page](https://ofac.treasury.gov/press-releases) and filtered [Federal Register OFAC RSS feed](https://www.federalregister.gov/api/v1/documents.rss?conditions%5Bagency_ids%5D%5B%5D=203&order=newest). It restores a durable sanctions-notice lane after [OFAC retired its RSS service](https://ofac.treasury.gov/recent-actions/20241122); the structured repeated title is documented with the manifest’s `structured-alert` policy.
- Added notification-off, Master-only **Federal Register — FinCEN AML & Financial-Crime Notices** from the official [FinCEN newsroom](https://www.fincen.gov/news-room) and filtered [FinCEN RSS feed](https://www.federalregister.gov/api/v1/documents.rss?conditions%5Bagency_ids%5D%5B%5D=194&order=newest), plus **Federal Register — OCC Banking Rules & Notices** from the official [OCC Federal Register page](https://www.occ.treas.gov/topics/laws-and-regulations/federal-register/index-federal-register.html) and filtered [OCC RSS feed](https://www.federalregister.gov/api/v1/documents.rss?conditions%5Bagency_ids%5D%5B%5D=80&order=newest). These add first-party AML, financial-crime, banking-rule and supervisory notices distinct from the existing OCC and Treasury streams.
- Three repeated validator-compatible probes were byte-identical with complete HTTPS item links: OFAC **9,708 bytes / 8 records / 3 unique structured titles through 14 August 2026**, FinCEN **6,867 bytes / 4 unique records through 14 August**, and OCC **9,257 bytes / 5 unique records through 13 August**. Exact title/link screening found zero active-bundle overlap for all three. All remain quiet Master-only inputs, so Air/Lite stay at **125 / 118** feeds with no added phone payload or interrupting notifications.
- The official [ASD ACSC RSS directory](https://www.cyber.gov.au/about-us/about-asdacsc/who-we-are/ACSC-social-media-community) was rechecked: its five advertised RSS routes returned HTTP 000 with zero bytes under repeated anonymous HTTPS probes, so they remain deferred pending reproducible transport.

## Latest expansion — Canadian Cyber Centre and Japanese securities-surveillance RSS

- Added notification-off, Master-only **Canadian Centre for Cyber Security — Alerts & Advisories** from the official [Cyber Centre RSS subscription page](https://www.cyber.gc.ca/en/contact-cyber-centre) and direct [alerts feed](https://www.cyber.gc.ca/api/cccs/rss/v1/get?feed=alerts_advisories&lang=en), plus **Canadian Centre for Cyber Security — Guidance, News & Events** from the official [news and events page](https://www.cyber.gc.ca/en/news-events) and direct [guidance/news feed](https://www.cyber.gc.ca/api/cccs/rss/v1/get?feed=news_events_guidance&lang=en). The alerts stream returned three byte-identical **131,383-byte** probes with **50 unique dated records through 21 August 2026** and zero active-bundle overlap; the guidance stream returned three byte-identical **1,954,234-byte** probes with **50 unique dated records through 12 August 2026**, 48 new records and two expected CSE cross-posts.
- Added notification-off, Master-only **Japan Securities and Exchange Surveillance Commission — Press Releases** from the official [English RSS page](https://www.fsa.go.jp/sesc/english/rss.html) and direct [Press Releases feed](https://www.fsa.go.jp/sescEnNewsList_rss2.xml). Three byte-identical **1,064-byte** probes returned two unique dated records through 26 June 2026, complete HTTPS links and zero active-bundle or Japan FSA overlap. The weaker SESC “Others” feed was not added.
- The deterministic bundle is now **536 Master / 125 Air / 118 Lite**, with **428 Finance / 108 Cyber Security** in Master. The current live Master audit accepts **535/536**; the final body/wire totals are recorded once the live rerun completes. The only expected hard failure is the retained CEPR malformed HTTP 200 body. Air remains **125/125** at **4,177,925 / 2,000,128** body/wire bytes with **16,379 bytes** of headroom; Lite remains **118/118** at **4,087,538 / 1,976,506** with **106,766 bytes**. Both phone audits have zero failures, noisy feeds, regression warnings and device-budget failures.
- The prior **South African Reserve Bank — News and Publications** endpoint now returns an HTML “Page not found” response from the official RSS URL, while the current **CIS — Cybersecurity Blog** endpoint returns a 238-byte HTML “Object moved” shell. Both were removed from the active manifest and remain documented recheck targets; the valid CIS MS-ISAC Advisories feed remains active.

## Latest expansion — National Crime Agency direct RSS

- Added notification-off, Master-only **National Crime Agency — Direct News** from the official [NCA news page](https://www.nationalcrimeagency.gov.uk/news/all-news) and direct [NCA RSS feed](https://www.nationalcrimeagency.gov.uk/news?format=feed&type=rss). It adds first-party operational coverage of serious and organised crime, cybercrime, drug trafficking, fraud, people-smuggling, illicit finance and international law-enforcement activity alongside the existing GOV.UK NCA stream.
- Three repeated validator-compatible HTTP 200 `application/rss+xml` probes returned **17,862-byte** responses with the same **20 dated, unique records through 19 August 2026**, complete HTTPS links and no internal noise. Only the channel `lastBuildDate` advanced by one second between probes; item titles, dates and links were identical. Exact title/link and conservative-fuzzy screening found zero overlap with the existing GOV.UK NCA feed or cached Master corpus.
- The deterministic bundle is now **532 Master / 125 Air / 118 Lite**, with **425 Finance / 107 Cyber Security** in Master. Master accepts **531/532** at **55,088,763 body bytes / 29,859,353 wire bytes**; the only hard failure remains the retained CEPR malformed HTTP 200 body. The two non-critical warnings are the dynamic Athens redirect and a Banco de la República publisher-title change. Air passes **125/125** at **4,177,871 / 1,960,133** body/wire bytes with **16,433 bytes** of headroom; Lite passes **118/118** at **4,087,538 / 1,936,370** with **106,766 bytes**. Both phone audits have zero failures, noisy feeds, critical regressions or regression warnings.

## Latest expansion — EUSPA Press Releases RSS

- Added notification-off, Master-only **EU Agency for the Space Programme — Press Releases** from the official [press releases page](https://www.euspa.europa.eu/pressroom/press-releases) and direct [press releases RSS feed](https://www.euspa.europa.eu/pressroom/press-releases/rss.xml). It adds first-party space-market, secure-connectivity, Galileo/Copernicus and strategic-space-security context alongside the existing EUSPA News stream.
- Three repeated validator-compatible HTTP 200 `application/rss+xml` probes were byte-identical at **43,387 bytes**, with **10 dated records through 26 May 2026**, complete HTTPS item links and zero exact title, link or conservative-fuzzy overlap with the cached Master corpus or existing EUSPA News feed.
- The deterministic bundle is now **531 Master / 125 Air / 118 Lite**, with **424 Finance / 107 Cyber Security** in Master. Master accepts **530/531** at **55,070,409 body bytes / 29,841,931 wire bytes**; the only hard failure remains the retained CEPR malformed HTTP 200 body. The three non-critical warnings are the dynamic Athens redirect, the EEA Maps and Charts item-link transport regression and the expected feed-added notice for EUSPA Press Releases. Air passes **125/125** at **4,177,871 / 1,959,968** body/wire bytes with **16,433 bytes** of headroom; Lite passes **118/118** at **4,088,492 / 1,936,655** with **105,812 bytes**. Both phone audits have zero failures, noisy feeds, critical regressions or regression warnings.

## Latest expansion — FRA Publications and eu-LISA RSS

- Added notification-off, Master-only **European Union Agency for Fundamental Rights — Publications** from the official [FRA RSS directory](https://fra.europa.eu/en/content/rss) and direct [publications RSS feed](https://fra.europa.eu/en/publications-and-resources/publications.rss.xml), plus **eu-LISA — News and Updates** from the official [updates page](https://www.eulisa.europa.eu/news-and-events?tp=77) and [updates RSS feed](https://www.eulisa.europa.eu/news-and-events.rss), and **eu-LISA — Publications** from the official [publications page](https://www.eulisa.europa.eu/our-publications) and [publications RSS feed](https://www.eulisa.europa.eu/our-publications.rss). These add fundamental-rights, privacy, AI, migration, rule-of-law, EU large-scale IT-system and digital-resilience signal without adding phone notifications or payload.
- Three repeated validator-compatible probes were byte-identical for every endpoint: FRA Publications returned **10 dated records / 12,307 bytes through 18 August 2026**; eu-LISA Updates **20 / 18,234 bytes through 14 July 2026**; and eu-LISA Publications **20 / 16,554 bytes through 21 August 2026**. All item links were HTTPS. FRA Publications had zero exact title/link overlap with FRA News; the two eu-LISA windows had zero exact title/link overlap with each other.
- The deterministic bundle is now **530 Master / 125 Air / 118 Lite**, with **423 Finance / 107 Cyber Security** in Master. Master accepts **529/530** at **55,027,022 body bytes / 29,908,469 wire bytes**; the only hard failure remains the retained CEPR malformed HTTP 200 body. The four non-critical Master warnings are the dynamic Athens redirect and the three expected feed-added entries. Air passes **125/125** at **4,177,911 / 2,041,008** body/wire bytes with **16,393 bytes** of headroom; Lite passes **118/118** at **4,088,492 / 2,031,150** with **105,812 bytes**. Both phone audits have zero failures, noisy feeds, critical regressions or regression warnings.

## Latest expansion — ComReg and Houses of the Oireachtas RSS

- Added notification-off, Master-only **ComReg — News and Publications** from the official [ComReg site](https://www.comreg.ie/) and [RSS feed](https://www.comreg.ie/feed/), plus **Houses of the Oireachtas — Press Releases**, **Dáil Schedule**, **Seanad Schedule** and **Committee Schedule** from the official [press-centre page](https://www.oireachtas.ie/en/press-centre/press-releases/), [Dáil schedule](https://www.oireachtas.ie/en/dail-schedule/), [Seanad schedule](https://www.oireachtas.ie/en/seanad-schedule/) and [committee schedule](https://www.oireachtas.ie/en/committees/schedule/). These add Irish communications regulation, parliamentary policy, sitting dates and committee oversight timing without adding phone interruptions.
- Three repeated validator-compatible probes were stable for all five endpoints: ComReg **10 / 31,642 bytes through 20 August 2026**; Oireachtas Press Releases **30 / 31,713 through 21 August**; Dáil **18 / 8,760 through 27 August**; Seanad **18 / 7,972 through 27 August**; and Committee **21 / 9,878 through 2 September**. Titles, dates and HTTPS item links pass; schedule feeds use the documented `scheduled-calendar` policy, 180,000-minute future tolerance and 365-day stale review. Their shared current-date cluster is expected calendar payload, not a noisy-feed failure.
- The deterministic bundle is now **527 Master / 125 Air / 118 Lite**, with **422 Finance / 105 Cyber Security** in Master. Master accepts **526/527** at **54,947,986 body bytes / 29,740,550 wire bytes**; the only hard failure remains the retained CEPR malformed HTTP 200 body. Air passes **125/125** at **4,177,911 / 2,041,071** with **16,393 bytes** of body headroom; Lite passes **118/118** at **4,088,492 / 2,017,665** with **105,812 bytes**. Phone audits have zero failures, noisy feeds, critical regressions or regression warnings.

## Latest expansion — European Commission Representation in Ireland RSS

- Added notification-off, Master-only **European Commission Representation in Ireland — News** from the official [Representation news page](https://ireland.representation.ec.europa.eu/news-and-events/news_en) and direct [English RSS feed](https://ireland.representation.ec.europa.eu/node/2/rss_en). The stream adds Ireland-facing EU institutional, policy, public-affairs and Irish EU Presidency 2026 context distinct from the existing pan-European Commission topic feeds.
- Three repeated validator-compatible HTTP 200 `application/rss+xml` probes were byte-identical at **42,633 bytes**, with **30 dated items through 29 July 2026**, complete HTTPS item links and zero exact title/link or optimized conservative-fuzzy overlap against the cached corpus.
- The addition is quiet, Master-only input for the local Apple Intelligence collector. The deterministic bundle is now **522 Master / 125 Air / 118 Lite**, with **417 Finance / 105 Cyber Security** in Master. Fresh reports pass **125/125 Air** at **4,186,239 body bytes / 1,988,033 wire bytes** and **118/118 Lite** at **4,097,854 / 1,965,566**, leaving **8,065** and **96,450** bytes below the 4 MiB phone ceilings. Master accepts **521/522** at **54,868,705 / 29,714,193**; the only hard failure remains the retained CEPR malformed HTTP 200 body. There are zero noisy feeds and zero critical regressions; the three non-critical warnings are the dynamic Athens redirect, the EEA Maps and Charts item-link transport regression and the expected feed-added entry for this stream.

## Expansion — UK national-security and cyber-security taxonomy RSS

- Added four notification-off, Master-only Atom streams from the official [GOV.UK national-security news and communications](https://www.gov.uk/search/news-and-communications?parent=%2Fgovernment%2Fnational-security&topic=8a98b827-82ad-49b4-819e-82c208c551c4), [cyber-security news](https://www.gov.uk/search/news-and-communications?topic=67f50352-bc30-482f-a2d0-a05714e3cea8), [research and statistics](https://www.gov.uk/search/research-and-statistics?parent=%2Fgovernment%2Fcyber-security&topic=67f50352-bc30-482f-a2d0-a05714e3cea8) and [policy papers and consultations](https://www.gov.uk/search/policy-papers-and-consultations?topic=67f50352-bc30-482f-a2d0-a05714e3cea8) directories: [National Security News & Communications](https://www.gov.uk/search/news-and-communications.atom?topic%5B%5D=8a98b827-82ad-49b4-819e-82c208c551c4), [Cyber Security News & Communications](https://www.gov.uk/search/news-and-communications.atom?topic%5B%5D=67f50352-bc30-482f-a2d0-a05714e3cea8), [Cyber Security Research & Statistics](https://www.gov.uk/search/research-and-statistics.atom?content_store_document_type=all_research_and_statistics&topic%5B%5D=67f50352-bc30-482f-a2d0-a05714e3cea8) and [Cyber Security Policy Papers & Consultations](https://www.gov.uk/search/policy-papers-and-consultations.atom?topic%5B%5D=67f50352-bc30-482f-a2d0-a05714e3cea8).
- Three repeated validator-compatible probes for each endpoint were byte-identical, returned HTTP 200 with a parseable Atom root and exposed 20 unique dated items. The four bodies measured **12,355 bytes** (national security, latest **17 July 2026**), **13,388 bytes** (cyber news, latest **6 July 2026**), **11,497 bytes** (cyber research, latest **13 August 2026**) and **11,647 bytes** (cyber policy, latest **13 July 2026**). All item links were HTTPS and the feeds passed the repository’s structural, freshness and noise checks.
- National-security news and cyber news had zero exact or conservative-fuzzy overlap against the cached 517-feed corpus. Cyber research had only the expected DSIT cross-posts — one exact title and two exact links — while adding breach-survey, AI-security, quantum, cyber-economy and digital-identity research. Cyber policy had one expected Ofgem cross-post, **Energy sector cyber security strategy**, and no other overlap.
- The four feeds stay Master-only and notification-off: the deterministic bundle is now **521 Master / 125 Air / 118 Lite**, with **416 Finance / 105 Cyber Security** in Master. The current audits pass **125/125 Air** and **118/118 Lite** at **4,187,391 / 1,986,850** and **4,097,854 / 1,965,530** body/wire bytes; Master accepts **520/521** at **54,827,383 / 29,707,308**. The only hard failure is the retained CEPR malformed HTTP 200 body; there are zero noisy feeds and zero critical regressions. The six non-critical warnings are the dynamic Athens redirect, CERT Polska’s publisher-title drift and the four expected feed-added entries.

## Latest expansion — Council of the EU meeting-calendar RSS

- Added five official, notification-off Council meeting calendars from the [Council RSS directory](https://www.consilium.europa.eu/en/about-site/rss/): **Economic & Financial Affairs**, **Eurogroup**, **European Council**, **Justice & Home Affairs** and **Transport, Telecommunications & Energy**. Their direct RSS endpoints are the `meetings.ashx` category feeds documented by the directory.
- Three repeated validator-compatible HTTP 200 `text/xml` probes were byte-identical: **29,176 bytes** for Economic & Financial Affairs, **28,967** for Eurogroup, **19,201** for European Council, **24,782** for Justice & Home Affairs and **21,488** for Transport, Telecommunications & Energy. Each returned 50 scheduled records, all item links were HTTPS and exact title/link screening found zero overlap with the cached Master corpus.
- The manifest marks these event-driven calendars with the explicit `scheduled-calendar` noise policy and a scoped **180,000-minute** future-date tolerance because repeated meeting titles are schedule records, not editorial duplication. European Council — Meetings is included in both Air and Lite; the other four remain Master-only. The current deterministic bundle is **517 Master / 125 Air / 118 Lite**, with **415 Finance / 102 Cyber Security** in Master.
- The current live reports pass **125/125 Air** and **118/118 Lite** with zero noisy feeds and passing device budgets. Master accepts **515/517**, retaining the known CEPR malformed HTTP 200 response and current CERT Polska HTTP 502; the six non-critical warnings are the dynamic Athens redirect plus the five intentional feed-added calendar entries, with zero critical regressions. The full-body totals are **54,758,456 / 29,628,621 bytes** for Master, **4,187,344 / 2,001,206** for Air and **4,097,847 / 1,977,943** for Lite.

## Latest expansion — Canadian official RSS and CIS Blog route recovery

- Added five notification-off Canadian government streams from the official [Canada.ca RSS directory](https://www.canada.ca/en/news/subscribe-emails.html): **National Defence — News** (**84,606 bytes / 100 unique dated items through 21 August 2026**, Master-only), **Global Affairs Canada — News** (**42,914 / 50 through 21 August**, Air/Lite), **Communications Security Establishment — News** (**31,172 / 37 through 29 June**, Air/Lite), **Defence Investment Agency — News** (**21,713 / 22 through 4 August**, Air/Lite) and **Canadian Security Intelligence Service — News** (**11,891 / 14 through 3 June**, Air/Lite). The Global Affairs stream is also listed by the official [Global Affairs Canada RSS directory](https://international.canada.ca/en/global-affairs/news/rss).
- Three repeated validator-compatible HTTP 200 probes for each endpoint were byte-identical, with complete HTTPS item links. Exact title/link screening against the cached 505-feed Master corpus found zero overlap for National Defence, CSE, Defence Investment Agency and CSIS; Global Affairs had one expected cross-government duplicate with the retained UK FCDO stream and no additional conservative-fuzzy overlap. The four compact streams fit both phone profiles as quiet Apple Intelligence inputs; the larger National Defence stream remains Master-only.
- Rechecked the official [CIS RSS Syndication page](https://www.cisecurity.org/rss-syndication) after the old [MS-ISAC Threat Level feed](https://www.cisecurity.org/feed/alert) began returning an HTML “Object moved” shell. The separately documented [CIS Blog feed](https://www.cisecurity.org/feed/blog) passed three repeated stable HTTP 200 `text/xml` probes at **23,821 bytes / 50 unique dated items through 19 August 2026**, with complete HTTPS links and zero exact or conservative-fuzzy overlap against the cached 512-feed corpus. It is added as notification-off, Master-only **CIS — Cybersecurity Blog**; the non-RSS text status endpoint was deliberately not substituted.
- The deterministic bundle is now **512 Master / 124 Air / 117 Lite**, with **411 Finance / 101 Cyber Security** in Master. The old **CIS — MS-ISAC Threat Level** entry was removed from the active profiles after its endpoint began returning an HTML “Object moved” shell rather than RSS/XML; valid **CIS — MS-ISAC Advisories** remains in Air and Lite, while **CIS — Cybersecurity Blog** is Master-only. The final clean-cache phone reports accept **124/124 Air** and **117/117 Lite**; Master accepts **510/512**. Master measures **54,634,696 body bytes / 29,597,091 wire bytes** with no unresolved critical regression; the remaining hard failures are the retained CEPR malformed HTTP 200 body and current CERT Polska HTTP 502, plus the dynamic Athens redirect warning. Air measures **4,168,183 / 1,983,756 bytes**, leaving **26,121 bytes**; Lite measures **4,078,686 / 1,960,969 bytes**, leaving **115,618 bytes**. Both device-budget checks pass, and all five Canadian additions pass.

## Latest expansion — U.S. Department of Energy and NIST critical-technology RSS

- Added notification-off, Master-only **U.S. Department of Energy — Energy News** from the official [Energy News listing](https://www.energy.gov/listings/energy-news) and direct [DOE RSS endpoint](https://www.energy.gov/rss/energygov/2193718). Three repeated validator-compatible HTTP 200 `application/rss+xml` probes were byte-identical at **7,486 bytes**, with **10 unique dated items through 20 August 2026**, complete HTTPS item links and zero exact or conservative-fuzzy overlap against the cached 505-feed Master corpus.
- Added notification-off, Master-only **NIST — General News & Critical Technology** from the official [NIST RSS directory](https://www.nist.gov/coo/nist-rss-feeds) and direct [NIST News RSS endpoint](https://www.nist.gov/news-events/news/rss.xml). Three repeated probes were byte-identical at **23,987 bytes**, with **40 unique dated items through 13 August 2026**, complete HTTPS item links and zero exact or conservative-fuzzy overlap against the cached 505-feed Master corpus, including the retained NIST Cybersecurity Insights stream.
- The two additions widen the local Apple Intelligence research pool with energy-security, critical-minerals, grid, nuclear, standards, AI and quantum context without consuming phone payload or notification budget. The deterministic bundle is now **507 Master / 121 Air / 114 Lite**, with **407 Finance / 100 Cyber Security** in Master. The fresh live reports accept **506/507 Master**, **121/121 Air** and **114/114 Lite**. Master measures **54,438,971 body bytes / 29,611,059 wire bytes** and retains only the known CEPR malformed HTTP 200 body; its three non-critical warnings are the dynamic Euronext Athens redirect target and the two expected feed-added notices. Air measures **4,062,348 / 1,992,853 bytes** with **131,956 bytes** of headroom; Lite measures **3,972,851 / 1,996,668 bytes** with **221,453 bytes** of headroom. Both phone profiles pass with zero feed failures, regression warnings and critical regressions.

## Latest expansion — Atlantic Council, FDD and Lawfare Cybersecurity & Tech RSS

- Added notification-off, Master-only **Atlantic Council — Global Security & Geopolitics** from the official [Atlantic Council site](https://www.atlanticcouncil.org/) and direct [RSS feed](https://www.atlanticcouncil.org/feed/); **FDD — National Security & Foreign Policy Analysis** from [FDD](https://www.fdd.org/), its [About FDD page](https://www.fdd.org/about-fdd/) and direct [RSS feed](https://www.fdd.org/feed/); and **Lawfare — Cybersecurity & Tech** from the official [Lawfare subscription directory](https://www.lawfaremedia.org/subscribe) and direct [focused RSS feed](https://www.lawfaremedia.org/feeds/cybersecurity-tech).
- Three repeated validator-compatible HTTP 200 probes were byte-identical: **175,367 bytes / 100 dated items** for Atlantic Council through 21 August 2026, **187,994 bytes / 50 dated items** for FDD through 21 August 2026, and **20,346 bytes / one dated item** for Lawfare through 21 August 2026. All item titles, dates and HTTPS links passed the structural and freshness gates; exact and conservative-fuzzy screening found zero overlap with the cached Master corpus. The broader Lawfare feed was not added because it repeated the focused cyber-policy story.
- The three feeds remain Master-only, notification-off specialist research inputs; Air and Lite stay unchanged at **121** and **114** feeds. The final clean-cache live Master report accepts **504/505** feeds and measures **54,407,497 body bytes / 29,512,840 wire bytes**. The only hard failure is the retained CEPR malformed HTTP 200 body; the report has four non-critical warnings and zero critical regressions. Fresh phone audits pass **121/121 Air** at **4,062,348 / 1,992,990 bytes** with **131,956 bytes** of headroom and **114/114 Lite** at **3,972,851 / 1,969,674 bytes** with **221,453 bytes** of headroom.

## Latest expansion — strategic-security, OSINT and organized-crime RSS

- Added notification-off, Master-only **ECFR — European Foreign & Security Policy** from the official [ECFR RSS subscription page](https://ecfr.eu/feeds/) and direct [all-content RSS feed](https://ecfr.eu/feed/); **Bellingcat — Open-Source Investigations** from the publisher’s [official homepage](https://www.bellingcat.com/) and direct [RSS feed](https://www.bellingcat.com/feed/); **Global Initiative — Organized Crime & Illicit Economies** from its [official newsroom](https://globalinitiative.net/about-us/newsroom/) and direct [RSS feed](https://globalinitiative.net/feed/); and **Jamestown — Eurasia & Terrorism Analysis** from the publisher’s [official site](https://jamestown.org/) and direct [RSS feed](https://jamestown.org/feed/).
- Three repeated validator-compatible HTTP 200 probes were byte-identical for every addition: **474,734 bytes** for ECFR (25 dated items through 21 August), **416,704 bytes** for Bellingcat (10 through 20 August), **15,626 bytes** for Global Initiative (12 through 21 August) and **251,605 bytes** for Jamestown (10 through 20 August). Every item had a unique title, parseable date and complete HTTPS link; all four feeds passed the repository noise and freshness gates.
- Exact title/link screening against the cached 498-feed Master corpus found zero overlap for all four candidates, and optimized conservative-fuzzy screening found no overlap. The additions extend the specialist layer with pan-European foreign/security policy, OSINT investigations, organized-crime and illicit-economy analysis, and Eurasia/terrorism intelligence distinct from RUSI, SIPRI, Chatham House and EUISS. ECFR and Bellingcat are payload-review sources; all four remain Master-only and notification-off.
- The deterministic bundle is now **502 Master / 121 Air / 114 Lite**, with **406 Finance / 96 Cyber Security** in Master. The clean-cache live Master report accepts **501/502** feeds, measures **54,038,330 body bytes / 29,374,497 wire bytes**, and retains only the known CEPR malformed HTTP 200 body as a hard failure. It reports zero critical regressions and six non-critical warnings: the four expected feed-added entries, the dynamic Euronext Athens redirect target and a Nasdaq Trade Halts item-count change. Fresh phone audits pass **121/121 Air** at **4,037,735 / 1,991,942 bytes** with **156,569 bytes** of headroom and **114/114 Lite** at **3,948,198 / 1,968,234 bytes** with **246,106 bytes** of headroom; each carries only the expected Nasdaq Trade Halts item-count warning.

## Latest expansion — EUISS strategic-security RSS

- Added notification-off, Master-only **EUISS — News & Publications** from the official [European Union Institute for Security Studies](https://www.iss.europa.eu/) and its direct [RSS endpoint](https://www.iss.europa.eu/rss.xml). Three repeated validator-compatible HTTP 200 `application/rss+xml` probes were byte-identical at **45,551 bytes** and returned 10 dated, unique items through 14 August 2026 with complete HTTPS item links.
- Exact title/link screening and optimized conservative-fuzzy screening found zero overlap with the cached Master corpus. The stream adds first-party EU strategic-security, defence, geopolitical, digital-autonomy, Ukraine, China, enlargement and critical-raw-materials analysis; the larger 45.6 KB response remains Master-only so the current phone profiles do not lose existing coverage or exceed their refresh budgets.
- The deterministic bundle is now **498 Master / 121 Air / 114 Lite**, with **406 Finance / 92 Cyber Security** in Master. The clean-cache live Master report accepts **497/498** feeds, measures **52,987,337 body bytes / 29,011,702 wire bytes**, records only the known CEPR malformed HTTP 200 response as a hard failure, and has zero critical regressions. The phone counts and payload measurements remain unchanged: Air **121/121** at **4,156,139 / 2,002,776** bytes with **38,165 bytes** of headroom; Lite **114/114** at **4,066,960 / 1,980,312** bytes with **127,344 bytes** of headroom.

## Latest expansion — CIS MS-ISAC RSS

- Added notification-off **CIS — MS-ISAC Threat Level** and **CIS — MS-ISAC Advisories** from the official [CIS RSS Syndication page](https://www.cisecurity.org/rss-syndication), using the direct [Threat Level feed](https://www.cisecurity.org/feed/alert) and [Advisories feed](https://www.cisecurity.org/feed/advisories). Three repeated validator-compatible HTTP 200 `text/xml` probes were byte-identical for each stream: **1,895 bytes** with one dated linked status item through 13 July 2026, and **65,497 bytes** with 50 dated items through 19 August 2026 (32 unique titles, 50 unique links, no missing links).
- Exact title/link screening and conservative-fuzzy screening found zero overlap with the cached Master corpus. The Threat Level stream adds compact event-driven MS-ISAC status context; Advisories adds vulnerability and patch guidance. Both are included in Air and Lite, stay below the phone payload ceiling and remain notification-off for Apple Intelligence digest review.
- The deterministic bundle is now **497 Master / 121 Air / 114 Lite**, with **406 Finance / 91 Cyber Security** in Master. Current live reports accept **496/497 Master**, **121/121 Air** and **114/114 Lite**. Master measures **52,955,682 body bytes / 29,051,163 wire bytes** and retains only the known CEPR malformed HTTP 200 response; the sole regression watch is the non-critical Euronext Athens redirect target. Air measures **4,156,139 / 2,002,776**, leaving **38,165 bytes**; Lite measures **4,066,960 / 1,980,312**, leaving **127,344 bytes** below the 4 MiB ceiling. Both phone profiles pass their device budgets with no failed feeds or critical regressions.
- **CIS — Cybersecurity Blog** was screened but not retained: a neutral probe returned XML, while the validator-compatible HTTP 200 response returned an HTML root. It therefore failed the repository’s transport/structure gate despite having relevant content.

## Latest expansion — U.S. Courts judiciary RSS

- Added notification-off **U.S. Courts — Judiciary News** from the official [U.S. Courts RSS directory](https://www.uscourts.gov/rss-feeds) and stable HTTPS [Judiciary News RSS feed](https://www.uscourts.gov/news/rss). The documented legacy endpoint redirects to this HTTPS URL. Three repeated HTTP 200 `application/rss+xml` probes were byte-identical at **6,265 bytes**, with **10 dated, unique items through 18 August 2026**, 10 unique article links and zero exact or conservative-fuzzy title/link overlap with the cached Master corpus.
- The compact source adds first-party federal-judiciary, bankruptcy, wiretap-data, court-modernisation and legal-system signal to both Air and Lite for quiet Apple Intelligence digest review. Its 10 article permalinks are legacy HTTP, recorded as the expected transport warning under the verified HTTPS feed policy.
- The deterministic bundle is now **495 Master / 119 Air / 112 Lite**, with **406 Finance / 89 Cyber Security** in Master. The final live reports accept **494/495 Master** (the retained CEPR malformed HTTP 200 body remains the only stable hard failure), **119/119 Air** and **112/112 Lite**. Master measured **52,926,866 body bytes / 28,926,208 wire bytes**; Air measured **4,088,202 / 1,963,661**, leaving **106,102 bytes**; Lite measured **3,999,528 / 1,941,406**, leaving **194,776 bytes** below the 4 MiB ceiling. Both phone profiles pass their device budgets with no failed feeds or critical regressions.
- Three existing National Bank of Poland rate feeds briefly returned HTTP 503 during the first Master pass, but immediate probes recovered them and the final rerun returned 495/495 HTTP 200 responses. No unrelated NBP change was made.

## Latest expansion — RUSI, Banco Central do Brasil, African Development Bank, SIPRI and Chatham House RSS

- Added notification-off **RUSI — Latest Commentary** from the official [RUSI RSS directory](https://www.rusi.org/rusi-rss-feeds) and direct [Latest Commentary feed](https://www.rusi.org/rss/latest-commentary.xml). Three repeated HTTP 200 `application/xml` probes were byte-identical at **15,107 bytes**, with **20 unique dated items through 20 August 2026**, complete HTTPS links and zero exact or conservative-fuzzy overlap with the cached Master corpus. It adds compact independent defence/security, geopolitical-risk, cybercrime, critical-infrastructure, defence-finance and strategic-resilience research to both phone profiles.
- Added notification-off, Master-only **Banco Central do Brasil — News (Portuguese)** from the official [BCB RSS directory](https://www.bcb.gov.br/en/about/rssen) and direct [News Atom feed](https://www.bcb.gov.br/api/feed/sitebcb/sitefeeds/noticias). Three repeated HTTP 200 `application/atom+xml` probes were byte-identical at **53,519 bytes**, with **10 unique dated items through 17 August 2026**, complete HTTPS links and zero exact title/link overlap with the cached Master corpus. It adds primary Brazilian central-bank signal on Pix/payments, virtual-asset regulation, foreign exchange, Open Finance and financial-system supervision without inflating the focused phone layer.
- Promoted the existing English [BCB Focus Market Readout feed](https://www.bcb.gov.br/api/feed/sitebcb/sitefeedsen/focusmarketreadout) into Air and Lite after three repeated HTTP 200 probes returned a stable **7,369-byte** body with **10 unique dated items through 14 August 2026**. The English stream keeps the phone layer’s Brazilian macro signal compact and readable; larger BCB research/minutes feeds remain Master-only.
- Added notification-off, Master-only **African Development Bank — News & Events** from the official [AfDB RSS directory](https://www.afdb.org/en/rss-feeds) and direct [News & Events RSS feed](https://www.afdb.org/en/news-and-events/rss). Three repeated HTTP 200 `application/rss+xml` probes were byte-identical at **17,344 bytes**, with **20 unique dated items through 21 August 2026**, complete HTTPS item links and zero exact or conservative-fuzzy overlap with the cached Master corpus. It adds African development-finance, infrastructure, energy-security, trade, climate-resilience and regional economic-development intelligence distinct from the existing Asian, Caribbean and global development-bank sources; it remains outside Air/Lite because those profiles are at their declared caps.
- Added notification-off **SIPRI — Global Security & Arms Control** from the official [SIPRI RSS page](https://www.sipri.org/rss) and direct [combined RSS feed](https://www.sipri.org/rss/combined.xml). Three repeated HTTP 200 `application/rss+xml` probes were byte-identical at **7,600 bytes**, with **10 unique dated items through 17 August 2026**, complete HTTPS item links and zero exact or conservative-fuzzy overlap with the cached Master corpus. It is included in Air and Lite as a compact strategic-security research source.
- Added notification-off, Master-only **Chatham House — Expert Comment** and **Chatham House — News Releases** from the official [RSS directory](https://www.chathamhouse.org/rss-feeds), using the direct [Expert Comment feed](https://www.chathamhouse.org/path/83/feed.xml) and [News Releases feed](https://www.chathamhouse.org/path/news-releases.xml). Their stable current windows were 50 items in **758,453** and **333,463** body bytes, with zero exact or conservative-fuzzy overlap against the cached Master corpus. The broader What's New stream was not retained because it overlaps 29 Expert Comment items and costs more mobile refresh budget.
- The deterministic bundle is now **494 Master / 118 Air / 111 Lite**, with **405 Finance / 89 Cyber Security** in Master. The final live audits accepted **493/494 Master** feeds, **118/118 Air** feeds and **111/111 Lite** feeds. Master measured **52,934,714 body bytes / 28,996,280 wire bytes** and retains the known CEPR malformed HTTP 200 response as its only stable hard failure; Air measured **4,081,682 / 1,962,019**, leaving **112,622 bytes**, and Lite measured **3,993,303 / 1,939,327**, leaving **201,001 bytes** below the 4 MiB ceiling. SIPRI is phone-safe, while the two Chatham House streams remain Master-only for deeper Apple Intelligence digest coverage.

## Latest expansion — Apple first-party RSS and phone rebalance

- Added notification-off **Apple Newsroom** from Apple’s official [RSS directory](https://www.apple.com/ca/rss/), using the direct [Newsroom RSS endpoint](https://www.apple.com/newsroom/rss-feed.rss). Three repeated validator-compatible probes returned stable HTTP 200 Atom/XML at **18,428 body bytes**, with **20 dated, unique items through 18 August 2026**, complete HTTPS links and zero exact title, link or conservative-fuzzy overlap with the cached Master corpus. It is included in both Air and Lite for first-party Apple company, iOS, Apple Intelligence, privacy and EU platform-policy signal.
- Added notification-off, **Master-only Apple Developer — News** from the same official directory, using [Apple’s Developer News RSS endpoint](https://developer.apple.com/news/rss/news.rss). Three repeated probes returned stable HTTP 200 RSS/XML at **433,267 body bytes**, with **142 dated items through 18 August 2026**, **121 unique titles**, **142 unique HTTPS links** and zero exact title/link overlap with the cached Master corpus. It adds platform, API, SDK, Apple Intelligence implementation, privacy, signing, App Store and EU implementation detail; its archive-heavy body stays outside the phone profiles.
- To make the compact Newsroom feed fit, **New Zealand NCSC — News** moved from Air/Lite to Master-only. Both **Canadian Centre for Cyber Security** feeds were removed/deferred after their official subscription page still advertised RSS but the current endpoints redirected to Atom paths with inconsistent or zero-byte responses under repeated validator-compatible fetches. **SANS Internet Storm Center** was also deferred after both publisher-listed RSS URLs returned HTML under HTTP 200; all three publisher lanes remain documented recheck targets.
- The deterministic bundle is now **488 Master / 115 Air / 108 Lite**, with **403 Finance / 85 Cyber Security** in Master. The current phone audits pass **115/115 Air** and **108/108 Lite** with no feed failures or device-budget failures. Air measures **4,038,543 body bytes / 1,976,791 wire bytes**, leaving **155,761 bytes** below the 4 MiB ceiling; Lite measures **3,923,859 / 1,951,392**, leaving **270,445 bytes**. Master measures **51,637,245 body bytes / 28,624,605 wire bytes** and retains the known CEPR malformed HTTP 200 response as the only stable hard failure; the validator reports zero noisy feeds, zero duplicate URLs, zero critical regressions and matching manifest/source/OPML URL sets. Three non-critical watches remain: the dynamic Athens redirect, a Bank of Japan item-link transport change and a South African Reserve Bank title flip.

## Latest expansion — Euronext market-operations RSS

- Added notification-off **Euronext — Market Status** from the official [Market Status page](https://live.euronext.com/en/market-status) and direct [Market Status RSS endpoint](https://live.euronext.com/en/market-status/rss-feed). Euronext describes the service as a free RSS/email channel for near-real-time degradation or interruption alerts across its cash and derivatives markets. Three repeated HTTPS probes returned HTTP 200 `text/plain` XML bodies of **694 bytes** with a valid RSS root and no active items, the expected healthy state; it is included in both phone profiles as a quiet digest source.
- Added notification-off, Master-only **Euronext Athens — Market Notices** from the official [Euronext Athens RSS directory](https://athens.euronext.com/en/rss) and direct [Market Notices feed](https://athens.euronext.com/en/rss/market-notices). Three repeated HTTP 200 RSS/XML probes returned **23,634-byte** bodies with **20 dated, unique records through 21 August 2026**, complete HTTPS item links and zero overlap with the current Master corpus. It adds primary exchange bulletins, corporate-action notices and index-composition changes; it remains Master-only because it is Athens-specific and dynamically takes about two seconds to fetch.
- The deterministic bundle is now **489 Master / 116 Air / 109 Lite**, with **401 Finance / 88 Cyber Security** in Master. The final phone audits passed **116/116 Air** and **109/109 Lite** with zero feed failures, regression warnings or device-budget failures. Air measured **4,185,313 body bytes / 1,994,890 wire bytes**, leaving **8,991 bytes** below the 4 MiB ceiling; Lite measured **4,095,838 / 1,971,017**, leaving **98,466 bytes**. The event-driven empty-feed policy is now exercised by Euronext Market Status and records its healthy no-active-alert state.
- The final Master audit accepted **488/489** feeds; the retained CEPR Discussion Papers endpoint remains malformed despite HTTP 200. The three remaining Master regression warnings are non-critical CDC publisher-title/redirect drift and the dynamic Athens Market Notices redirect target. BLS’s official Latest Numbers endpoint returned HTTP 403, and FINRA’s documented feeds remain HTTP-only/unreliable over HTTPS; neither lane was imported.

## Latest expansion — National Futures Association derivatives RSS

- Added seven official notification-off, Master-only NFA streams from the [NFA RSS directory](https://www.nfa.futures.org/news/rss.asp): [Manual Updates](https://www.nfa.futures.org/rss/manualRSS.xml), [News Releases](https://www.nfa.futures.org/rss/newsReleasesRSS.xml), [Notices to Members](https://www.nfa.futures.org/rss/noticesRSS.xml), [Board Updates](https://www.nfa.futures.org/rss/boardUpdatesRSS.xml), [Comment Letters](https://www.nfa.futures.org/rss/commentLettersRSS.xml), [CFTC Rule Submission Letters](https://www.nfa.futures.org/rss/ruleSubmissionsRSS.xml) and [Regulatory Actions](https://www.nfa.futures.org/rss/regActionsRSS.xml).
- Three repeated HTTP 200 `text/xml` probes were byte-identical for every stream: **2,071 bytes** for Manual Updates (two dated records through 1 July 2026), **1,184** for News Releases (one through 23 July), **673** for Notices to Members (one through 29 July), **872** for Board Updates (one through 25 June), **697** for Comment Letters (one through 6 March), **1,846** for CFTC Rule Submission Letters (two through 21 August) and **695** for Regulatory Actions (one through 19 August). All 9 records across the seven feeds had unique titles, complete HTTPS item links and parseable dates; the combined body contribution is **8,038 bytes**.
- Exact title/link and conservative-fuzzy screening found zero overlap with the current Master cache and zero cross-candidate overlap. The additions provide derivatives rulebook, member-notice, self-regulatory governance, consultation, CFTC rule-submission and disciplinary-action context distinct from the retained CFTC press, enforcement and testimony streams. Their sparse event-driven cadence is intentional and uses a 365-day stale-review window.
- The deterministic bundle is now **487 Master / 115 Air / 108 Lite**, with **399 Finance / 88 Cyber Security** in Master. The seven NFA feeds remain outside Air/Lite and carry no interrupting notification cost; the current deferred ACSC, CFTC Federal Register and Central Bank of Ireland Research Exchange rechecks remain unimported.
- The final live Master rerun accepted **486/487** feeds, while Air and Lite accepted **115/115** and **108/108**. Master measured **53,274,371 body bytes / 30,553,369 wire bytes** and retained only the malformed CEPR Discussion Papers failure, with zero regression warnings or critical regressions. Air measured **4,165,891 body bytes / 2,018,306 wire bytes**, leaving **28,413 bytes** of headroom; Lite measured **4,076,938 / 1,995,337**, leaving **117,366 bytes**. Both phone reports contain one tolerated Council of the EU scheduled-item timestamp under the scoped four-hour feed-specific clock tolerance and no hard future-date failures. All seven NFA feeds passed their live XML, date, link and freshness gates.

## Latest expansion — OCC banking-supervision RSS

- Added four official notification-off and Master-only OCC streams from the [OCC RSS directory](https://www.occ.treas.gov/rss/index-rss.html): [News Releases](https://www.occ.treas.gov/rss/occ_news.xml), [Speeches](https://www.occ.treas.gov/rss/occ-speeches.xml), [Congressional Testimony](https://www.occ.treas.gov/rss/occ-congressional-testimony.xml) and [Publications](https://www.occ.treas.gov/rss/occ-publications.xml). The existing OCC Bulletins stream remains in the phone profiles.
- Three repeated validator-style probes were byte-identical for each new stream: **9,479 bytes** for News Releases (10 dated records through 19 August 2026), **8,070 bytes** for Speeches (10 through 6 August), **8,804 bytes** for Congressional Testimony (10 through 4 June) and **9,854 bytes** for Publications (10 through 30 June). Every stream had 10 unique titles, 10 unique HTTPS item links and no missing links.
- Exact title/link and conservative-fuzzy screening found one expected joint-agency title cross-post for OCC News Releases with the retained OCC Bulletins feed, zero exact link overlap and no additional fuzzy overlap; the other three streams had zero overlap with the current Master cache. They add national-bank supervision, digital-asset, chartering, leadership, congressional-oversight, trading, derivatives, cybersecurity and financial-resilience context.
- The bundle is now **480 Master / 116 Air / 108 Lite**, with **392 Finance / 88 Cyber Security** in Master. These four feeds remain outside Air/Lite and add **36,207 bytes** of Master body payload without mobile cost or notification cost. The deferred ACSC, CFTC Federal Register and Central Bank of Ireland Research Exchange rechecks again failed their transport/item-link gates and were not imported.
- The completed live reports accept **479/480 Master**, **116/116 Air** and **108/108 Lite**. Master measured **53,335,907 body bytes / 30,833,122 wire bytes** and retains only the malformed CEPR Discussion Papers failure; the five non-critical warnings are four expected OCC feed-added notices plus an EEA Featured Articles item-link transport regression. Air measured **4,188,487 / 1,985,810** with **5,817 bytes** of headroom; Lite measured **4,036,132 / 1,935,705** with **158,172 bytes** of headroom. Both phone profiles pass with zero warnings.

## Latest expansion — SEC and CFTC testimony RSS

- Added official, notification-off and Master-only [SEC — Testimony](https://www.sec.gov/news/testimony.rss) from the [SEC RSS directory](https://www.sec.gov/about/rss-feeds), plus [CFTC — Speeches and Testimony](https://www.cftc.gov/RSS/RSSST/rssst.xml) from the [CFTC RSS directory](https://www.cftc.gov/RSS/index.htm). Three repeated validator-style probes were byte-identical for each endpoint: **16,308 bytes** for SEC (25 dated records, 18 unique titles, 25 unique HTTPS permalinks through 12 February 2026) and **4,798 bytes** for CFTC (10 dated, unique records through 20 August 2026). Both streams passed HTTP 200, RSS/XML, title/date/link, freshness and noise checks.
- Exact title/link screening and conservative-fuzzy screening found zero overlap with the cached Master corpus for both candidates. SEC adds congressional testimony and committee context beyond its press-release and speeches/statements feeds; CFTC adds commissioner remarks, testimony and derivatives-policy context beyond its press-release and enforcement streams.
- The deterministic bundle is now **476 Master / 116 Air / 108 Lite**, with **388 Finance / 88 Cyber Security** in Master. Both additions remain notification-off and outside Air/Lite because the phone profiles are at their declared caps and the current Air audit leaves **5,340 bytes** below the 4 MiB full-body ceiling. The live reports pass **116/116 Air** and **108/108 Lite** with zero warnings; Master accepts **475/476**, with only the pre-existing malformed CEPR Discussion Papers endpoint failing. The Master report has three non-critical warnings: Eurofound and CDC publisher-title changes, plus an EEA item-link transport regression.

## Latest expansion — Afreximbank Research Journal of African Trade RSS

- Added official, notification-off and Master-only [Afreximbank Research — Journal of African Trade](https://jat.afreximbank.com/recent.rss) from the [Journal of African Trade RSS page](https://jat.afreximbank.com/announcements.html). Three repeated HTTP 200 `application/rss+xml` probes were byte-identical at **29,917 bytes**, with 20 dated, unique records through 4 June 2026 and complete HTTPS article permalinks.
- Exact title/link screening and conservative-fuzzy title screening found zero overlap with the cached Master corpus. The stream adds AfCFTA, intra-African trade, tariff, fiscal-stability, trade-finance and African economic-growth research distinct from the existing development-bank and global trade-policy coverage. It remains outside Air/Lite because the phone profiles are at their declared caps.
- The deterministic bundle is now **474 Master / 116 Air / 108 Lite**, with **386 Finance / 88 Cyber Security** in the Master set. The fresh live reports accept **473/474 Master**, **116/116 Air** and **108/108 Lite**; Master has one retained CEPR malformed-body failure and four non-critical regression warnings, while both phone profiles remain clean and inside their payload budgets. CDB remains the immediately preceding Master-only addition.

## Previous expansion — Caribbean Development Bank News Releases RSS

- Added official, notification-off and Master-only [Caribbean Development Bank — News Releases](https://www.caribank.org/taxonomy/term/523/feed) from the [CDB News Releases page](https://www.caribank.org/publications-and-resources/resource-library/news-releases). Three repeated HTTP 200 `application/rss+xml` probes were byte-identical at **89,075 bytes**, with 10 dated, unique records through 6 August 2026 and complete HTTPS item links.
- Exact title/link screening and conservative-fuzzy title screening found zero overlap with the cached Master corpus. CDB adds Caribbean development-finance, climate-resilience, public-debt, energy-transition, trade-finance and regional economic-development intelligence distinct from the existing Asian, European and global development-bank coverage. It remains outside Air/Lite because the phone profiles are at their declared caps.
- At that checkpoint, the deterministic bundle was **473 Master / 116 Air / 108 Lite**, with **385 Finance / 88 Cyber Security** in the Master set. The current state is recorded in the Afreximbank expansion above.

## Previous expansion — Asian Infrastructure Investment Bank RSS

- Added official, notification-off and Master-only [Asian Infrastructure Investment Bank — News](https://aiib.org/en/rss/aiib-news-rss.xml) and [Asian Infrastructure Investment Bank — Blogs](https://aiib.org/en/rss/aiib-blogs-rss.xml) from the [AIIB RSS directory](https://aiib.org/en/rss/index.html). Three repeated HTTP 200 `text/xml` probes were byte-identical at **7,790 bytes** for News and **7,254 bytes** for Blogs; each returned 10 unique dated records with complete HTTPS item links, through 14 August and 18 August 2026 respectively.
- Exact title/link screening and conservative-fuzzy title screening found zero overlap with the cached Master corpus. The two streams add Asian infrastructure finance, climate resilience, regional connectivity, sustainable-finance and development-impact context distinct from the retained Asian Development Bank, EIB, EIF and central-bank research feeds. They remain outside Air/Lite because both phone profiles are already at their declared feed-count caps.
- At that checkpoint, the deterministic bundle was **472 Master / 116 Air / 108 Lite**, with **384 Finance / 88 Cyber Security** in the Master set. CDB is the subsequent Master-only addition; the current live state is recorded above.

## Current configured state

- **498 master feeds / 121 iPhone Air feeds / 114 iPhone-lite feeds**; 406 Finance and 92 Cyber Security sources in the master set.
- The phone layer keeps its declared 121-feed Air / 114-feed Lite maxima and 4 MiB limits while carrying **CIS — MS-ISAC Threat Level**, **CIS — MS-ISAC Advisories**, **Apple Newsroom**, **U.S. Courts — Judiciary News**, **RUSI — Latest Commentary**, **SIPRI — Global Security & Arms Control**, **Euronext — Market Status** and the compact official Irish, EU, UK, US and cyber-security coverage. **EUISS — News & Publications**, **Apple Developer — News**, **Euronext Athens — Market Notices**, **Chatham House — Expert Comment**, **Chatham House — News Releases** and the broader research and specialist feeds remain available in Master. The Canadian and SANS endpoints deferred in this expansion are not counted in the current profiles.

## Latest expansion — European Cybersecurity Competence Centre and Network RSS

- Added official, notification-off and Master-only [European Cybersecurity Competence Centre and Network — News](https://cybersecurity-centre.europa.eu/node/2/rss_en) from the [ECCC English News page](https://cybersecurity-centre.europa.eu/news_en?page=0). Three repeated HTTP 200 `application/rss+xml` probes were byte-identical at **39,378 bytes**, with 30 dated, unique records through 23 June 2026 and complete HTTPS item links.
- Exact title and link screening found zero overlap with the cached Master corpus, and conservative-fuzzy title screening found no overlap. The stream adds EU cybersecurity funding calls, critical-infrastructure and submarine-cable resilience, National Coordination Centre governance, cyber-skills and programme-delivery context distinct from the retained European Commission Digital Strategy, CERT-EU advisory and national-CSIRT feeds; it remains outside Air/Lite because the source is periodic and the phone payload is already at its declared ceiling.
- The current live audit is **470 feeds / 470 HTTP 200 / 469 accepted**. The known CEPR malformed-body response remains the only hard failure; ECCC itself passed every XML, date, link, freshness and noise gate. The report carries one expected non-critical ECCC `feed-added` warning and the existing non-critical Bank of Japan item-link transport watch.

## Latest expansion — UN Geneva meeting-summary RSS

- Added official, notification-off and Master-only [United Nations Office at Geneva — Meeting Summaries](https://www.ungeneva.org/news-media/meeting-summaries-list/rss.xml) from the [UN Geneva RSS directory](https://www.ungeneva.org/en/news-media/rss). Three repeated HTTP 200 RSS/XML probes were byte-identical at **9,107 bytes**, with 10 dated, unique records through 19 August 2026 and complete HTTPS item links.
- Exact title and link screening found zero overlap with the cached Master corpus, and conservative-fuzzy title screening found no overlap. The stream adds committee-level disability-rights, racial-discrimination, treaty-body review, diplomatic-credentials and multilateral-governance context distinct from the retained UN News and UN Meetings Coverage streams; it remains outside Air/Lite to preserve the near-ceiling phone payload.
- The current Master audit is **469 feeds / 469 HTTP 200 / 468 accepted**, with the retained CEPR malformed-body response as the only hard failure. The new feed itself passed all XML, date, link, freshness and noise checks; the only additional report signal is the expected non-critical `feed-added` regression warning.

## Latest expansion — Banca d’Italia English news RSS

- Added [Banca d’Italia — News (English)](https://www.bancaditalia.it/util/index.rss.html?sezione=/media/notizia&lingua=en) from the official [Banca d’Italia RSS directory](https://alert.bancaditalia.it/webApp/rss?LANGUAGE=en). Three repeated validator-style HTTP 200 probes were byte-identical at **3,322 bytes**, with three dated items through 19 August 2026, complete HTTPS item links and no internal noise; current Air title/link screening found zero exact overlap.
- This notification-off stream adds compact Italian balance-of-payments, public-finance, financial-market, payments, supervision and digital-euro context to both phone profiles. Live validation passed **115/115 Air** and **107/107 Lite**; Air measured **4,188,443 body bytes / 1,983,427 wire bytes**, leaving **5,861 bytes**, while Lite measured **4,036,354 / 1,934,173**, leaving **157,950 bytes**. Master is now **468 feeds** and the Air profile is intentionally left near its body ceiling.

## Latest expansion — Norges Bank press-release RSS

- Promoted [Norges Bank — Press Releases](https://www.norges-bank.no/en/rss-feeds/Press-releases---Norges-Bank/) into both phone profiles from the official [Norges Bank RSS directory](https://www.norges-bank.no/en/rss-feeds/). Three repeated validator-style HTTP 200 probes were byte-identical at **4,862 bytes**, with five dated items through 13 August 2026, complete HTTPS item links and no noise failure.
- The notification-off stream adds Norwegian policy-rate, foreign-exchange, payments and financial-stability context. Its repeated policy-rate title uses distinct article links and passed the validator’s duplicate checks. Live validation passed **116/116 Air** and **108/108 Lite**; Air measured **4,193,239 body bytes / 2,038,978 wire bytes**, leaving **1,065 bytes**, while Lite measured **4,041,063 / 1,990,374**, leaving **153,241 bytes**. Further phone additions now require a smaller feed or an explicit replacement/rebalance.

## Latest expansion — compact European policy RSS

- Promoted three existing official feeds into Air and Lite: [ECB Banking Supervision — Publications](https://www.bankingsupervision.europa.eu/rss/pub.html), [Deutsche Bundesbank — Speeches, Interviews & Contributions](https://www.bundesbank.de/service/rss/en/633296/feed.rss) and [Danmarks Nationalbank — Press Releases](https://www.nationalbanken.dk/api/rssfeed?topic=Press+release&lang=en). Their official directories are the [ECB Banking Supervision RSS page](https://www.bankingsupervision.europa.eu/home/html/rss.en.html), [Deutsche Bundesbank RSS page](https://www.bundesbank.de/en/homepage/rss/deutsche-bundesbank-s-rss-feed-620440) and [Danmarks Nationalbank RSS page](https://www.nationalbanken.dk/en/rss-feeds).
- Three repeated validator-style probes were byte-identical at **6,373**, **1,935** and **4,746 body bytes**, respectively, returning 15, two and five dated items through 12 August, 20 August and 4 August 2026 with complete HTTPS item links. No feed failed, became noisy or created a new duplicate-story cluster.
- Added one final compact official stream, [Danmarks Nationalbank — Market Announcements](https://www.nationalbanken.dk/api/rssfeed?topic=Market+announcement&lang=en), documented by the [Nationalbank RSS directory](https://www.nationalbanken.dk/en/rss-feeds). Three repeated probes were byte-identical at **3,349 body bytes**, returning five dated items through 23 June 2026 with complete HTTPS item links and no duplicate-story cluster.
- The final live audits passed **114/114 Air** and **106/106 Lite**. Air measured **4,184,975 body bytes / 1,982,066 wire bytes**, leaving **9,329 bytes**; Lite measured **4,032,863 / 1,933,326**, leaving **161,441 bytes**. Each report has only the one expected non-critical `feed-added` promotion warning; the Air profile is intentionally left with a small safety margin for feed-body drift.

## Latest expansion — compact RBA analysis, ECB statistics and Federal Reserve decision RSS

- Promoted five existing official feeds into Air and Lite: [RBA Bulletin](https://www.rba.gov.au/rss/rss-cb-bulletin.xml), [RBA Research Discussion Papers](https://www.rba.gov.au/rss/rss-cb-rdp.xml), [ECB Statistical Releases](https://www.ecb.europa.eu/rss/statpress.html), [Federal Reserve Banking Applications](https://www.federalreserve.gov/feeds/press_orders.xml) and [Federal Reserve Other Announcements](https://www.federalreserve.gov/feeds/press_other.xml). The [RBA RSS directory](https://www.rba.gov.au/updates/rss-feeds.html), [ECB RSS directory](https://www.ecb.europa.eu/home/html/rss.en.html) and [Federal Reserve RSS directory](https://www.federalreserve.gov/feeds/feeds.htm) document these first-party channels.
- Three repeated validator-style probes were byte-identical: **4,337**, **5,199**, **5,499**, **10,972** and **11,728 body bytes**, respectively. The feeds returned valid dated items and complete HTTPS links; the only current overlap is one expected ECB banknote announcement cross-posted with the general ECB news stream.
- The final live audits passed **110/110 Air** and **102/102 Lite**. Air measured **4,168,535 body bytes / 2,018,211 wire bytes**, leaving **25,769 bytes**; Lite measured **4,016,460 / 1,955,606**, leaving **177,844 bytes**. Both had zero feed failures, noise failures, duplicate URLs or device-budget failures; the five feed-added warnings are expected promotion notices.

## Latest expansion — Reserve Bank of Australia decision, stability and speech RSS

- Promoted four existing official RBA streams into Air and Lite from the [RBA RSS directory](https://www.rba.gov.au/updates/rss-feeds.html): [Media Releases](https://www.rba.gov.au/rss/rss-cb-media-releases.xml), [Financial Stability Review](https://www.rba.gov.au/rss/rss-cb-fsr.xml), [Statements on Monetary Policy](https://www.rba.gov.au/rss/rss-cb-smp.xml) and [Speeches](https://www.rba.gov.au/rss/rss-cb-speeches.xml). Three repeated HTTP 200 RDF/XML probes for each endpoint were byte-identical at **2,192**, **2,505**, **2,633** and **3,034 bytes**, with one dated record and a complete HTTPS item link in each stream. The latest records were 19 August, 19 March, 11 August and 13 August 2026.
- The compact feeds add Australian central-bank decisions and payments announcements, household/business/bank/non-bank resilience risk, inflation/output/employment/policy-outlook analysis and senior-officer policy commentary distinct from the Australian Treasury, FSB and Bank of Canada streams. They remain notification-off for the Apple Intelligence digest; the RBA directory identifies the FSR as half-yearly and the SMP as quarterly.
- The final live audits passed **105/105 Air** and **97/97 Lite**. The RBA streams passed all XML, date, link and duplicate checks; no RBA duplicate-story cluster was created. Air measured **4,130,855 body bytes / 1,997,581 wire bytes**, leaving **63,449 bytes** of headroom; Lite measured **3,978,685 / 1,961,849**, leaving **215,619 bytes**. Both had zero feed failures, noise failures, duplicate URLs or device-budget failures; the only regression warning was the expected RBA Speeches `feed-added` notice per phone report.

## Latest expansion — Bank of Canada Financial Stability Report promoted to phone

- Promoted existing official **Bank of Canada — Financial Stability Report** into Air and Lite. The Bank’s [Financial Stability Report page](https://www.bankofcanada.ca/publications/financial-stability-report/) describes the feed’s annual assessment of risks to Canada’s financial system; the direct [RSS feed](https://www.bankofcanada.ca/content_type/fsr/feed/) passed three repeated HTTP 200 `application/rss+xml` probes with identical 12,450-byte bodies, 10 dated and unique annual-report records through 28 May 2026, and 10 complete HTTPS item links.
- The periodic source adds household, business, banking, repo, private-credit and market-vulnerability assessments distinct from the existing Canadian press and market-notice feeds. It remains notification-off for the Apple Intelligence digest; the phone caps move to **101 Air / 93 Lite** while Master remains 467.
- The final live audits passed **101/101 Air** and **93/93 Lite**. Air measured **4,121,040 body bytes / 1,994,237 wire bytes**, leaving **73,264 bytes** of full-body headroom; Lite measured **3,968,937 / 1,945,675**, leaving **225,367 bytes**. Both had zero feed failures, noise failures, duplicate URLs or device-budget failures; each report carries only the expected non-critical Bank of Canada `feed-added` warning.

## Latest expansion — EIOPA insurance and pensions news promoted to phone

- Promoted existing official **EIOPA — News** into Air and Lite. EIOPA’s [Media page](https://www.eiopa.europa.eu/media_en) identifies the authority’s current insurance and occupational-pensions news; the direct [RSS feed](https://www.eiopa.europa.eu/node/4816/rss_en) passed three repeated HTTP 200 `application/rss+xml` probes with identical 47,344-byte bodies, 30 dated and unique records through 13 August 2026, and 30 complete HTTPS item links.
- The feed adds Solvency II, insurance conduct, occupational-pensions, DORA/cyber-risk, private-credit exposure and supervisory-resilience intelligence. Three EBA/EIOPA/ESMA joint or appeal headlines are deliberately retained as corroboration for Apple Intelligence clustering; the remaining current records are distinct. The phone caps move to **100 Air / 92 Lite** while Master remains 467.
- The affected live audits passed **100/100 Air** and **92/92 Lite** with zero failures, noisy feeds, duplicate URLs or budget breaches. Air measured **4,108,630 body bytes / 2,009,400 wire bytes** with **85,674 bytes** of headroom; Lite measured **3,956,527 / 1,960,266** with **237,777 bytes** of headroom. Each report carries only the expected non-critical EIOPA `feed-added` warning, and the two expected three-way joint-story clusters are available for digest deduplication.

## Latest expansion — Financial Stability Board news promoted to phone

- Promoted the existing official **Financial Stability Board — News** stream into Air and Lite. The FSB’s [RSS directory](https://www.fsb.org/rss-feeds/) documents RSS news feeds, and the live [feed](https://www.fsb.org/feed/) passed three repeated HTTP 200 `application/rss+xml` probes: identical 12,719-byte bodies, 10 dated and unique records through 10 August 2026, and 10 complete HTTPS item links.
- The compact source adds systemic-risk, regulatory-coordination, resolution-planning, cross-border-payments and market-resilience context. It remains notification-off and is routed to the quiet Apple Intelligence digest. The phone feed caps move to **99 Air / 91 Lite** while the Master set remains 467.
- The affected live audits passed **99/99 Air** and **91/91 Lite** with zero failures, noisy feeds, duplicate URLs or budget breaches. Air measured **4,050,451 body bytes / 2,000,355 wire bytes** with **143,853 bytes** of headroom; Lite measured **3,898,323 / 1,951,075** with **295,981 bytes** of headroom. Each report carries only the expected non-critical FSB `feed-added` warning.

## Latest expansion — EIF development-finance news and SRB phone promotion

- Promoted official **Single Resolution Board — News** into Air and Lite, and added official **European Investment Fund — News** to Master, Air and Lite. Both are notification-off digest sources in `02 — Core — Official & Macro`; the EIF stream adds EU SME finance, venture capital, InvestEU guarantees and development-finance activity, while SRB adds resolvability, crisis preparedness, MREL and resolution-policy context.
- The [EIF newsroom](https://www.eif.org/news-and-publications/newsroom/all-news) exposes the canonical [EIF RSS feed](https://www.eif.org/press/release/index.rss). Three repeated HTTP 200 `application/rss+xml` probes returned stable item signatures with 10 dated, unique records through 18 August 2026, complete HTTPS item links and a 5,687-byte body; only the feed-level publication timestamp changed. The [SRB RSS feed](https://www.srb.europa.eu/en/rss) returned stable 10-item signatures through 16 August 2026 in an 8,813-byte body. Both sources passed the final profile audits without duplicate URLs or noise failures.
- Fresh live reports accepted **466/467 Master** (the retained CEPR malformed-body exception), **98/98 Air** and **90/90 Lite**. Master measured **53,204,885 body bytes / 30,806,783 wire bytes**; Air measured **4,039,139 / 1,997,135** and Lite **3,886,724 / 1,947,762**. Air retained **155,165 bytes** of headroom and Lite **307,580 bytes**; both phone budgets passed with zero failures, and the Air and Lite audits reported zero noisy feeds and zero duplicate URLs.

## Latest expansion — ESRB publications and macroprudential policy RSS

- Added official, notification-off **European Systemic Risk Board — Publications & Research**, **Policy Warnings & Advice** and **National Macroprudential Notifications** from the [ESRB RSS directory](https://www.esrb.europa.eu/home/html/rss.en.html) and direct [publications feed](https://www.esrb.europa.eu/rss/pub.rss), [policy feed](https://www.esrb.europa.eu/rss/esrb_policy.rss) and [national-notifications feed](https://www.esrb.europa.eu/rss/nat_policy.rss). Three repeated probes per endpoint were byte-identical at **13,567**, **7,810** and **6,617 body bytes**, with 15 dated, unique records through 3 August, 7 July and 2 July 2026 respectively. Each had **15/15** valid HTTPS item links; exact title/link screening found zero overlap with the cached Master corpus and zero overlap between the three candidate streams.
- The Publications & Research and Policy Warnings & Advice streams are included in Air and Lite; National Macroprudential Notifications is Master-only because the phone profiles are at their declared feed caps and this is a specialist, lower-frequency policy stream. The two selected ESRB phone feeds add **21,377 body bytes** to each mobile profile. All three remain notification-off for local Apple Intelligence digest review.
- The current live reports accepted **465/466 Master**, **96/96 Air** and **88/88 Lite** feeds. Master measured **53,332,807 body bytes / 30,669,436 wire bytes** with the retained CEPR malformed-body failure and three non-critical feed-added warnings. Air measured **4,025,089 / 1,992,526** with **169,215 bytes** of headroom; Lite measured **4,030,452 / 1,913,620** with **163,852 bytes** of headroom. Both phone device-budget checks passed with zero noisy feeds; the ESRB streams themselves passed all XML, date, link and duplicate checks.

## Latest expansion — European Union Featured News RSS

- Added official, notification-off **European Union — Featured News** from the [EU Featured News page](https://european-union.europa.eu/news-and-events/featured-news_en) and direct [Featured News RSS feed](https://european-union.europa.eu/node/309/rss_en). Three repeated HTTP 200 `application/rss+xml; charset=utf-8` probes were byte-identical at 44,001 body bytes and returned 30 dated, unique records through 19 August 2026 with complete HTTPS item links. Exact-title screening found zero overlap with the cached Master corpus; four exact-link cross-posts are expected institutional republishes, and conservative fuzzy-title screening found no overlap.
- The feed adds cross-institution EU humanitarian, energy, environment, economy, security, justice, research and transport context. It is Master-only because its 44,001-byte body is larger than the remaining **32,782-byte** Air headroom; the phone profiles and their on-device Apple Intelligence digest surface remain bounded.
- The completed live reports accepted **462/463 Master**, **94/94 Air** and **86/86 Lite** feeds. Master measured **53,304,800 body bytes / 30,749,101 wire bytes** with the retained CEPR malformed-body failure and one non-critical feed-added warning for the new EU stream. The new stream itself passed **30/30** dated records and **30/30** HTTPS links at **44,001 body bytes / 8,807 wire bytes**. Air measured **4,161,522 / 1,956,156** with **32,782 bytes** of headroom; Lite measured **4,008,800 / 1,907,311** with **185,504 bytes** of headroom. Both phone device-budget checks passed with zero failures and zero noisy feeds.

## Latest expansion — IAEA Publications RSS

- Added official, notification-off **IAEA — Publications** from the [IAEA publications page](https://www.iaea.org/publications) and direct [Publications RSS feed](https://www.iaea.org/feeds/publications). Three repeated HTTP 200 `application/rss+xml; charset=utf-8` probes were byte-identical at 10,341 body bytes and returned 15 dated records through 10 August 2026 with 15 unique titles and links. Exact title/link screening found zero overlap with the cached Master corpus and conservative fuzzy-title screening found no overlap.
- The feed adds primary nuclear-safety, safeguards, nuclear-security, energy-systems, radiation-protection and nuclear-applications research beside **IAEA — News**. Its publication permalinks are legacy HTTP while the verified feed endpoint remains HTTPS; the validator accepts that publisher behavior with the normal transport warning. It is included in both phone profiles as a quiet Apple Intelligence digest source, with notifications off.
- The completed live reports accepted **461/462 Master**, **94/94 Air** and **86/86 Lite** feeds. Master measured **53,263,351 body bytes / 30,680,261 wire bytes** with one retained CEPR malformed-body failure and two non-critical regression warnings. Air measured **4,161,717 / 1,956,105** with **32,587 bytes** of headroom; Lite measured **4,009,035 / 1,907,337** with **185,269 bytes** of headroom. Both phone device-budget checks passed with zero failures and zero noisy feeds; the expected IAEA feed-added warning was non-critical.

## Latest expansion — Ireland NCSC guidance RSS

- Added official, notification-off **Ireland NCSC — Guidance Documents** from the [NCSC guidance page](https://www.ncsc.gov.ie/guidance/) and direct [Guidance RSS feed](https://www.ncsc.gov.ie/guidance/guidance.rss). Three repeated HTTP 200 `application/rss+xml` probes were byte-identical at 32,591 body bytes and returned 33 dated records through 6 July 2026 with 33 unique HTTPS document links. The single repeated title is the two distinct National Cyber Emergency Plan editions; exact title/link overlap with the current Master corpus was zero and conservative fuzzy-title screening found no overlap.
- The feed adds Irish cyber-governance, AI-security, NIS2, business-email-compromise, operational-technology and national-resilience guidance distinct from the existing Irish NCSC alert stream. It is included in both phone profiles as a compact, notification-off Apple Intelligence digest source; its measured body fits the declared 4 MiB Air and Lite budgets.
- The completed live reports accepted **459/461 Master**, **93/93 Air** and **85/85 Lite** feeds. Master has two current hard failures—Banco de la República’s HTTP 404 and CEPR’s malformed HTTP 200 body—plus one non-critical RWI feed-title-change warning and zero critical regressions. Air and Lite have zero failures and zero noisy feeds; their payloads are **4,151,084 bytes Air** and **3,998,451 bytes Lite**, leaving **43,220** and **195,853 bytes** respectively below the 4 MiB ceiling. NCSC itself passed **33/33** dated records and **33/33** HTTPS links in all three profiles.

## Previous expansion — Eurofound RSS

- Added official, notification-off **Eurofound — News** from the [Eurofound News and Events page](https://www.eurofound.europa.eu/en/news-and-events), the [Eurofound newsroom](https://eurofound.mynewsdesk.com/) and its direct [current-news RSS feed](https://eurofound.mynewsdesk.com/rss/current_news/58119). Three repeated HTTP 200 `application/xml` probes were byte-identical at 24,927 body bytes and returned 20 dated, unique records through 30 July 2026 with complete HTTPS item links. Exact-link overlap with the current Master corpus was zero; the one exact-title overlap, “Overheated and underprepared: European survey finds citizens concerned about heat and ability to cope with climate change”, is an expected cross-post with the retained European Environment Agency press stream.
- Eurofound adds independent EU living-and-working-conditions, employment, job-quality, industrial-relations and social-policy research distinct from the European Training Foundation, European Labour Authority and Commission employment streams. The compact source is included in both iPhone profiles for quiet Apple Intelligence digest review; its measured body fits the declared 4 MiB Air and Lite budgets.
- The completed live reports accepted **459/460 Master**, **92/92 Air** and **84/84 Lite** feeds. Eurofound passed **20/20** dated records and **20/20** HTTPS item links in each profile, with a 24,927-byte body and 6,052-byte wire response. Both phone budgets passed; CEPR remains the only hard feed failure and there were no critical regressions.

## Previous expansion — European Union Agency for Railways RSS

- Added official, notification-off **European Union Agency for Railways — News** from the [ERA News page](https://www.era.europa.eu/events-news/news_en), the agency’s [RSS guidance](https://www.era.europa.eu/content/stay-informed-receive-era-updates-directly) and direct [News RSS feed](https://www.era.europa.eu/events-news/news_en.xml). Three repeated HTTP 200 probes were byte-identical at 73,817 body bytes and returned 30 dated, unique records through 28 July 2026 with complete HTTPS item links. Exact-link overlap with the current Master corpus was zero; the one exact-title overlap, “Europe Day 2026”, is an expected institutional cross-post.
- ERA adds rail-safety, interoperability, climate resilience, ETCS/ATO, passenger-rights, technical-regulation, digitalisation and European transport-policy intelligence distinct from the existing general transport and aviation streams. The compact feed is included in both iPhone profiles for quiet Apple Intelligence digest review; its measured body fits within the declared 4 MiB Air and Lite budgets.
- The completed live audits accepted **458/459 Master**, **91/91 Air** and **83/83 Lite** feeds. ERA passed with **30/30** dated records and **30/30** HTTPS item links. Master measured **53,102,002 body bytes / 30,677,925 wire bytes**; Air measured **4,120,061 / 1,930,876** and Lite **3,967,521 / 1,868,975**, with both phone device-budget checks passing. The only hard feed failure is the retained malformed CEPR body; all regression warnings are non-critical.

## Previous expansion — European Training Foundation RSS

- Added official, notification-off and Master-only **European Training Foundation — News** from the [ETF newsroom](https://www.etf.europa.eu/en/news-and-events/news) and direct [RSS feed](https://www.etf.europa.eu/en/rss.xml). Three repeated HTTP 200 application/rss+xml probes were byte-identical at 229,706 bytes and returned 10 dated, unique records through 4 June 2026 with complete HTTPS item links. Exact-title and exact-link screening found zero overlap with the current Master corpus.
- ETF adds labour-migration, employability, green and digital skills, education reform and human-capital intelligence in EU partner countries, distinct from CEDEFOP’s European VET and labour-market stream. It is notification-off and Master-only with a 180-day event-driven stale-review window because ETF publishes in periodic policy and research cycles; it adds no phone payload or interrupting-notification cost.
- The current live reports returned HTTP 200 for **459/459** Master, **91/91** Air and **83/83** Lite endpoints. Master accepted **458/459** feeds because CEPR remains malformed; ETF passed all feed-level gates with **10/10** dated records, **10/10** HTTPS item links and a 229,706-byte body. The reports have zero noisy feeds, zero critical drift warnings and one explicit catalogue-update policy exception. Master measured **53,102,002 body bytes / 30,677,925 wire bytes**; Air/Lite measured **4,120,061 / 3,967,521 body bytes**.

## Previous expansion — Eurostat catalogue-update RSS

- Added official, notification-off and Master-only **Eurostat — Data and Data Structure Updates** from the [Eurostat RSS catalogue guide](https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access/api-detailed-guidelines/catalogue-api/rss) and direct [catalogue-update RSS feed](https://ec.europa.eu/eurostat/api/dissemination/catalogue/rss/en/statistics-update.rss). Three repeated HTTP 200 application/xml probes were byte-identical at 285,510 bytes and returned 920 dated, all-HTTPS records through 20 August 2026. The seven-day rolling window contains 633 unique normalized titles and 544 unique links; the validator measures 53.2% repeated titles and 65.3% repeated links because multiple dataset events reuse generic update titles and dataset pages. The explicit catalogue-update noise policy records those repeated records as the data-change payload rather than editorial duplication. Exact-title and exact-link screening found zero overlap with the current Master corpus.
- The feed is distinct from Eurostat’s existing news-release streams: it reports first-party dataset, data-structure and code-list creation, update and deletion events. Eurostat returns HTTP 406 when the validator’s normal RSS-specific Accept header is sent, but serves the same official XML document with the endpoint’s default curl negotiation; the validator now applies that transport exception only to this Eurostat catalogue path. The high-volume stream remains Master-only so it adds no iPhone payload or interrupting-notification cost.
- The current live audit accepted Eurostat at **981/981** valid dated records and **981/981** HTTPS item links with a 304,025-byte body. The high-volume structured-data stream remains Master-only; the explicit catalogue-update policy remains the only noise exception.

## Deferred candidate — CEDEFOP News RSS

- CEDEFOP’s [RSS directory](https://www.cedefop.europa.eu/en/news-and-events/rss-feeds) and direct [News RSS feed](https://www.cedefop.europa.eu/news-and-press/news.rss) initially passed three repeated probes at 29,283 bytes with 50 dated, unique records through 6 August 2026, zero exact-link overlap and one expected cross-post. The candidate adds vocational-education, skills-shortage, productivity, labour-market and human-capital intelligence; its Publications and Briefing Notes streams stop in January 2025, while Press Releases stops in September 2025.
- During the subsequent full live audit, the same official endpoint began redirecting to an HTML mathematical challenge (`/challenge`) and returned no parseable RSS/XML. It was removed from the active manifest rather than leaving a critical live failure or an RSS subscription that a phone reader cannot reliably consume. Re-screen the official directory before reconsidering it.

## Latest expansion — EMSA and European Commission Oceans & Fisheries RSS

- Added official **European Maritime Safety Agency — Latest News** from the [EMSA newsroom](https://www.emsa.europa.eu/newsroom/latest-news.html) and its canonical [RSS feed](https://www.emsa.europa.eu/newsroom/latest-news.feed?type=rss&format=feed). Three repeated HTTP 200 `application/rss+xml` probes returned 12,768-byte bodies; the item signatures were stable across all three probes, with 10 dated, unique records through 19 August 2026 and complete HTTPS item links. One probe changed only dynamic feed-level metadata. Exact-title, exact-link and conservative-fuzzy screening found zero overlap with the cached Master corpus. It adds maritime-safety, coast-guard cooperation, oil-pollution response, maritime surveillance/CISE, hydrogen-fuel and operational-resilience signal.
- Added official **European Commission — Oceans & Fisheries News** from the [Oceans and Fisheries newsroom](https://oceans-and-fisheries.ec.europa.eu/news_en) and direct [RSS feed](https://oceans-and-fisheries.ec.europa.eu/node/2/rss_en). Three repeated HTTP 200 `application/rss+xml` probes were byte-identical at 44,316 bytes, with 30 dated, unique records through 18 August 2026 and complete HTTPS item links. Two exact cross-posts are expected (Swedish fisheries state aid and bathing waters); the remaining records add distinct fisheries-management, aquaculture, seafood-market, maritime-security, blue-economy and ocean-resilience context.
- These two additions expand Master to **456 feeds / 370 Finance / 86 Cyber Security** and Air/Lite to **90/82**. Both are included in the phone profiles as notification-off digest feeds; the measured payload increase is 57,084 bytes, keeping both profiles below the 4 MiB full-body budget.
- The fresh live audits accepted **455/456 Master**, **90/90 Air** and **82/82 Lite**. The sole failure remains CEPR’s malformed Discussion Papers body; the Master report has two expected feed-added notices and one unrelated EEA item-link transport warning, while Air and Lite have only the two expected feed-added notices each. Device budgets pass at **3,971,067 bytes Air** and **3,816,740 bytes Lite**.

## Latest expansion — European Commission agriculture and enlargement RSS

- Added official, notification-off and Master-only **European Commission — Agriculture & Rural Development News** from the [Agriculture and Rural Development newsroom](https://agriculture.ec.europa.eu/news_en) and direct [RSS feed](https://agriculture.ec.europa.eu/node/2/rss_en). Three repeated HTTP 200 `application/rss+xml` probes were byte-identical at 43,141 bytes, with 30 dated, unique records through 30 July 2026, complete HTTPS item links and no conservative-fuzzy overlap with the current Master cache. One EU–Mexico summit item is an expected exact cross-post with an existing Commission press stream; the remaining records add CAP, agri-food trade, food-system resilience, farm and rural-economy context.
- Added official, notification-off and Master-only **European Commission — Enlargement & Eastern Neighbourhood News** from the [Enlargement and Eastern Neighbourhood newsroom](https://enlargement.ec.europa.eu/news_en) and direct [RSS feed](https://enlargement.ec.europa.eu/node/2/rss_en). Three repeated HTTP 200 `application/rss+xml` probes were byte-identical at 44,815 bytes, with 30 dated, unique records through 18 August 2026, complete HTTPS item links and zero exact-title, exact-link or conservative-fuzzy overlap with the current Master cache. The canonical feed redirects from the former neighbourhood-enlargement host; it adds accession, Eastern Neighbourhood, governance, humanitarian, resilience and geopolitical context.
- These two additions expand Master to **454 feeds / 368 Finance / 86 Cyber Security** while leaving Air/Lite at **88/80** and adding no phone payload or interrupting-notification cost. The active Economy and Finance RSS candidate was not added because its current 30-item window ends on 23 October 2025.

## Latest expansion — ASEAN and AMRO RSS

- Added official, notification-off and Master-only **ASEAN — News** from the [ASEAN main portal](https://asean.org/) and direct [News RSS feed](https://asean.org/category/news/feed/). Three repeated HTTP 200 `application/rss+xml` probes were byte-identical at 96,181 bytes, with 10 dated, unique records through 19 August 2026, complete HTTPS item links and no exact-title, exact-link or conservative-fuzzy overlap with the current Master cache. It adds Southeast Asian diplomatic, regional economic, trade, climate and geopolitical context.
- Added official, notification-off and Master-only **ASEAN+3 Macroeconomic Research Office — News & Research** from the [AMRO website](https://amro-asia.org/) and direct [RSS feed](https://amro-asia.org/feed/). Three repeated HTTP 200 `application/rss+xml` probes were byte-identical at 13,261 bytes, with 10 dated, unique records through 14 August 2026, complete HTTPS item links and no exact-title, exact-link or conservative-fuzzy overlap with the current Master cache. It adds ASEAN+3 macroeconomic surveillance, financial-stability research, seminars and policy analysis.
- Added official, notification-off and Master-only **ASEAN+3 Macroeconomic Research Office — Press Releases** from the [AMRO press-release page](https://amro-asia.org/category/press-releases/) and direct [RSS feed](https://amro-asia.org/category/press-releases/feed/). Three repeated HTTP 200 `application/rss+xml` probes were byte-identical at 13,884 bytes, with 10 dated, unique records through 31 July 2026, complete HTTPS item links and no overlap with the current Master cache. One Singapore resilience item is intentionally cross-posted with the general AMRO stream; the remaining records add distinct country consultations, outlooks and resilience assessments.
- These three additions expand Master to **452 feeds / 366 Finance / 86 Cyber Security** while leaving Air/Lite at **88/80** and adding no phone payload or interrupting-notification cost. NATO, OSCE, ASIC, RBNZ, EDPS, BNM, AIIB, ACSC and other screened candidates were not substituted where their current feed was missing, stale, blocked, malformed or unable to supply valid dated item records.

## Latest expansion — AFM, Ofgem, Ofcom, OFSI and UK Export Finance RSS

- Added official, notification-off and Master-only **AFM — Sector News (Dutch)** from the [AFM RSS directory](https://www.afm.nl/nl-nl/contact/woordvoering-pers-en-media/rss-feeds) and direct [sector-news RSS feed](https://www.afm.nl/nl-nl/rss-feed/nieuws-professionals). Three repeated HTTP 200 `text/xml` probes were byte-identical at 53,135 bytes, with 50 dated, unique records through 6 August 2026, complete HTTPS item links and zero exact or conservative fuzzy overlap with the cached Master corpus. It adds Dutch market-conduct, market-integrity, crypto, audit and pension-supervision context.
- Added official, notification-off and Master-only **Ofgem — Activity on GOV.UK** and **Ofcom — Activity on GOV.UK** from the [Ofgem organisation page](https://www.gov.uk/government/organisations/ofgem) and [Ofcom organisation page](https://www.gov.uk/government/organisations/ofcom), using their direct [Ofgem Atom feed](https://www.gov.uk/government/organisations/ofgem.atom) and [Ofcom Atom feed](https://www.gov.uk/government/organisations/ofcom.atom). Each was byte-identical across three HTTP 200 probes: Ofgem returned 20 dated records in 13,376 bytes through 5 August 2026, and Ofcom returned 20 dated records in 12,555 bytes through 16 July 2026. Each had complete HTTPS links, one expected cross-government Competition Act duplicate and one expected DESNZ annual-report fuzzy match; the remaining records add distinct UK energy-market, telecoms, online-safety, postal, spectrum and digital-resilience regulation.
- Added official, notification-off and Master-only **OFSI — Activity on GOV.UK** from the [OFSI organisation page](https://www.gov.uk/government/organisations/office-of-financial-sanctions-implementation) and direct [Atom feed](https://www.gov.uk/government/organisations/office-of-financial-sanctions-implementation.atom). Three repeated HTTP 200 probes were byte-identical at 12,601 bytes, with 20 dated, unique records through 17 August 2026, complete HTTPS item links and one expected exact Russia-sanctions-guidance cross-post. It adds direct sanctions notices, guidance, licensing and compliance activity beside the retained OFSI blog.
- Added official, notification-off and Master-only **UK Export Finance — Activity on GOV.UK** from the [UKEF organisation page](https://www.gov.uk/government/organisations/uk-export-finance) and direct [Atom feed](https://www.gov.uk/government/organisations/uk-export-finance.atom). Three repeated HTTP 200 probes were byte-identical at 13,350 bytes, with 20 dated, unique records through 12 August 2026, complete HTTPS item links and zero exact or conservative fuzzy overlap. It adds export-credit, guarantees, sovereign-risk, trade, supply-chain and strategic-economic-security context.
- These five additions expand Master to **449 feeds / 363 Finance / 86 Cyber Security** while leaving Air/Lite at **88/80** and adding no phone payload or interrupting-notification cost. Competition Appeal Tribunal and Office for Nuclear Regulation feeds were screened out as archive-heavy; no web-only or podcast source was substituted for a current RSS/Atom stream.
- The final live audit returned HTTP 200 for all **449/449** Master endpoints and accepted **448/449**; all five new feeds passed, and the only failure remains CEPR’s malformed Discussion Papers body. **Air 88/88** and **Lite 80/80** passed with device-budget checks passing and zero profile drift warnings; Master has zero critical drift warnings and five expected feed-added notices.

## Latest expansion — EIOPA, EU harmonised standards and UK DWP RSS

- Added official, notification-off and Master-only **EIOPA — News** from the [EIOPA media/news page](https://www.eiopa.europa.eu/media/news_en) and direct [RSS feed](https://www.eiopa.europa.eu/node/4816/rss_en). Three repeated HTTP 200 `application/rss+xml` probes were byte-identical at 47,344 bytes, with 30 dated, unique records through 13 August 2026, complete HTTPS item links and zero exact link overlap with the cached Master corpus. Three expected exact title overlaps are EBA/EIOPA/ESMA joint or appeal cross-posts; the remaining records add distinct EU insurance, occupational-pensions, Solvency II, conduct and operational-resilience supervision signal.
- Added official, notification-off and Master-only **European Commission — Harmonised Standards** from the [DG Internal Market RSS directory](https://single-market-economy.ec.europa.eu/rss_en) and direct [Harmonised Standards RSS feed](https://ec.europa.eu/newsroom/growth/feed?tpa_id=29399). Three repeated HTTP 200 XML probes were byte-identical at 22,731 bytes, with 27 dated, unique records through 16 July 2026, complete HTTPS item links and zero exact or conservative fuzzy overlap. The stream adds product-compliance, market-access, safety, industrial-policy and technical implementation signal; its window includes an older archive tail by design.
- Added official, notification-off and Master-only **UK Department for Work and Pensions — Activity on GOV.UK** from the [DWP organisation page](https://www.gov.uk/government/organisations/department-for-work-pensions) and direct [Atom feed](https://www.gov.uk/search/news-and-communications.atom?organisations%5B%5D=department-for-work-pensions). Three repeated HTTP 200 `application/atom+xml` probes were byte-identical at 13,343 bytes, with 20 dated, unique records through 17 August 2026, complete HTTPS item links and one expected cross-government duplicate. It adds official UK state-pensions, workplace-pensions, labour-market, welfare and household-financial-resilience signal.
- These three additions expand Master to **444 feeds / 358 Finance / 86 Cyber Security** while leaving Air/Lite at **88/80** and adding no phone payload or interrupting-notification cost. The EU standardisation-notification feed was excluded because two current records lack item links; the UK Pensions Ombudsman feed was archive-heavy, the Financial Ombudsman feed was stale, and ECA/EDPS, FSPO Ireland and the Pensions Authority Ireland had no direct current importable RSS/Atom endpoint in this pass.
- The final live audit accepted **443/444 Master feeds**; the three new feeds passed, and the single failure remains CEPR’s malformed Discussion Papers body. A transient GFSC HTTP 525 recovered on the repeat run; the report retains one non-critical GFSC publisher-title warning. **Air 88/88** and **Lite 80/80** passed with device-budget checks passing and zero profile drift warnings.

## Latest maintenance — European Commission public-health, climate and digital-policy RSS

- Added official, notification-off and Master-only **European Commission — Public Health News** from the [Health and Food Safety newsroom](https://health.ec.europa.eu/news_en) and direct [RSS feed](https://health.ec.europa.eu/node/2/rss_en). Three repeated HTTP 200 `application/rss+xml` probes were byte-identical at 32,970 bytes, with 30 dated, unique records through 19 August 2026, complete HTTPS item links and zero exact title or link overlap with the cached Master corpus. It adds EU health-security, medical-device, clinical-assessment, medicines, pandemic-preparedness and scientific-committee policy context distinct from ECDC, EFSA, EMA, CDC and FDA coverage.
- Added official, notification-off and Master-only **European Commission — Climate Action News** from the [Climate Action newsroom](https://climate.ec.europa.eu/news_en) and direct [RSS feed](https://climate.ec.europa.eu/node/2/rss_en). Three repeated HTTP 200 `application/rss+xml` probes were byte-identical at 42,884 bytes, with 30 dated, unique records through 14 August 2026 and complete HTTPS item links. Four item links and three normalized titles overlap the retained corpus, but the remaining records add EU ETS auction calendars, carbon-farming certification, carbon capture, climate resilience, clean-energy investment and transition-regulation signal.
- Added official, notification-off and Master-only **European Commission — Digital Strategy News** from the [Shaping Europe’s digital future newsroom](https://digital-strategy.ec.europa.eu/en/news) and direct [RSS feed](https://digital-strategy.ec.europa.eu/en/rss.xml). Three repeated HTTP 200 `application/rss+xml` probes were byte-identical at 67,031 bytes, with 10 dated, unique records through 18 August 2026, complete HTTPS item links and zero exact title or link overlap. It adds first-party EU AI Act, DSA/DMA, Cyber Resilience Act, semiconductor, telecoms, digital-identity and technology-resilience policy signal distinct from UK DSIT and operational cyber advisories.
- These three additions raise Master to **439 feeds / 353 Finance / 86 Cyber Security** while leaving Air/Lite at **88/80** and adding no phone payload or notification cost. The ECFIN RSS endpoint was screened out as stale despite its active webpage (latest feed item 23 October 2025); Irish Department of Finance, Revenue, CSO, DPC, UK PSR and U.S. BIS candidate URLs remained HTML, 404 or blocked, so no web page was substituted for a feed.
- The final live audit accepted **438/439 Master feeds**; the single failure is CEPR’s current Discussion Papers body, which returns HTTP 200 but contains a non-XML control character. Banco de la República passed after a transient first-run transport/body failure. **Air 88/88** and **Lite 80/80** passed cleanly, with zero profile drift warnings and device-budget checks passing.

## Latest maintenance — UK payments and pension-resilience RSS

- Added official, notification-off and Master-only **Payment Systems Regulator — Activity on GOV.UK** from the [GOV.UK organisation page](https://www.gov.uk/government/organisations/payment-systems-regulator) and direct [Atom feed](https://www.gov.uk/government/organisations/payment-systems-regulator.atom). Three repeated HTTP 200 `application/atom+xml` probes were byte-identical at 11,718 bytes, with 16 dated, unique records through 9 July 2026 and complete HTTPS item links. Exact title and link screening found zero overlap with the cached Master corpus; one conservative fuzzy match is the expected cross-posted annual-report headline with The Pensions Regulator. It adds primary payment-system, open-banking, card-scheme, consumer-protection and operational-resilience oversight.
- Added official, notification-off and Master-only **Pension Protection Fund — Activity on GOV.UK** from the [GOV.UK organisation page](https://www.gov.uk/government/organisations/pension-protection-fund) and direct [Atom feed](https://www.gov.uk/government/organisations/pension-protection-fund.atom). Three repeated HTTP 200 `application/atom+xml` probes were byte-identical at 13,171 bytes, with 20 dated, unique records through 9 July 2026 and complete HTTPS item links. Exact and conservative fuzzy title/link screening found zero overlap with the cached Master corpus. It adds pension compensation, levy, insolvency and long-term financial-resilience signal distinct from The Pensions Regulator.
- These two additions raise Master to **441 feeds / 355 Finance / 86 Cyber Security** while leaving Air/Lite at **88/80** and adding no phone payload or notification cost. The PSR standalone newsroom remains web-only; the official GOV.UK Atom feed provides the stable importable endpoint. The BIS page remains queued because its current HTML exposes no direct first-party RSS/Atom endpoint.
- The final live audit accepted **440/441 Master feeds**; PSR and PPF passed all structural, freshness, HTTPS-link and item checks, while the single failure remained CEPR’s malformed Discussion Papers body. **Air 88/88** and **Lite 80/80** passed with device-budget checks passing; Lite’s final pass followed a transient FTC HTTP 503 recovery. No critical drift warnings were introduced.

## Latest maintenance — UK pensions and EU labour/environment RSS expansion

- Added official, notification-off and Master-only **The Pensions Regulator — Activity on GOV.UK** from the [TPR organisation page](https://www.gov.uk/government/organisations/the-pensions-regulator) and direct [Atom feed](https://www.gov.uk/government/organisations/the-pensions-regulator.atom). Three repeated HTTP 200 `application/atom+xml` probes were byte-identical at 13,955 bytes, with 20 dated, unique records through 13 August 2026, complete HTTPS item links and zero exact or conservative fuzzy title/link overlap with the cached Master corpus. It adds UK workplace-pensions scheme funding, governance, automatic-enrolment compliance and pension-scam risk intelligence beside FCA and PRA coverage.
- Added official, notification-off and Master-only **European Labour Authority — News** from the [ELA news directory](https://www.ela.europa.eu/en/news-events/news) and direct [RSS feed](https://www.ela.europa.eu/rss.xml). Three repeated HTTP 200 `application/rss+xml` probes were byte-identical at 25,304 bytes, with 10 dated, unique records through 7 August 2026, complete HTTPS item links and zero exact or conservative fuzzy title/link overlap. It adds cross-border labour mobility, social-security coordination, joint inspections, declared work and labour-shortage intelligence.
- Added official, notification-off and Master-only **European Commission — Employment, Social Affairs & Inclusion News** from the [Employment, Social Affairs and Inclusion newsroom](https://employment-social-affairs.ec.europa.eu/news_en) and direct [RSS feed](https://employment-social-affairs.ec.europa.eu/node/2/rss_en), plus **European Commission — Environment News** from the [Environment newsroom](https://environment.ec.europa.eu/news_en) and direct [RSS feed](https://environment.ec.europa.eu/node/92/rss_en). Three repeated HTTP 200 probes were byte-identical for each: Employment returned 30 dated, unique records through 18 August 2026 in 46,535 bytes with one conservative fuzzy overlap; Environment returned 30 dated, unique records through 14 August 2026 in 39,883 bytes with two expected exact overlaps and one conservative fuzzy overlap. The streams add distinct EU labour-market, social-protection, circular-economy, climate-resilience, packaging, land, water and resource-security policy context.
- The four additions expand Master to **436 feeds / 351 Finance / 85 Cyber Security** while leaving Air/Lite at **88/80** and adding no phone payload or notification cost. The Irish Fiscal Advisory Council feed was rechecked but remains excluded because its latest item is from June 2024; no stale Irish fiscal archive was substituted for a current direct source.
- The final live audit recorded **Master 435/436 accepted** with the known CEPR parser failure, while **Air 88/88** and **Lite 80/80** passed cleanly. Manifest/artifact synchronization, documentation, hygiene, all 47 tests, shell syntax and whitespace checks also passed; no critical drift warnings were introduced.

## Latest maintenance — EU asylum intelligence RSS expansion

- Added official, notification-off and Master-only **European Union Agency for Asylum — Press Releases** from the [EUAA press-release page](https://www.euaa.europa.eu/news-events/press-releases) and direct [Press Releases RSS feed](https://euaa.europa.eu/category/press-releases/feed). Three repeated HTTP 200 `application/rss+xml` probes were byte-identical at 39,706 bytes, with 30 dated, unique records through 7 August 2026 and complete HTTPS item links.
- Exact title and link screening found zero overlap with the current Master cache. The feed adds first-party Common European Asylum System, reception, operational-support, migration and country-of-origin information alongside the existing Commission Migration & Home Affairs and Frontex streams.
- The publisher’s RSS channel title is empty, so the manifest supplies the stable NetNewsWire display title as a documented metadata exception; all item-level hard gates pass. The addition expands Master to **432 feeds / 347 Finance / 85 Cyber Security** while leaving Air/Lite at **88/80** and adding no phone payload or notification cost.

## Latest maintenance — EU fundamental-rights RSS expansion

- Added official, notification-off and Master-only **European Union Agency for Fundamental Rights — News** from the [FRA RSS directory](https://fra.europa.eu/en/content/rss) and direct [News RSS feed](https://fra.europa.eu/en/news-and-events/news.rss.xml). Three repeated HTTP 200 `application/rss+xml` probes were byte-identical, with 10 dated, unique records through 23 July 2026, complete HTTPS item links and a 1,544,916-byte full-text response.
- Exact title and link screening found no overlap with the current Master cache. The feed adds EU rule-of-law, privacy, AI/data-protection, migration, labour-exploitation and civil-liberties signal; its large full-text body is intentionally kept out of the iPhone profiles and notification layer.
- This addition expands Master to **431 feeds / 346 Finance / 85 Cyber Security** while leaving Air/Lite at **88/80**. Europol’s current official RSS endpoint was screened out because its items have no publication dates; FRA Publications remains screened out because its channel title is empty.

## Latest maintenance — UK judiciary and audit-regulation RSS expansion

- Canonicalized the existing **US GAO — Tax Policy & Administration Reports** URL to the official lowercase endpoint (`https://www.gao.gov/rss/topic/tax-policy-and-administration`) after the former mixed-case path began returning a 301; the feed content remains current RSS/XML and its coverage is unchanged.
- Added official, notification-off and Master-only **Courts and Tribunals Judiciary — Judgments** from the [Judiciary RSS directory](https://www.judiciary.uk/rss-feeds/) and direct [Judgments Atom feed](https://www.judiciary.uk/judgments/feed/). Three repeated HTTP 200 probes were byte-stable, with 10 dated, unique records through 19 August 2026, complete HTTPS item links and a 43,046-byte body; exact and conservative fuzzy title/link screening found zero overlap with the cached Master corpus.
- Added official, notification-off and Master-only **UK Financial Reporting Council — Activity on GOV.UK** from the [FRC organisation page](https://www.gov.uk/government/organisations/financial-reporting-council) and direct [Atom feed](https://www.gov.uk/government/organisations/financial-reporting-council.atom). The live response returned HTTP 200 Atom/XML with 20 dated, unique records through 16 July 2026, complete HTTPS item links and a 13,661-byte body; exact and conservative fuzzy title/link screening found zero overlap. It adds UK audit enforcement, accounting and actuarial standards, corporate reporting, stewardship and governance regulation.
- These additions expand Master to **430 feeds / 345 Finance / 85 Cyber Security** while leaving Air/Lite at **88/80** and adding no phone payload or notification cost. The FRC news-search variant was not added separately because it repeats the same ten GOV.UK records; the Judiciary announcements, publications and appointments feeds were screened out of this pass because they are appointments or prevention-of-future-death archives rather than stronger finance/cyber intelligence lanes.

## Latest maintenance — UK prosecution and courts RSS expansion

- Added official, notification-off and Master-only **UK Crown Prosecution Service — Activity on GOV.UK** from the [CPS organisation page](https://www.gov.uk/government/organisations/crown-prosecution-service) and direct [Atom feed](https://www.gov.uk/government/organisations/crown-prosecution-service.atom). The live response returned HTTP 200 Atom/XML with 20 dated, unique records through 19 August 2026, complete HTTPS item links and a 13,567-byte body. Sixteen records were distinct from the cached Master corpus; four repeated CPS/AGO or CPS/NCA releases were retained because the stream adds first-party prosecution coverage. The separate CPS news-search stream was excluded as redundant with this activity feed.
- Added official, notification-off and Master-only **HM Courts & Tribunals Service — Activity on GOV.UK** from the [HMCTS organisation page](https://www.gov.uk/government/organisations/hm-courts-and-tribunals-service) and direct [Atom feed](https://www.gov.uk/government/organisations/hm-courts-and-tribunals-service.atom). The live response returned HTTP 200 Atom/XML with 20 dated, unique records through 19 August 2026, complete HTTPS item links and an 11,062-byte body; exact and conservative fuzzy overlap screening found zero overlap with the cached Master corpus.
- These additions expand Master to **428 feeds / 343 Finance / 85 Cyber Security** while leaving Air/Lite at **88/80** and adding no phone payload or notification cost. Together they add direct UK prosecution, court, tribunal, hearing-list, fee and digital-justice signal beside the retained MoJ, AGO, NCA, SFO, Insolvency Service, PSFA and ECHR streams.

## Latest maintenance — UK justice and prosecution RSS expansion

- Added official, notification-off and Master-only **UK Ministry of Justice — Activity on GOV.UK** from the [Ministry of Justice organisation page](https://www.gov.uk/government/organisations/ministry-of-justice) and direct [Atom feed](https://www.gov.uk/government/organisations/ministry-of-justice.atom). The live response returned HTTP 200 Atom/XML with 20 dated, unique records through 19 August 2026, complete HTTPS item links and an 11,367-byte body.
- Added official, notification-off and Master-only **UK Attorney General's Office — Activity on GOV.UK** from the [Attorney General's Office organisation page](https://www.gov.uk/government/organisations/attorney-generals-office) and direct [Atom feed](https://www.gov.uk/government/organisations/attorney-generals-office.atom). The live response returned HTTP 200 Atom/XML with 20 dated, unique records through 19 August 2026, complete HTTPS item links and a 14,015-byte body.
- Exact title/link screening found zero overlap for both feeds against the cached Master corpus; the AGO stream also had zero conservative fuzzy-title overlap. Together they add current UK justice policy, tribunals, sentencing, prosecution, criminal-law and legal-risk signal beside the retained NCA, SFO, Insolvency Service and ECHR streams. The additions expand Master to **426 feeds / 341 Finance / 85 Cyber Security** while leaving Air/Lite at **88/80** and adding no phone payload or notification cost.
- A fresh ACSC recheck still failed at transport level (HTTP/2 `INTERNAL_ERROR`; HTTP/1.1 zero-byte timeouts) across the documented advisory, alert, threat, news, advice and publication paths. NATO/OSCE and other access-limited candidates remain queued rather than being substituted with HTML.

## Latest maintenance — European Court of Human Rights RSS expansion

- Added three official, notification-off and Master-only English HUDOC streams from the [ECHR RSS directory](https://www.echr.coe.int/en/echr-rss-feeds): [Press Releases](https://hudoc.echr.coe.int/app/transform/rss?length=20&library=echrengpress&query=contentsitename%3AECHR+AND+doctype%3DPR+AND+languageisocode%3AENG&rankingModelId=11111111-0000-0000-0000-000000000000&sort=kpdate+Descending&start=0), [Grand Chamber Judgments](https://hudoc.echr.coe.int/app/transform/rss?length=20&library=echreng&query=contentsitename%3AECHR+AND+languageisocode%3AENG+AND+%28%28documentcollectionid%3D%22GRANDCHAMBER%22%29%29&rankingModelId=11111111-0000-0000-0000-000000000000&sort=kpdate+Descending&start=0) and [Chamber Judgments and Decisions](https://hudoc.echr.coe.int/app/transform/rss?length=20&library=echreng&query=contentsitename%3AECHR+AND+languageisocode%3AENG+AND+%28%28importance%3D%221%22%29+OR+%28importance%3D%222%22%29+OR+%28importance%3D%223%22%29%29+AND+documentcollectionid%3D%22CHAMBER%22&rankingModelId=11111111-0000-0000-0000-000000000000&sort=kpdate+Descending&start=0). Each returned HTTP 200 `text/xml` with 20 dated, unique English records and complete HTTPS item links; current body sizes were 7,174, 6,648 and 6,644 bytes respectively. The feed server refreshes `lastBuildDate` at request time, but the item records were stable across repeated probes.
- Exact title and link screening found zero overlap with the current Master cache, and the Chamber query excludes Grand Chamber records to keep the case-law streams distinct. The three additions expand Master to **424 feeds / 339 Finance / 85 Cyber Security** while leaving Air/Lite at **88/80** and adding no phone payload or notification cost. EDPS and ECA paths remained blocked or without a direct current RSS endpoint; ACSC, AUSTRAC, NATO, OSCE and other access-limited candidates remain queued.

## Latest maintenance — FAO food-security and agrifood-market RSS expansion

- Added official, notification-off and Master-only **Food and Agriculture Organization of the United Nations — Newsroom** from the [FAO Newsroom](https://www.fao.org/newsroom/en) and direct [FAO Newsroom RSS feed](https://www.fao.org/feeds/fao-newsroom-rss). Three repeated HTTP 200 `application/rss+xml` probes were byte-stable with 11 dated, unique records through 18 August 2026, complete HTTPS item links and a 5,306-byte body. Exact title and link screening found zero overlap with the current Master cache; the current window covers Gaza food-system damage, food-system goals, the FAO Food Price Index, crop resilience and agrifood-market shocks.
- This compact source expanded the Master profile to **421 feeds / 336 Finance / 85 Cyber Security** while leaving Air/Lite at **88/80** and adding no phone payload. IEA, WFP, ILO, EBRD and World Bank guesses were not added because their tested paths returned 404, 403 or HTML; FAO’s advertised Stories path also returned 404 and remains excluded.

## Latest maintenance — UK trade, food-security, science-policy and Americas health RSS expansion

- Added official, notification-off and Master-only **UK Department for Business and Trade — Activity on GOV.UK**, **UK Department for Environment, Food & Rural Affairs — Activity on GOV.UK** and **UK Government Office for Science — Activity on GOV.UK** from the [DBT](https://www.gov.uk/government/organisations/department-for-business-and-trade), [DEFRA](https://www.gov.uk/government/organisations/department-for-environment-food-rural-affairs) and [Government Office for Science](https://www.gov.uk/government/organisations/government-office-for-science) organisation pages and their direct Atom feeds ([DBT](https://www.gov.uk/government/organisations/department-for-business-and-trade.atom), [DEFRA](https://www.gov.uk/government/organisations/department-for-environment-food-rural-affairs.atom), [GOS](https://www.gov.uk/government/organisations/government-office-for-science.atom)). Three repeated HTTP 200 Atom/XML probes were byte-stable: each returned 20 dated records, 20 unique titles, complete HTTPS item links and bodies of 13,000, 12,503 and 13,236 bytes respectively. DBT has one expected Growth Gateway cross-post with FCDO; DEFRA and GOS had no exact title or link overlap with the cached Master corpus.
- Added official, notification-off and Master-only **Pan American Health Organization — News** from the [PAHO media page](https://www.paho.org/en/media) and direct [RSS feed](https://www.paho.org/en/rss.xml). Three repeated HTTP 200 `application/rss+xml` probes were byte-stable with 10 dated, unique records through 17 August 2026, complete HTTPS item links and an 8,219-byte body; the current window covers cyberbullying prevention, earthquake response, measles surveillance and regional health-system resilience.
- The four additions expand the Master profile to **420 feeds / 335 Finance / 85 Cyber Security** while leaving Air/Lite at **88/80** and adding no phone payload. WHO Europe was not added because its legacy FeedBurner response was malformed XML; ACSC, AUSTRAC, NATO, OSCE and other access-limited or unavailable candidates remain in the next recheck queue.

## Latest maintenance — UK foreign-policy, resilience, health-security and UN RSS expansion

- Added official, notification-off and Master-only **UK Foreign, Commonwealth & Development Office — Activity on GOV.UK**, **UK Cabinet Office — Activity on GOV.UK** and **UK Department of Health and Social Care — Activity on GOV.UK** from their [FCDO](https://www.gov.uk/government/organisations/foreign-commonwealth-development-office), [Cabinet Office](https://www.gov.uk/government/organisations/cabinet-office) and [DHSC](https://www.gov.uk/government/organisations/department-of-health-and-social-care) organisation pages and direct Atom endpoints.
- Three repeated validator-style HTTP 200 Atom/XML probes were byte-stable: FCDO returned 20 dated, unique records in an 11,746-byte body; Cabinet Office returned 20 dated, unique records in 13,848 bytes; and DHSC returned 20 dated, unique records in 13,489 bytes. All item links were HTTPS. Exact pre-screening found zero FCDO overlaps, two expected Cabinet/PSFA National Fraud Initiative cross-posts and one expected DHSC/DSIT Life Sciences Healthcare Goals cross-post.
- Added official, notification-off and Master-only **United Nations — Meetings Coverage and Press Releases** from the [UN Meetings Coverage and Press Releases page](https://press.un.org/en) and direct [RSS feed](https://press.un.org/en/rss.xml). Three repeated HTTP 200 RSS/XML probes were byte-stable with 10 dated items, 9 unique normalized titles, 10 unique HTTPS links and a 7,219-byte body; the feed adds Security Council, sanctions, humanitarian and multilateral-policy context beside the existing UN News topic feeds.
- The four additions expand the Master profile to **416 feeds / 331 Finance / 85 Cyber Security** while leaving Air/Lite at **88/80** and adding no phone payload. WHO Global News was not added because its stable feed was nearly stale at 175 days; NATO and OSCE RSS candidates were not added because their advertised paths currently returned unavailable endpoints. ACSC, AUSTRAC and other access-limited candidates remain in the next recheck queue.

## Latest maintenance — WHO Africa public-health RSS expansion

- Added official, notification-off and Master-only **WHO Africa — Featured News** from the [WHO Regional Office for Africa RSS directory](https://afro.who.int/rss-feeds) and direct [Featured News RSS feed](https://afro.who.int/rss/featured-news.xml).
- Three repeated validator-style HTTP 200 RSS/XML probes were byte-stable, with 20 dated records, 17 unique titles and 17 unique HTTPS links; the current window reaches 19 August 2026. Exact and conservative three-day overlap screening against the cached Master corpus found zero overlap. The feed adds African outbreak, health-security, resilience and public-health context for deeper Apple Intelligence research.
- The refreshed Master report measures **49,384,563 body bytes / 28,115,254 wire bytes** across 412 feeds; the two phone profiles remain 88 Air / 80 Lite and the WHO feed consumes no phone payload.

## Latest maintenance — Asian Development Bank RSS expansion

- Added official, notification-off and Master-only **Asian Development Bank — News Releases** and **Asian Development Bank — Publications** from the [ADB RSS directory](https://www.adb.org/rss), using the documented [News Releases feed](https://feeds.feedburner.com/adb_news) and [Publications feed](https://feeds.feedburner.com/adb_publications).
- Three repeated validator-style HTTP 200 XML probes were stable for both streams: News Releases returned 20 dated items in an 11,463-byte body and Publications returned 10 dated items in a 6,416-byte body; titles and links were unique and all item links resolved to HTTPS. Exact and conservative three-day overlap screening against the cached Master corpus found zero overlap for either stream.
- The current Master report measures **49,235,051 body bytes / 28,109,225 wire bytes** across 411 feeds, with 409 successful feed checks. CEPR’s discussion-paper endpoint and Krebs on Security’s RSS endpoint remain the two existing publisher failures; fresh phone audits pass **88/88 Air** and **80/80 Lite**, with both device budgets passing. The documented ADB Research Publications candidate was rejected because its channel had no feed-level title.

## Latest maintenance — UK energy-security and digital/cyber-policy RSS expansion

- Added official **UK Department for Energy Security and Net Zero — Activity on GOV.UK** from the [DESNZ organisation page](https://www.gov.uk/government/organisations/department-for-energy-security-and-net-zero) and direct [Atom feed](https://www.gov.uk/government/organisations/department-for-energy-security-and-net-zero.atom). Three repeated HTTP 200 Atom/XML pulls were byte-stable with 20 dated, unique items and HTTPS links; the current Master response measured **13,557 body bytes / 13,557 wire bytes**. It is Master-only to preserve the phone payload for higher-priority daily signal.
- Added official **UK Department for Science, Innovation and Technology — Activity on GOV.UK** from the [DSIT organisation page](https://www.gov.uk/government/organisations/department-for-science-innovation-and-technology) and direct [Atom feed](https://www.gov.uk/government/organisations/department-for-science-innovation-and-technology.atom). Three repeated HTTP 200 Atom/XML pulls were byte-stable with 20 dated, unique items and HTTPS links; the current response measured **13,709 body bytes / 13,709 wire bytes**. It is included in both phone profiles for primary UK AI, telecoms-security, cyber-resilience and digital-policy context.
- Rebalanced the phone layer by moving **The Hacker News** to Master-only, keeping the profile counts at **88 Air / 80 Lite** while promoting a primary official source. The current live reports show **409 feeds with 407 successful Master responses** (the two pre-existing EEA timeouts remain visible), **88/88 Air** and **80/80 Lite**, with both device budgets passing. AUSTRAC’s exact RSS endpoint and the five ACSC endpoints remain deferred after local access timeouts and/or durability concerns.

## Latest maintenance — Bank of Finland Bulletin RSS promotion

- Added **Bank of Finland Bulletin — Articles** from the official [Bank of Finland Bulletin RSS information page](https://www.bofbulletin.fi/en/about-the-website/) and direct [articles RSS feed](https://www.bofbulletin.fi/rss/articles/). Three repeated HTTP 200 `text/xml` pulls were byte-stable, with ten dated items, ten unique titles and ten unique links; the final Master audit measured **11,486 body bytes / 3,363 wire bytes** and the newest item was 24 July 2026.
- Exact title/link screening against the cached Master corpus found **zero exact overlaps**. The feed adds Finnish monetary-policy, household-finance, financial-stability, payments, digitalisation and AI/cyber-risk analysis from a primary central-bank source.
- Promoted the Bulletin into both iPhone profiles by moving the quieter **DNB — Publications** stream to Master-only. This keeps Air/Lite at **88/80** and preserves the phone payload budget while retaining DNB Publications for the hourly Master collector and deeper Apple Intelligence research pass.
- The fresh phone audits passed **88/88 Air** and **80/80 Lite** with zero failures, warnings or device-budget breaches. The full Master audit passed **406/407** HTTP/XML checks; the only failure was the pre-existing EEA Maps and Charts endpoint timing out, while the new Bulletin feed passed transport, XML, date, title, link and freshness checks. The current Master report measured **49,205,451 body bytes / 28,011,208 wire bytes**, with 44 payload-review feeds, eight above 1 MiB and 20 slow-refresh advisories.

## Previous maintenance — Eurostat, St. Louis Fed and security-research RSS expansion

- Added **Eurostat — Industry, Trade & Services Releases** from the official [Eurostat RSS directory](https://ec.europa.eu/eurostat/web/rss) and direct Atom endpoint. Three repeated pulls were stable and returned 11 dated, unique records with HTTPS item links; the current response measured **10,848 body bytes / 1,512 wire bytes** and remained a small mobile payload. Exact and conservative fuzzy screening found no overlap with the existing Eurostat Economy & Finance release stream.
- Promoted the Eurostat industry/trade/services stream into both iPhone profiles by moving **RTÉ — Business** to Master-only. The phone count and budgets remain unchanged; the RTÉ feed remains available for broader Irish context in the Master bundle.
- Added seven notification-off, Master-only feeds: **Federal Reserve Bank of St. Louis — FRED Blog**, [On the Economy](https://www.stlouisfed.org/rss/page%20resources/publications/blog-entries) and [Review](https://www.stlouisfed.org/rss/page-resources/publications/review), plus [Google Security Blog](https://blog.google/security/rss/), [Krebs on Security](https://krebsonsecurity.com/feed/), [Rapid7 — Research](https://www.rapid7.com/blog/tag/research/rss/) and [Elastic Security Labs](https://www.elastic.co/security-labs/rss/feed.xml). The St. Louis Fed’s official [RSS directory](https://www.stlouisfed.org/rss) documents the feeds. Their live responses were valid and current, while the security feeds add distinct cloud, incident-response, threat-research and security-engineering coverage without consuming phone payload.
- The current Master audit passed **406/406** HTTP/XML transport and parsing checks with zero failed feeds, zero metadata/stale-review/noise failures, zero future-date failures and zero regression warnings. It measured **49,174,962 body bytes / 27,964,841 wire bytes**, with 39 payload-review feeds, eight above 1 MiB and 16 slow-refresh advisories. The validator and hourly collector now use a narrow neutral-identity plus HTTP/1.1 exception for the two St. Louis Fed RSS endpoints; the Japanese FSA stream is parsed in `Asia/Tokyo`, removing its false future-date watch.
- The companion phone audits passed **88/88 Air** at **3,945,630 body bytes / 1,938,464 wire bytes** and **80/80 Lite** at **3,789,844 / 1,888,159**. Both remain under the 4 MiB full-body ceiling with device budgets passing; their expected profile-drift entries are the Eurostat-in/RTÉ Business-out rebalance, not feed-health failures.

## Latest maintenance — Swiss National Bank monetary-policy and research RSS expansion

- Added **Swiss National Bank — Monetary Policy** from the official [SNB RSS and calendar-feed directory](https://www.snb.ch/en/services-events/digital-services/rss-calendar-feeds) and direct [Monetary Policy RSS feed](https://www.snb.ch/public/rss/en/mopo). Three repeated requests returned HTTP 200 XML with an RSS root, 13 dated items, 13 unique titles and complete HTTPS item links in a 6,445-byte body through 24 June 2026. Two policy-assessment stories are expected exact cross-posts with the existing SNB Press Releases stream; the other 11 records add curated policy-bulletin context.
- Added **Swiss National Bank — Research & Working Papers** from the same [SNB RSS directory](https://www.snb.ch/en/services-events/digital-services/rss-calendar-feeds) and direct [Research & Working Papers RSS feed](https://www.snb.ch/public/rss/en/papers). Three repeated requests returned HTTP 200 XML with an RSS root, 20 dated items, 20 unique titles and complete HTTPS item links in an 89,369-byte body through 8 July 2026; the current Master audit found no exact story or link duplicate involving this stream.
- The two additions contribute **95,814 body bytes / 95,814 wire bytes** to Master; Monetary Policy adds 6,445 body/wire bytes to Air and Research & Working Papers remains outside the phone payload. The final Master audit passed **398/398** HTTP/XML checks with zero failed feeds, zero metadata/stale-review/noise failures and two expected feed-added baseline warnings; it measured **47,958,738 body bytes / 27,584,872 wire bytes**, with 39 payload-review feeds, eight above 1 MiB and 17 slow-refresh advisories. The final Air audit passed **88/88** HTTP/XML checks at **3,963,869 body bytes / 1,944,002 wire bytes**, leaving 230,435 bytes below the 4 MiB ceiling; Lite passed **80/80** at **3,807,747 / 1,894,122**, leaving 386,557 bytes. The strict Master report retains two future-dated items in the pre-existing Japan FSA All News stream; both phone device-budget checks pass.

## Latest maintenance — European Economic and Social Committee policy RSS expansion

- Added **European Economic and Social Committee — News** from the official [EESC news page](https://www.eesc.europa.eu/en/news-media/news) and direct [RSS feed](https://www.eesc.europa.eu/en/news-media/news.rss). Three repeated live requests returned identical HTTP 200 `application/rss+xml` responses with 20 dated, unique records through 4 August 2026, complete HTTPS item links and a 42,525-byte body.
- Exact title/link and conservative fuzzy-overlap screening against the selected Council of the EU, European Parliament committee/plenary, and European Commission finance, competition and migration streams found no duplicate story. The feed adds first-party EU economic, social, energy, transport, digital and civil-society policy context, remains Master-only and is notification-off.

## Latest maintenance — UK parliamentary research RSS expansion

- Added **House of Commons Library — Research**, **House of Lords Library — Research** and **UK Parliament POST — Research** from the official [UK Parliament RSS directory](https://www.parliament.uk/site-information/rss-feeds/), the [Commons publisher page](https://api.parliament.uk/library-feeds/publishers/1), [Lords publisher page](https://api.parliament.uk/library-feeds/publishers/2) and [POST publisher page](https://api.parliament.uk/library-feeds/publishers/3). Their direct RSS endpoints are [Commons](https://api.parliament.uk/library-feeds/publishers/1.rss), [Lords](https://api.parliament.uk/library-feeds/publishers/2.rss) and [POST](https://api.parliament.uk/library-feeds/publishers/3.rss).
- Three repeated probes established stable HTTP 200 `application/rss+xml` delivery: Commons had 258 dated records, 258 unique titles, 255 unique HTTPS links and a 76,644-byte body; Lords had 47 records, 47 unique titles, 46 unique links and a 16,927-byte body; POST had 13 records, 13 unique titles and links and a 4,494-byte body. The final live report saw 259 Commons records after a normal publisher update. Revision-link pairs are accepted as source metadata, and exact title/link overlap screening against the prior Master cache found no duplicate story.
- The three feeds contribute official UK fiscal, economic, energy, financial-services, legislative, digital, cyber-resilience, science and public-policy research. Their final live body/wire contribution was **98,352 / 14,684 bytes**; all remain Master-only, notification-off and outside the iPhone payload.
- Repaired the existing **SANS Internet Storm Center — Full-Text RSS** source using the official [SANS RSS directory](https://isc.sans.edu/xml.html) and current [compact RSS feed](https://isc.sans.edu/rssfeed.xml). Three repeated requests returned identical HTTP 200 RSS/XML responses with ten dated, unique records through 19 August 2026, complete HTTPS item links and an 8,267-byte body; the former `rssfeed_full.xml` path now serves an HTML page despite a `text/xml` label. The repaired feed remains notification-off in Air/Lite and Master; its final wire measurements were 2,135 bytes in Master and 2,137 bytes in each phone profile.
- The current Master run passed **395/395** feed-level HTTP/XML checks with zero failed feeds, zero regression warnings and zero critical regressions. It measured **47,899,811 body bytes / 27,568,323 wire bytes**, with 38 payload-review feeds, eight above 1 MiB and 17 slow-refresh advisories. The strict wrapper remains nonzero only for three future-dated items across Japan FSA All News (two) and EUSPA News (one).
- The companion phone audits passed **87/87 Air** and **80/80 Lite**. Air measured **3,958,694 body bytes / 1,962,313 wire bytes**, leaving 235,610 bytes of headroom; Lite measured **3,826,979 / 1,894,370**, leaving 367,325 bytes. Both budgets passed with zero future-date, regression or critical warnings.

## Latest maintenance — U.S. Treasury and SEC policy RSS expansion

- Added **U.S. Treasury — Press Releases** from the official [Treasury press-release page](https://home.treasury.gov/news/press-releases) and its direct [GovDelivery RSS feed](https://public.govdelivery.com/topics/USTREAS_49/feed.rss). Three repeated live requests returned stable HTTP 200 RSS/XML responses with 25 dated items, 25 unique titles and links, complete HTTPS item links, and a latest item through 17 August 2026. The measured response was 232,615 body bytes and is retained Master-only because it provides first-party fiscal-policy, financial-regulation, sanctions and international-finance context.
- Added **SEC — Speeches and Statements** from the official [SEC RSS directory](https://www.sec.gov/about/rss-feeds) and direct [speeches/statements RSS feed](https://www.sec.gov/news/speeches-statements.rss). Three repeated live requests returned the same HTTP 200 RSS/XML payload with 25 dated items, 25 unique titles and links, complete HTTPS item links, and a latest item through 18 August 2026. The measured response was 11,785 body bytes and adds first-party securities-regulation, market-structure and investor-protection policy signal.
- The two additions contribute **244,400 body bytes / 235,421 wire bytes** and no phone payload or notification cost. SEC litigation, administrative-proceeding and trading-suspension feeds were not added after repeated validator-compatible access checks returned HTTP 403; Treasury’s daily interest-rate XML was also left out because it is a non-RSS data feed rather than an editorial stream.
- The final live reports show **392/392 Master**, **87/87 Air** and **80/80 Lite** successful HTTP/XML feed checks, with zero failed feeds, zero regression warnings and zero critical regressions. Master measured **47,806,198 body bytes / 27,579,490 wire bytes**; Air measured **4,020,417 / 1,974,429** and Lite **3,871,770 / 1,929,865**, with both device-budget checks passing. The strict reports retain four future-dated items across the pre-existing DNB General News, DNB Statistical News and Japan FSA All News feeds; the wrappers remain nonzero for those publisher-clock checks and the historical consecutive-failure alert.

## Previous maintenance — ESA space science and EASA regulatory-document RSS expansion

- Added two notification-off, Master-only **European Space Agency** streams from the official [ESA RSS directory](https://www.esa.int/Services/RSS_Feeds): [Space Science](https://www.esa.int/rssfeed/Our_Activities/Space_Science) and [Operations](https://www.esa.int/rssfeed/Our_Activities/Operations). Three repeated live requests for each returned stable HTTP 200 RSS/XML responses. Space Science contained 15 dated items, 15 unique titles and links and a 12,502-byte body through 17 August 2026; Operations contained 15 dated items, 15 unique titles and links and an 8,878-byte body through 13 August 2026.
- Added three notification-off, Master-only **European Union Aviation Safety Agency** regulatory-document streams from the official [EASA RSS page](https://www.easa.europa.eu/en/rss): [Agency Decisions](https://www.easa.europa.eu/en/document-library/agency-decisions/feed.xml), [Certification Specifications](https://www.easa.europa.eu/en/document-library/certification-specifications/feed.xml) and [Comment Response Documents](https://www.easa.europa.eu/en/document-library/comment-response-documents/feed.xml). Each passed three repeated HTTP 200 RSS/XML requests: Agency Decisions had 50 dated, unique items in 7,029 bytes through 14 July 2026; Certification Specifications had 50 dated items, 48 unique normalized titles and 50 unique links in 1,884 bytes through 14 July; Comment Response Documents had 50 dated, unique items in 1,526 bytes through 15 July.
- The five candidates add **31,819 body bytes** and no phone payload or notification cost. Exact overlap screening found zero title/link overlap for ESA Operations and all three EASA streams; ESA Space Science has five exact title and five exact link matches against the current corpus, with the remaining items adding distinct scientific-mission context. The overlapping ESA Human and Robotic Exploration stream was not retained; EASA Rulemaking Programmes was stale at 2017, and the tested Public Consultations path returned repeatable HTTP 404.
- The refreshed 392-feed live reports are the authority for current full-bundle payload, future-date and regression status; the five new feeds themselves passed transport, XML, date, title, link, duplication and freshness checks.

## Previous maintenance — ESA and EASA space, aviation safety and connectivity RSS expansion

- Added six notification-off, Master-only **European Space Agency** streams from the official [ESA RSS directory](https://www.esa.int/Services/RSS_Feeds): [Space News](https://www.esa.int/rssfeed/Our_Activities/Space_News), [Navigation](https://www.esa.int/rssfeed/Our_Activities/Navigation), [Observing the Earth](https://www.esa.int/rssfeed/Our_Activities/Observing_the_Earth), [Launchers](https://www.esa.int/rssfeed/Our_Activities/Launchers), [Space Engineering & Technology](https://www.esa.int/rssfeed/Our_Activities/Space_Engineering_Technology) and [Telecommunications & Integrated Applications](https://www.esa.int/rssfeed/Our_Activities/Telecommunications_Integrated_Applications). The live responses returned HTTP 200 RSS/XML with 84 dated items in total, unique titles and links per stream, and current windows through 7–18 August 2026. They add first-party navigation/PNT, Earth observation, launcher, space-technology and secure-connectivity context.
- Added six notification-off, Master-only **European Union Aviation Safety Agency** streams from the official [EASA RSS page](https://www.easa.europa.eu/en/rss): [News](https://www.easa.europa.eu/en/newsroom-and-events/news/feed.xml), [Press Releases](https://www.easa.europa.eu/en/newsroom-and-events/press-releases/feed.xml), [Notices of Proposed Amendment](https://www.easa.europa.eu/en/document-library/notices-of-proposed-amendment/feed.xml), [Opinions](https://www.easa.europa.eu/en/document-library/opinions/feed.xml), [Regulations](https://www.easa.europa.eu/en/document-library/regulations/feed.xml) and [Acceptable Means of Compliance & Guidance](https://www.easa.europa.eu/en/document-library/acceptable-means-of-compliance-and-guidance-material/feed.xml). Each returned HTTP 200 RSS/XML with 50 dated, unique items; the latest retained items range from 15 April to 17 August 2026, keeping the rulemaking streams inside the 180-day freshness window.
- The twelve additions contributed **304,030 body bytes / 72,006 wire bytes** to the Master refresh and passed the XML, date, title, link, freshness, duplicate and noise gates. Expected cross-posts are limited to ESA program cross-posting and the EASA News/Press relationship; EASA Research Reports was screened out because its newest item was from September 2024.
- The final live reports now show **385/385 Master**, **87/87 Air** and **80/80 Lite** successful HTTP/XML feed checks, with zero failed feeds and zero regression warnings. Master measured **47,453,610 body bytes / 27,287,859 wire bytes**; Air measured **4,052,554 / 1,951,102** and Lite **3,902,613 / 1,919,996**, with both device-budget checks passing. The shell wrappers still report nonzero because their historical consecutive-failure alert remains active, not because this run has a feed failure.

## Previous maintenance — UK and EU legislative RSS expansion

- Added **UK Parliament — Public Bills** from the official [UK Parliament RSS directory](https://www.parliament.uk/site-information/rss-feeds/) and direct [public-bills RSS feed](https://bills.parliament.uk/rss/publicbills.rss). The live response returned HTTP 200 RSS/XML with 50 dated items, 50 unique titles and links, all HTTPS item links, and a current window through 17 August 2026. It is included in iPhone Lite and inherited iPhone Air because it adds compact, first-party UK legislative-stage context to the phone layer.
- Added **UK Parliament — Private Bills** from the same official directory and direct [private-bills RSS feed](https://bills.parliament.uk/rss/privatebills.rss). The live response returned HTTP 200 RSS/XML with four dated, unique items through 16 July 2026. It remains Master-only because the stream is sparse and specialist.
- Added **European Parliament — Plenary Press Releases** from the official [European Parliament RSS catalogue](https://www.europarl.europa.eu/at-your-service/en/stay-informed/rss-feeds) and direct [plenary RSS feed](https://www.europarl.europa.eu/rss/doc/press-releases-plenary/en.xml). The live response returned HTTP 200 RSS/XML with 20 dated items, 20 unique links and 17 unique normalized titles through 9 July 2026. It has zero exact title/link overlap with the current committee feed and remains Master-only because it is event-driven and the Air payload is already close to its ceiling.
- All three additions are notification-off. The current full-refresh budgets leave both phone profiles inside their 4 MiB body-payload limits; the refreshed live validation report is the authority for exact measured bytes, latency advisories and any publisher exceptions.
- The clean-cache audit recorded **373/373 Master**, **87/87 Air** and **80/80 Lite** HTTP/XML responses. Air measured **4,052,672 body bytes / 1,950,913 wire bytes** with **141,632 bytes** of body headroom; Lite measured **3,902,715 / 1,906,912** with **291,589 bytes** of headroom. Both phone budgets passed, and the three new feeds had no transport, XML, title, date, link or duplication failure.
- The strict report remains marked unhealthy only because three pre-existing feeds published timestamps beyond the 90-minute future-date tolerance during this early-morning run: DNB General News, DNB Statistical News and Japan FSA All News. Master also records one non-critical Nasdaq Trade Halts item-count drift warning; neither condition is caused by the new UK/EU feeds.

## Latest maintenance — UN topic expansion

- Added four notification-off, Master-only UN News RSS streams: **Climate and Environment**, **Law and Crime Prevention**, **UN Affairs** and **Migrants and Refugees**. Each live endpoint returned HTTP 200 RSS/XML with 30 dated records, 30 unique titles, 30 unique HTTPS links and no internal duplicate-title or duplicate-link noise. The current windows run through 17, 18, 12 and 12 August 2026 respectively.
- Together the four feeds add **135,692 full-body bytes** and **135,692 wire bytes**. They add primary climate/physical-risk, illicit-finance and justice, AI/multilateral-governance, migration and humanitarian context to the Master collector without consuming Air/Lite payload or adding notification interrupts.
- The initial post-addition Master validation recorded four expected feed-added drift warnings for these new URLs; the fresh three-profile recheck now passes **370/370** with zero regression warnings and zero critical warnings, alongside no structural, freshness, metadata, duplicate-URL or noise failures.

## Latest maintenance — FDA safety and FEMA emergency response

- Added **FEMA — News Releases** from the official [FEMA data-sources directory](https://www.fema.gov/about/openfema/other-data-sources) and direct [national Press Releases feed](https://www.fema.gov/feeds/news.rss). The live Master response returned HTTP 200 RSS/XML with 10 dated, unique records through 18 August 2026, a 34,737-byte body and 8,328-byte wire response. It adds disaster-declaration, wildfire, resilience and emergency-response context without importing FEMA’s numeric declaration feeds or regional duplicates.
- Added six distinct **U.S. FDA** streams from the official [FDA RSS directory](https://www.fda.gov/about-fda/contact-fda/subscribe-podcasts-and-news-feeds): Food Safety Recalls (20 items, 18,331 bytes), MedWatch Safety Alerts (20, 17,204 bytes), Press Releases (20, 16,526 bytes), What’s New for Drugs (20, 12,053 bytes), What’s New for Vaccines, Blood & Biologics (20, 13,249 bytes) and Health Fraud Alerts (10, 7,038 bytes). The newest five were current through 18 August 2026; Health Fraud is a sparse event-driven feed with its newest retained alert on 7 April 2026. All six had unique titles and links.
- FDA article permalinks are currently legacy HTTP, so the validator records item-link transport warnings while accepting the verified HTTPS feed endpoints. The generic FDA Recalls and Food Allergies feeds were not added because they duplicate the selected Food Safety Recalls stream.
- All seven additions are notification-off and Master-only. Together they add **119,138 payload bytes** and **26,690 wire bytes** without changing the 86-feed Air or 79-feed Lite profiles. The FEMA WAF requires a neutral/default request identity; the validator records that exception alongside the existing official-feed identity exceptions.

## Latest maintenance — NASA space and cyber-news recovery

- Added five notification-off, Master-only NASA streams from the official [NASA RSS directory](https://www.nasa.gov/rss-feeds/): [News Releases](https://www.nasa.gov/news-release/feed/), [Technology](https://www.nasa.gov/technology/feed/), [Aeronautics](https://www.nasa.gov/aeronautics/feed/), [Space Station](https://www.nasa.gov/missions/station/feed/) and [Artemis](https://www.nasa.gov/missions/artemis/feed/). Each returned HTTP 200 RSS/XML with ten dated items, unique titles and links and complete HTTPS article links; the first three were current through 18 August 2026 and the latter two through 13 August 2026. Their measured bodies total **1,436,450 bytes** and their wire responses total **254,109 bytes**.
- NASA’s taxonomy feeds have limited expected cross-posting—one current News Releases item overlaps Technology and two overlap Aeronautics, while Artemis shares two items with Technology and one with Aeronautics—but each feed has a distinct operational scope. They add first-party space, technology-transfer, aviation-infrastructure, orbital-research and lunar-infrastructure context without changing the phone profiles.
- Replaced two currently unavailable commercial cyber feeds: **Dark Reading** returned HTTP 404 and **Krebs on Security** returned HTTP 403 across tested feed variants. Added **The Hacker News** from the official [The Hacker News site](https://thehackernews.com/) feed endpoint, which resolves to [FeedBurner RSS](https://feeds.feedburner.com/TheHackersNews); the live response contained 50 dated, unique records through 18 August 2026, with 59,356 payload bytes, 21,256 wire bytes and no link overlap against the cached corpus. It is included in both Air and Lite, preserving the phone counts.
- The net result of that prior maintenance was **366/86/79** with all five NASA feeds Master-only, The Hacker News in the phone layer, and no new notification interrupts. IMF, WHO, NOAA/NWS and NHC candidates were screened but not imported where endpoints were blocked, stale, future-dated or operationally noisy.

## Latest maintenance — nuclear regulation, public-health surveillance and physical risk

- Added **U.S. Nuclear Regulatory Commission — News Releases** from the official [NRC RSS page](https://www.nrc.gov/public-involve/rss-feeds) and direct [News Releases feed](https://www.nrc.gov/public-involve/rss?feed=news). The live Master response returned HTTP 200 RSS/XML with 166 dated items through 13 August 2026, 166 unique links, 165 unique normalized titles, a 53,253-byte body and 6,597-byte wire response. It adds primary U.S. nuclear-regulation, licensing, enforcement, safety and advanced-reactor signal distinct from IAEA nuclear-security coverage.
- Added **CDC — Morbidity and Mortality Weekly Report (MMWR)** from the official [CDC MMWR RSS page](https://www.cdc.gov/mmwr/rss/rss.html) and direct [MMWR feed](https://tools.cdc.gov/api/v2/resources/media/342778.rss). The live response returned HTTP 200 RSS/XML with 2,310 dated items through 13 August 2026, 2,310 unique links, a 1,927,778-byte body and 358,286-byte wire response. It is intentionally Master-only because it is a large research/surveillance archive; the hourly collector still limits its handoff to the bounded digest budget.
- Added **U.S. Geological Survey — Significant Earthquakes** from the official [USGS earthquake feed directory](https://earthquake.usgs.gov/earthquakes/feed/) and direct [significant-earthquake Atom feed](https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_week.atom). The live response returned five current dated and unique event records, 7,125 payload bytes and 1,366 wire bytes, adding compact physical-risk and infrastructure context without importing the much larger magnitude-2.5 stream.
- All three additions are notification-off and Master-only. The NRC and USGS streams are small; MMWR is flagged for payload review but remains well below the Master response limit. Air/Lite stay at 86/79 and their device budgets are unchanged.

## Latest maintenance — U.S. energy and public-health research context

- Added **U.S. Energy Information Administration — Today in Energy**, **Press Releases** and **What’s New** from the official [EIA RSS directory](https://www.eia.gov/tools/rssfeeds/) and direct [Today in Energy](https://www.eia.gov/rss/todayinenergy.xml), [Press Releases](https://www.eia.gov/rss/press_rss.xml) and [What’s New](https://www.eia.gov/about/new/WNtest3.php) endpoints. These provide distinct primary energy-market analysis, forecast and energy-data product-release signal alongside the retained European Commission energy and IAEA nuclear-security streams.
- Added **CDC Travelers' Health — Travel Notices** and **CDC — Emerging Infectious Diseases Ahead-of-Print** from the official [CDC RSS directory](https://wwwnc.cdc.gov/eid/rss) and direct [travel-notices](https://wwwnc.cdc.gov/travel/rss/notices.xml) and [ahead-of-print](https://wwwnc.cdc.gov/eid/rss/ahead-of-print.xml) feeds. They add U.S. global outbreak/travel-risk notices and technical emerging-infection research distinct from the retained ECDC threat and communicable-disease streams.
- All five additions are notification-off and Master-only, preserving the 86-feed Air and 79-feed Lite profiles and their device budgets. Their current manifest metadata and generated source-table entries are synchronized; the refreshed live validation report remains the authority for current response, freshness and overlap measurements.

## Latest maintenance — ECDC health threats and UK strategic/public infrastructure

- Added **ECDC — News** and **ECDC — Communicable Disease Threat Reports** from the official [ECDC RSS directory](https://www.ecdc.europa.eu/en/rss-feeds) and direct [news](https://www.ecdc.europa.eu/en/taxonomy/term/1307/feed) and [CDTR](https://www.ecdc.europa.eu/en/taxonomy/term/1505/feed) endpoints. Each passed three repeated live HTTP 200 RSS/XML requests with dated HTTPS-linked items, unique titles and links, and zero exact or conservative fuzzy-story overlap with the cached corpus. The feeds add outbreak, surveillance and weekly cross-border communicable-disease threat signal.
- Added **UK Home Office — Activity on GOV.UK**, **UK Ministry of Defence — Activity on GOV.UK** and **UK Department for Transport — Activity on GOV.UK** from the official [Home Office](https://www.gov.uk/government/organisations/home-office.atom), [Ministry of Defence](https://www.gov.uk/government/organisations/ministry-of-defence.atom) and [Department for Transport](https://www.gov.uk/government/organisations/department-for-transport.atom) Atom feeds. Each passed three repeated live HTTP 200 requests with 20 dated items, unique titles and links, all HTTPS item links and zero exact or conservative fuzzy-story overlap. They add UK internal-security and migration-policy, defence and strategic-resilience, and transport-infrastructure and vehicle-regulation context.
- All five are notification-off and Master-only. Their measured bodies total 54,714 bytes and do not change the 86-feed Air or 79-feed Lite profiles.

## Latest maintenance — U.S. defense and nuclear-security coverage

- Added **U.S. Department of Defense — News** from the official [defense RSS directory](https://www.defense.gov/news/rss) and direct [news feed](https://www.defense.gov/DesktopModules/ArticleCS/RSS.ashx?ContentType=1&Site=945&max=10). Three repeated live requests returned stable HTTP 200 RSS/XML responses with 10 dated items through 18 August 2026, a 10,041-byte body, 3,039-byte wire response, unique titles and links, complete HTTPS item links and no exact or conservative fuzzy-story overlap with the cached corpus. The endpoint redirects its article permalinks to the publisher's current `war.gov` domain and adds U.S. operational, force-posture, technology and strategic-security context.
- Added **U.S. Department of Defense — Releases** from the same official [RSS directory](https://www.defense.gov/news/rss) and direct [formal-release feed](https://www.defense.gov/DesktopModules/ArticleCS/RSS.ashx?ContentType=9&Site=945&max=10). Three repeated requests returned stable HTTP 200 RSS/XML responses with 10 dated items through 17 August 2026, a 9,573-byte body, 2,627-byte wire response, unique titles and links, complete HTTPS item links and no exact or conservative fuzzy-story overlap. It adds distinct formal policy, procurement, research-security and critical-defense-industrial-base signal.
- Added **IAEA — News** from the official [IAEA news page](https://www.iaea.org/news) and direct [news feed](https://www.iaea.org/feeds/news). Three repeated requests returned stable HTTP 200 RSS/XML responses with 150 dated items through 18 August 2026, a 122,561-byte body, 18,973-byte wire response, 141 unique normalized titles, 142 unique links, an 11.3% repeated-title rate and 10.0% repeated-link rate—both below the 50% noise threshold—and no exact or conservative fuzzy-story overlap. It adds primary nuclear safety, safeguards, nuclear-security, radiation, Ukraine nuclear-site and strategic-energy context. All 150 current article permalinks are legacy HTTP; the HTTPS feed endpoint is verified and the validator records this as a warning rather than a feed failure.
- All three are notification-off and Master-only. Together they add 142,175 bytes of full-feed payload and 24,639 wire bytes without changing the 86-feed Air or 79-feed Lite profiles or their device budgets.

## Latest maintenance — European aviation, space and border resilience

- Added **EASA — Cybersecurity News** from the official [EASA cybersecurity news page](https://www.easa.europa.eu/en/domain-types/cybersecurity-news) and direct [cybersecurity RSS feed](https://www.easa.europa.eu/en/taxonomy/term/11675/all/feed.xml). The live endpoint returned HTTP 200 RSS/XML with 32 dated items through 8 July 2026 in a 49,846-byte decompressed body; all titles and normalized links were unique, all item links were HTTPS, and the archive-heavy stream passed the event-driven freshness policy with a 365-day stale-review window. It adds aviation information security, GNSS interference, AI assurance and critical-aviation-systems context.
- Added **EU Agency for the Space Programme — News** from the official [EUSPA newsroom](https://www.euspa.europa.eu/newsroom-events/news) and direct [news RSS feed](https://www.euspa.europa.eu/newsroom-events/news/rss.xml). The live endpoint returned HTTP 200 RSS/XML with 10 dated items through 17 August 2026 in a 77,267-byte decompressed body, unique titles and links, complete HTTPS item links and no exact or conservative fuzzy-story overlap with the cached Master corpus. It adds Galileo, Copernicus, IRIS², GNSS authentication, space-security, infrastructure and strategic-resilience signal.
- Added **European Commission — Migration & Home Affairs News** from the official [DG HOME news page](https://home-affairs.ec.europa.eu/news_en) and direct [Migration & Home Affairs RSS feed](https://home-affairs.ec.europa.eu/node/2/rss_en). The live endpoint returned HTTP 200 RSS/XML with 30 dated items through 18 August 2026 in a 51,718-byte decompressed body, unique titles and links, complete HTTPS item links and no exact or conservative fuzzy-story overlap. It adds EU internal security, border management, organised crime, migration, Schengen, EES and resilience-funding context.
- Added **Frontex — News Releases** from the official [Frontex newsroom](https://frontex.europa.eu/media-centre/newsroom/news-release/) and direct [news-release feed](https://frontex.europa.eu/media-centre/news/news-release/feed). The live endpoint returned HTTP 200 Atom/XML with 20 dated items through 18 August 2026 in a 15,823-byte decompressed body, 19 unique normalized titles, 20 unique links, complete HTTPS item links and no exact or conservative fuzzy-story overlap. Its 5% repeated-title rate remains below the noise threshold and adds operational border, customs/cash-smuggling, maritime-surveillance and cross-border-crime signal distinct from the Commission policy stream.
- Each candidate passed three repeated validator-style requests with stable HTTP 200 responses, body hashes and measured payloads. All four are notification-off and Master-only; together they add 194,654 bytes without changing the 86-feed Air or 79-feed Lite profiles or their device budgets.

## Latest maintenance — European Commission energy, trade and research coverage

- Added **European Commission — Energy News** from the official [DG Energy news page](https://energy.ec.europa.eu/news_en) and its direct [Energy RSS feed](https://energy.ec.europa.eu/node/2/rss_en). The live candidate response returned HTTP 200 RSS/XML with 30 dated items through 14 August 2026 in a 39,987-byte body, all 30 HTTPS item links and unique titles and links. Two State-aid headlines and one article link also occur in the retained Competition Policy stream; the overlap is limited to those two cross-cutting Commission announcements, while the remaining items add distinct energy-security, electricity, renewables and transition context.
- Added **European Commission — Trade & Economic Security News** from the official [DG Trade news page](https://policy.trade.ec.europa.eu/news_en) and its direct [Trade RSS feed](https://policy.trade.ec.europa.eu/node/2/rss_en). The live candidate response returned HTTP 200 RSS/XML with 30 dated items through 13 August 2026 in a 41,409-byte body, all 30 HTTPS item links, unique titles and links, and zero exact, link or conservative fuzzy-story overlap with the cached Master corpus.
- Added **European Commission — Research & Innovation News** from the official [Research & Innovation news page](https://research-and-innovation.ec.europa.eu/news/all-research-and-innovation-news_en) and its direct [Research & Innovation RSS feed](https://research-and-innovation.ec.europa.eu/node/2/rss_en). The live candidate response returned HTTP 200 RSS/XML with 30 dated items through 18 August 2026 in a 39,343-byte body, all 30 HTTPS item links, unique titles and links, and zero exact, link or conservative fuzzy-story overlap with the cached Master corpus.
- All three feeds passed three repeated validator-style requests with stable HTTP 200 status, payload sizes and response hashes. They are notification-off and Master-only, adding 120,739 bytes of official EU energy, trade/economic-security, science, technology and innovation signal without changing the iPhone Air/Lite profiles or their device budgets.

## Latest maintenance — European transport, food-safety and patent intelligence

- Added **European Commission — Mobility & Transport News** from the official [Mobility & Transport news page](https://transport.ec.europa.eu/news-events/news_en) and its direct [RSS feed](https://transport.ec.europa.eu/node/2/rss_en). The live candidate response returned HTTP 200 RSS/XML with 30 dated items through 6 August 2026 in a 37,606-byte body, all 30 HTTPS item links and unique titles and links, with zero exact title, link or conservative fuzzy-story overlap with the cached Master corpus.
- Added **European Food Safety Authority — News** from the official [EFSA RSS directory](https://www.efsa.europa.eu/en/rss) and direct [News RSS feed](https://www.efsa.europa.eu/en/press/rss). It returned HTTP 200 RSS/XML with 10 dated items through 22 July 2026 in a 7,249-byte body, unique titles and links, all HTTPS item links and zero exact title, link or conservative fuzzy-story overlap.
- Added **European Food Safety Authority — Publications** from the same official RSS directory and direct [Publications RSS feed](https://www.efsa.europa.eu/en/publications/rss). It returned HTTP 200 RSS/XML with 20 dated items through 18 August 2026 in a 45,800-byte body, 20 unique links and a 5% repeated-title rate, below the noise threshold, with zero exact title, link or conservative fuzzy-story overlap.
- Added **European Patent Office — News** from the official [EPO RSS directory](https://www.epo.org/en/service-support/rss-feeds) and direct [News RSS feed](https://www.epo.org/en/news-events/news/feed). It returned HTTP 200 RSS/XML with 965 dated items through 18 August 2026 in a 527,319-byte archive-heavy body, 948 unique normalized titles, 965 unique links, a 1.8% repeated-title rate and zero exact title, link or conservative fuzzy-story overlap. The repeated checks kept the body hash stable even though transfer-size headers varied.
- All four feeds passed three repeated validator-style requests with stable HTTP 200 responses and are notification-off and Master-only. Together they add 617,974 bytes of transport-policy, logistics, food-safety, scientific-risk, patent and innovation context without changing the iPhone Air/Lite profiles or their device budgets.

## Latest maintenance — EUR-Lex legal and Official Journal coverage

- Added **EUR-Lex — Parliament & Council Legislation (English)** from the official [EUR-Lex predefined RSS alerts page](https://eur-lex.europa.eu/content/help/search/predefined-rss.html?locale=en) and direct [legislation feed](https://eur-lex.europa.eu/EN/display-feed.rss?rssId=162). The live HTTP 200 RSS/XML response contained 100 dated items through 18 August 2026 in a 65,673-byte body, with 100 HTTPS item links, zero internal duplicate titles or links and no exact title or link overlap with the cached corpus.
- Added **EUR-Lex — Official Journal C (English)** from the same official RSS catalogue and direct [Official Journal C feed](https://eur-lex.europa.eu/EN/display-feed.rss?rssId=221). It returned HTTP 200 RSS/XML with 100 dated information/notices items through 18 August 2026 in a 76,550-byte body, with 100 HTTPS item links, zero internal duplicate titles or links and no exact title or link overlap with the cached corpus. Its 2.01-second fetch is recorded as a Master refresh advisory, not a hard failure.
- Both feeds are notification-off and Master-only. They add adopted EU legislation, state-aid, competition, procurement, calls and institutional-notice signal distinct from the Commission, Council, Parliament, regulator and Ombudsman streams; their combined payload is roughly 142 KB and does not change the phone profiles.
- EUR-Lex’s case-law and Commission-proposal feeds were not imported because their current RSS items lack item-level dates. The Official Journal L feed was also left out after repeated validator-style requests intermittently timed out with zero bytes; it remains a recheck candidate rather than an unreliable dependency.

## Latest maintenance — European Environment Agency RSS coverage

- Added **European Environment Agency — Press Releases**, **Publications**, **Featured Articles** and **Maps & Charts** from the official [EEA RSS directory](https://www.eea.europa.eu/en/newsroom/rss-feeds), using the direct [press-release feed](https://www.eea.europa.eu/en/newsroom/rss-feeds/eeas-press-releases-rss/rss.xml), [publications feed](https://www.eea.europa.eu/en/newsroom/rss-feeds/publications-rss/rss.xml), [featured-articles feed](https://www.eea.europa.eu/en/newsroom/rss-feeds/featured-articles-rss/rss.xml) and [maps-and-charts feed](https://www.eea.europa.eu/en/newsroom/rss-feeds/maps-and-charts/rss.xml).
- The live candidate checks returned HTTP 200 RSS/XML with 25 dated items each: Press Releases through 1 July 2026 (30,521 bytes), Publications through 1 July 2026 (32,413 bytes), Featured Articles through 18 June 2026 (29,064 bytes) and Maps & Charts through 13 August 2026 (25,603 bytes). Every item had a unique title and HTTPS link; all four had zero exact title/link overlap with the cached corpus and zero conservative fuzzy-story overlap. Three repeated validator-style requests passed for each endpoint.
- All four feeds are notification-off and Master-only. Together they add 117,601 bytes of official EU environmental-policy, climate, energy, pollution, biodiversity, transition, publication and data-visualisation context without changing the iPhone Air/Lite profiles or their device budgets.

## Latest maintenance — European institutional-accountability coverage

- Added **European Ombudsman — News & Decisions (English)** from the official [European Ombudsman RSS page](https://www.ombudsman.europa.eu/rss) and direct [English RSS stream](https://www.ombudsman.europa.eu/rest/rss?lang=en&max=50). The live HTTP 200 `application/rss+xml` response contained 50 dated English-language items through 18 August 2026, a roughly 36 KB response, all 50 HTTPS item links, zero internal duplicate titles or links and no exact title or link overlap with the cached 321-feed corpus.
- It is notification-off and Master-only, adding official EU maladministration, access-to-documents, procurement, transparency and institutional-accountability signal distinct from OLAF, EPPO, Eurojust and Commission feeds. It adds no phone payload or notification cost.
- The final profiles are **322 Master / 86 Air / 79 Lite**; all three live device-budget checks pass.

## Latest maintenance — Italian CSIRT and Swedish supervisory coverage

- Added **ACN / CSIRT Italia — Security Updates (Italian)** from the official [ACN / CSIRT Italia RSS endpoint](https://www.acn.gov.it/portale/feedrss/-/journal/rss/20119/723192). The live HTTP 200 response was RSS/XML with 50 dated items through 18 August 2026, a roughly 35.6 KB decompressed body, all 50 HTTPS item links, a 4% repeated-title rate and no exact title or link overlap with the cached Master corpus. It is included in iPhone Air, notification-off, for Italian national-CSIRT and EU operational security signal.
- Added **Finansinspektionen — News (English)** from the official [Finansinspektionen RSS instructions](https://www.fi.se/en/subscribe/?category=17&category=80&email=) and direct [English news feed](https://www.fi.se/en/published/news/rss). The live HTTP 200 response was RSS/XML with nine dated items through 7 July 2026 in a roughly 6.7 KB body, complete HTTPS links and no exact title or link overlap with the cached corpus. Its episodic cadence makes it a useful notification-off, Master-only source for Swedish financial-supervision developments.
- To keep the phone payload bounded, **Bloomberg — Markets** was restored to Air while **CrowdStrike — Cybersecurity Research**, **European Environment Agency — Indicators** and **HKMA — Publications** moved to Master-only. The final profiles are **322 Master / 86 Air / 79 Lite**; all three live device-budget checks pass.

## Latest maintenance — BaFin and Swiss NCSC coverage

- Added **BaFin — Supervisory Measures (German)** and **BaFin — Circulars (German)** from the official [BaFin RSS directory](https://www.bafin.de/DE/service/rss/rss_node.html). Their direct [measures feed](https://www.bafin.de/DE/service/rss/_function/RSS_Massnahmen.xml?nn=150166) and [circulars feed](https://www.bafin.de/DE/service/rss/_function/RSS_Rundschreiben.xml?nn=150166) returned HTTP 200 RSS/XML with 20 dated items each; body sizes were 14,510 and 9,570 bytes, with complete item links and no noise-gate failure.
- Added **Swiss NCSC — Press Releases (German)** from the official [NCSC RSS page](https://www.ncsc.admin.ch/ncsc/en/home/dokumentation/medienmitteilungen/rss.html) and direct [German-language RSS stream](https://d-nsbc-p.admin.ch/NSBSubscriber/feeds/rss?lang=de&org-nr=1101&topic=&kind=M). It returned HTTP 200 RSS/XML with 124 dated items through 25 June 2026 in a 96,234-byte body, 123 unique titles and 124 unique links; the translated French and Italian streams were not duplicated.
- All three feeds are notification-off and Master-only. They raise the manifest to **319 feeds (240 Finance / 79 Cyber Security)** while Air/Lite remain **88/80**. The shell validator also now preserves colon-containing `Last-Modified` values when building conditional refresh requests, avoiding malformed revalidation headers.

## Latest maintenance — UK economic-crime and fraud-prevention RSS coverage

- Added **National Crime Agency — News** from the official [NCA organisation page](https://www.gov.uk/government/organisations/national-crime-agency) and direct [news-and-communications Atom feed](https://www.gov.uk/search/news-and-communications.atom?organisations%5B%5D=national-crime-agency). The live HTTP 200 response contained 20 dated items through 19 May 2026 in a 12,667-byte body, with unique titles and HTTPS links; it adds UK economic-crime, cybercrime, sanctions-enforcement and serious-organised-crime intelligence.
- Added **Public Sector Fraud Authority — Activity on GOV.UK** from the official [PSFA organisation page](https://www.gov.uk/government/organisations/public-sector-fraud-authority) and direct [Atom feed](https://www.gov.uk/government/organisations/public-sector-fraud-authority.atom). The live HTTP 200 response contained 20 dated items through 11 August 2026 in a 13,486-byte body, with unique titles and HTTPS links; it adds fraud-prevention, data-matching, civil-penalty and public-sector economic-crime policy activity.
- Both feeds are notification-off and Master-only. They raise the manifest to **316 feeds (238 Finance / 78 Cyber Security)** while Air/Lite remain **88/80**, adding no phone payload or notification cost.

## Latest maintenance — Guernsey financial-regulatory RSS coverage

- Added **Guernsey Financial Services Commission — Financial Crime News** and **Guernsey Financial Services Commission — Sanctions** from the official [GFSC RSS directory](https://www.gfsc.gg/rss-feeds), using the direct [financial-crime feed](https://www.gfsc.gg/article.xml?tid=55) and [sanctions feed](https://www.gfsc.gg/article.xml?tid=56).
- The live HTTP 200 `text/xml` responses contained ten dated items each: the financial-crime feed measured 204,267 bytes through 30 July 2026 with unique titles and links; the sanctions feed measured 68,554 bytes through 18 August 2026 with ten unique links. The sanctions stream repeats generic notice titles for distinct sanctions events, so the manifest records an explicit `structured-alert` policy rather than treating those notices as editorial duplication.
- Both feeds are notification-off and Master-only. They raise the master set to **314 feeds (236 Finance / 78 Cyber Security)** while Air/Lite remain **88/80**, adding no phone payload or notification cost.

## Latest maintenance — RBA daily exchange-rate context

- Added **Reserve Bank of Australia — Daily Exchange Rates** from the [official RBA RSS directory](https://www.rba.gov.au/updates/rss-feeds.html) and direct [RSS 1.0/XML feed](https://www.rba.gov.au/rss/rss-cb-exchange-rates.xml). The live endpoint returned HTTP 200 `text/xml` with 21 dated currency records for 18 August 2026 in a 40,620-byte body; all records had unique titles and HTTPS links with currency-specific fragments.
- The feed is notification-off and Master-only. It adds current AUD cross-rate and Asia-Pacific market-data context alongside the existing official exchange-rate series. Because the 21 currency records point to one RBA rate-table page, the manifest records an explicit `structured-alert` item-link policy so the shared table URL is not mistaken for editorial story noise.
- The addition leaves Air/Lite at **88/80** and raises the manifest to **312 feeds (234 Finance / 78 Cyber Security)**. The existing narrow anonymous/default RBA identity exception covers this endpoint; no broad validator or collector relaxation was introduced.
- ASIC’s official Inside ASIC podcast RSS was screened but not retained because its 14-item window was last updated 8 July 2025. AUSTRAC’s official subscription page says its media-release RSS will be removed, and the Protective Security Policy Framework RSS endpoint timed out under the local validator-compatible transport; all three remain recheck candidates rather than active subscriptions.

## Latest maintenance — CFPB consumer-finance regulatory coverage

- Added **CFPB — Newsroom** from the [official CFPB newsroom](https://www.consumerfinance.gov/about-us/newsroom/) and direct [RSS feed](https://www.consumerfinance.gov/about-us/newsroom/feed/). The live endpoint returned HTTP 200 RSS/XML with 21 dated items through 14 August 2026 in a 14,985-byte body; titles and links were unique, all item links were HTTPS, and the feed passed the freshness and noise gates.
- The feed adds official US consumer-finance regulation, complaints, supervision, enforcement, financial-data and financial-literacy context distinct from the retained FTC, CFTC and SEC streams. It is included in iPhone-lite and inherited by iPhone Air, notification-off for Apple Intelligence digest review.
- The CFPB WAF returns HTTP 403 to descriptive browser/collector identities but serves the same public RSS with the neutral `curl/8.0` identity. The validator and hourly collector use that identity only for this exact endpoint, with a regression test protecting the exception. The addition brought the manifest to **311 feeds (233 Finance / 78 Cyber Security)** before the RBA daily exchange-rate addition; the phone profiles remain **88 Air / 80 Lite**.

## Latest maintenance — Dutch central-bank RSS coverage

- Added five streams listed in the [official DNB RSS directory](https://www.dnb.nl/en/rss/): [General News](https://www.dnb.nl/en/rss/16451/6882), [Supervision News](https://www.dnb.nl/en/rss/16453/6892), [Statistical News](https://www.dnb.nl/en/rss/16452/6893), [Publications](https://www.dnb.nl/en/rss/13039/4612) and [Research Publications](https://www.dnb.nl/en/rss/16455/4614). Each live endpoint returned HTTP 200 `text/xml` RSS with dated items, complete HTTPS item links and no duplicate-link or noise-gate failure.
- Supervision News, Statistical News and Publications are included in both iPhone profiles; General News and Research Publications remain Master-only because their archive bodies are larger, while the full five-feed addition remains well inside the declared mobile payload ceilings. All five are notification-off and intended for digest review.
- DNB’s WAF rejects descriptive user-agent strings, so the validator and hourly collector use a neutral `curl/8.0` identity for these exact official endpoints. The endpoint-specific behavior is covered by a regression test; normal feed identity handling remains unchanged.

## Latest maintenance — EIOPA insurance market-risk data

- Added **EIOPA — Symmetric Adjustment Equity Capital Charge** from the [official EIOPA technical-data page](https://www.eiopa.europa.eu/tools-and-data/symmetric-adjustment-equity-capital-charge_en) and direct [RSS feed](https://www.eiopa.europa.eu/feed/68/rss_en). The live endpoint returned HTTP 200 RSS/XML with 137 dated monthly releases through 5 August 2026 in a 60,049-byte body; every item link is HTTPS and titles/links are unique.
- The feed is notification-off and Master-only because it is specialist Solvency II market-risk data rather than a compact phone-news stream. Air/Lite remain **84/76**, while the master set becomes **305 feeds (227 Finance / 78 Cyber Security)**.

## Latest maintenance — OSFI and RSS endpoint recovery

- Added **OSFI — News** from the [official OSFI news page](https://www.osfi-bsif.gc.ca/en/news) and direct `https://www.osfi-bsif.gc.ca/en/rss.xml`. The live endpoint returned HTTP 200 RSS/XML with ten dated items, unique titles and HTTPS links; it is notification-off and Master-only, raising the current bundle at that checkpoint to **304 feeds (226 Finance / 78 Cyber Security)** while Air/Lite remained **84/76**.
- OSFI emits harmless Drupal comments before the XML declaration. The shared safe parser now accepts only whitespace/comment/processing-instruction preambles and has a regression test; unexpected bytes remain rejected.
- At that earlier checkpoint, the [official SANS RSS directory](https://isc.sans.edu/xml.html) showed title-only `https://isc.sans.edu/rssfeed.xml` returning an HTML page despite a `text/xml` label, while official full-text `https://isc.sans.edu/rssfeed_full.xml` passed. A later maintenance repair rechecked the publisher and moved the manifest to the current compact RSS endpoint; see the latest parliamentary-research entry above.
- Nasdaq Equity Trader Alerts remains a valid current feed, but one item is stamped about four hours ahead of the publisher’s current HTTP `Date`/`Last-Modified` headers. A documented 360-minute feed-specific tolerance keeps this source under review while the global 90-minute future-date gate remains unchanged for every other feed.

## Latest expansion — European and Asian regulator and national-CSIRT depth

- Added **Finanstilsynet — News (Norwegian)** and **Finanstilsynet — Circulars (Norwegian)** from the [official Finanstilsynet RSS directory](https://www.finanstilsynet.no/RSS/). The live screens returned HTTP 200 Atom/XML with 20 current dated items each; the circulars feed had 18 unique titles out of 20 and remained below the repository’s 50% noise gate.
- Added **Japan Financial Services Agency — All News (Japanese)** from the [official FSA RSS directory](https://www.fsa.go.jp/kouhou/rss.html), **CSSF — All Publications** and **CSSF — Cybersecurity Publications** from the [official CSSF RSS directory](https://www.cssf.lu/en/rss-feed/), **FMA Austria — All News** from the [official FMA RSS directory](https://www.fma.gv.at/en/rss-newsfeed/), **FSMA Belgium — News & Warnings** from the [FSMA news page](https://www.fsma.be/en/news-articles), and **NCSC-FI — Vulnerabilities** from the [official NCSC-FI RSS directory](https://kyberturvallisuuskeskus.fi/en/ncsc-news/rss-feeds). Each passed the direct HTTPS endpoint, parseable XML, dated-item, title/link and freshness gates in the focused audit; FSMA’s 28/30 unique-title result and CSSF’s filtered cybersecurity stream remained within the configured noise limits.
- At that prior expansion checkpoint, all eight feeds were notification-off and Master-only, raising the manifest to **303 feeds (225 Finance / 78 Cyber Security)** while Air/Lite remained **84/76**. Europol, Bank of Greece, CNMV, FATF, ENISA and ASIC candidates were screened but not imported when their direct endpoints lacked dates, returned access denial, reused links too heavily or were not available as direct RSS.
- The former **ifo Institute — News & Research** endpoint (`https://www.ifo.de/rss.xml`) was removed from the configured bundle after it redirected to a publisher WAF HTML page instead of parseable RSS/XML; the current [official ifo press page](https://www.ifo.de/presse) no longer advertises an RSS replacement. It remains a recheck candidate rather than an active subscription; the eight feeds above were the prior expansion checkpoint.

## Latest expansion — ECB general publications

- Added **European Central Bank — Publications** from the [official ECB RSS directory](https://www.ecb.europa.eu/home/html/rss.en.html). The live HTTP 200 RSS/XML response contained 15 dated items through 12 August 2026, with 15 unique titles and links. It adds official Eurosystem monetary-policy implementation, macro-financial, digital-euro and euro-area policy publications distinct from the retained ECB blog, working-paper and research-bulletin streams.
- The feed is notification-off and Master-only. The manifest is now 289 feeds (213 Finance / 76 Cyber Security), while Air/Lite remain 84/76.
- The official [Google Online Security Blog feed](https://security.googleblog.com/feeds/posts/default?alt=rss) was rechecked but rejected because its effective URL redirects to the HTTP FeedBurner endpoint; Android’s directly tested security-bulletin RSS path returned 404.

## Latest expansion — UK trade sanctions and strategic export controls

- Added **Office of Trade Sanctions Implementation — Updates** from the [official OTSI organisation page](https://www.gov.uk/government/organisations/office-of-trade-sanctions-implementation) and its [Atom feed](https://www.gov.uk/government/organisations/office-of-trade-sanctions-implementation.atom). The live HTTP 200 Atom/XML response contained 20 dated items through 3 August 2026 in a 12.0 KB body, with unique titles and complete HTTPS links. It adds UK trade-sanctions licensing, compliance, circumvention and civil-enforcement context beside OFSI’s financial-sanctions stream.
- Added **Export Control Joint Unit — Updates** from the [official ECJU organisation page](https://www.gov.uk/government/organisations/export-control-joint-unit) and its [Atom feed](https://www.gov.uk/government/organisations/export-control-joint-unit.atom). The live HTTP 200 Atom/XML response contained 20 dated items through 17 August 2026 in a 12.6 KB body, with unique titles and complete HTTPS links. It adds strategic export-control, military/dual-use licensing, notices-to-exporters and enforcement context.
- Both feeds are notification-off and Master-only. The manifest is now 291 feeds (215 Finance / 76 Cyber Security), while Air/Lite remain 84/76. The broad FCDO activity feed was screened but not retained because its current window is dominated by travel and consular guidance rather than focused intelligence.

## Latest expansion — HKMA depth streams

- Added five notification-off feeds from the [official HKMA RSS directory](https://www.hkma.gov.hk/eng/other-information/rss/): **Consultations**, **Supervisory Policy Manual**, **Publications**, **Research** and **inSight**. Their live screens returned 45, 43, 7, 14 and 15 dated items respectively, all with current HTTPS endpoints and valid HTTPS item links; the research stream’s two repeated annual-index links remain below the noise gate. Compact **Publications** and **inSight** are included in Air; the larger or more episodic **Consultations**, **Supervisory Policy Manual** and **Research** streams remain Master-only.
- They add Hong Kong banking-supervision consultations, prudential-policy updates, official publications, macro-financial research and policy analysis distinct from the retained Circulars, Daily Monetary Statistics and Speeches streams. The manifest is now 296 feeds (220 Finance / 76 Cyber Security), while Air/Lite remain 84/76.
- HKMA’s broad Press Releases stream was not retained because its duplicate-title rate exceeds the repository’s 50% noise threshold; Guidelines is archive-heavy and Regtech Knowledge Hub is stale.

## Latest expansion — Indian securities-regulator coverage

- Added **SEBI — Press Releases, Circulars & Orders** from the [official SEBI RSS directory](https://www.sebi.gov.in/rss.html). Its live HTTP 200 RSS/XML response contained 30 dated items through 18 August 2026 in a 22.1 KB body, with 30 unique titles, 30 unique HTTPS links and no internal duplicate signal. It adds Indian securities-market enforcement, circulars, investor warnings and market-policy context distinct from the retained Reserve Bank of India banking and monetary streams.
- SEBI’s item dates use the explicit publisher form `18 Aug, 2026 +0530`; the shared parser now accepts that narrow format and normalizes it under the manifest’s `Asia/Kolkata` metadata. The feed is notification-off and Master-only because its enforcement/recovery cadence is useful for research but too noisy for the default phone layer.
- At that stage, the addition raised the manifest to 286 feeds (210 Finance / 76 Cyber Security) while Air/Lite remained 84/76.

## Latest expansion — US national-security enforcement

- Added **DOJ National Security Division — News** from the [official NSD news page](https://www.justice.gov/nsd/nsd-news) and its direct [RSS endpoint](https://www.justice.gov/news/rss?type%5B0%5D=press_release&type%5B1%5D=speech&type%5B2%5D=youtube_video&field_topic%5B0%5D=25321&field_topic%5B1%5D=44971&field_topic%5B2%5D=44956&field_topic%5B3%5D=7881&field_topic%5B4%5D=44951&field_topic%5B5%5D=45186&field_component=361&search_api_language=en&show_public_archived=0&require_all=0). The live HTTP 200 RSS/XML response contained 25 dated items through 10 August 2026, with unique titles and HTTPS item links. It adds official US sanctions, terrorism-finance, export-control, counterintelligence and national-security enforcement context distinct from DOJ Antitrust.
- The feed is notification-off and Master-only. At that stage, the manifest reached 287 feeds (211 Finance / 76 Cyber Security), while Air/Lite remained 84/76.
- The official [SEC Litigation Releases page](https://www.sec.gov/enforcement-litigation/litigation-releases) exposes a direct RSS URL, but the current response contains an unescaped ampersand in an item title and fails XML parsing. It was rejected pending a publisher-side repair; the existing SEC Press Releases feed remains included.

## Latest expansion — Federal Reserve other announcements

- Added **Federal Reserve — Other Announcements** from the [official Federal Reserve RSS directory](https://www.federalreserve.gov/feeds/feeds.htm). The live HTTP 200 RSS/XML response contained 15 dated items through 1 July 2026 with unique titles and links; it fills the Board’s other-announcements gap for payments, leadership and system-policy developments.
- The addition is notification-off and Master-only. The manifest is now 288 feeds (212 Finance / 76 Cyber Security), while Air/Lite remain 84/76.
- The official **Federal Reserve — Testimony** feed was rechecked but rejected after the validator measured 66.7% repeated titles, above the 50% noise gate, despite unique item links.

## Latest expansion — Estonian and French national cyber coverage

- Added **Estonian RIA — Cybersecurity News (Estonian)** from the [official RIA RSS directory](https://www.ria.ee/ria-rss-vood). Its live HTTP 200 RSS/XML response contained 312 dated items through 3 July 2026 in a 198.9 KB body, with unique titles and HTTPS item links. It adds national cyber-policy, resilience, incident and threat context beyond the existing English-language national-CSIRT layer.
- Added **ANSSI — Cyber Threat Overviews (English)** from the [official ANSSI publication page](https://cyber.gouv.fr/en/publications/cyber-threat-overviews/). Its live HTTP 200 RSS/XML response contained five dated items through 19 May 2026 in a 2.7 KB body with unique titles. The feed emits legacy HTTP item URLs that redirect to HTTPS ANSSI pages; the validator records that expected item-link transport warning while confirming the article pages return HTTP 200.
- Both feeds are notification-off and Master-only: the Estonian-language archive and the episodic English threat-overview stream add research value without changing the 84-feed Air or 76-feed Lite profiles. The manifest is now 285 feeds (209 Finance / 76 Cyber Security).

## Latest expansion — Reserve Bank of Australia official coverage

- Added six **Master-only**, notification-off Finance feeds from the [official RBA RSS directory](https://www.rba.gov.au/updates/rss-feeds.html): **Media Releases**, **Speeches**, **Bulletin**, **Financial Stability Review**, **Statements on Monetary Policy** and **Research Discussion Papers**.
- The live candidate screen returned valid RSS 1.0/XML for all six through the RBA’s anonymous/default HTTPS identity: one dated item per stream, latest dates from 19 March to 14 August 2026, bodies from 2.4–5.1 KB, complete HTTPS item links, zero internal duplicate titles or links and HTTP 200 article pages. Their event-driven cadence and tiny bodies make them useful Master research sources without expanding the phone profiles.
- The RBA WAF rejects the repository’s generic validation user-agent but accepts the anonymous/default curl identity. The validator now scopes that exception to `www.rba.gov.au/rss/*`; no general transport gate was weakened. The additions raise the manifest to 285 feeds (209 Finance / 76 Cyber Security) while Air/Lite remain 84/76.

## Latest expansion — BIS management speeches

- Added **BIS — Management Speeches** as a notification-off, Master-only Finance stream from the [official BIS RSS directory](https://www.bis.org/rss/index.htm).
- The live screen returned HTTP 200 RSS 1.0/XML with 25 dated items through 2 July 2026 in a 33.1 KB body, 25 unique titles, 25 unique HTTPS links and no internal duplicate signal. It adds BIS leadership and global financial-system policy context distinct from the existing BIS central-bank-speech aggregator.
- The official BIS Central Bank Research Hub was rechecked but rejected for a materially future-dated item; the Portuguese CNCS feed was stale (latest June 2019), and the Slovak SK-CERT RSS link was not parseable. The new BIS stream leaves Air/Lite unchanged at 84/76.

## Latest expansion — German economic institutes and official environment policy

- Added seven **Master-only**, notification-off Finance feeds after a live HTTP/XML, freshness, link and overlap audit: **ifo Institute — News & Research**; **German Council of Economic Experts — RSS**; **DIW Berlin — News & Press Releases**; **DIW Berlin — Publications**; **DIW Berlin — SOEP News (English)**; **RWI Essen — Unstatistiken**; and **BMUKN — All News**.
- The ifo feed returned 50 items through 18 August 2026 in a 45.3 KB body; the German Council of Economic Experts returned 30 dated items through 28 July in a 46.9 KB body. Both had unique titles and links and no prior cached-corpus overlap.
- DIW News and Publications returned 20 and 35 items through 13 and 14 August in 21.9 KB and 35.8 KB bodies. DIW SOEP News returned 20 English-language items through 15 July in a 16.3 KB body with a 40% repeated-title rate below the 50% noise gate. All three had complete item links and no prior cached-corpus link overlap.
- RWI Unstatistiken returned 176 dated items through 30 July in a 1.19 MiB body with 176 unique links and a 1.1% repeated-title rate; it remains Master-only because the archive is payload-heavy. BMUKN All News returned 20 items through 18 August in a 17.3 KB body with unique titles and links.
- The additions raise the current manifest to 275 feeds (201 Finance / 74 Cyber Security) while the generated iPhone Air and Lite profiles remain 84 and 76 feeds; all seven are notification-off and excluded from the phone profiles, alongside the two new Master-only national-CERT feeds.

## Latest expansion — European national cyber authority coverage

- Added nine official, notification-off Cyber feeds after live endpoint and XML/item-integrity checks: **Centre for Cybersecurity Belgium — Advisories** and **News**; **Romania DNSC — Cybersecurity News & Alerts**; **CERT.LV — News & Cybersecurity Updates**; **SI-CERT — Vulnerability & Cybersecurity News**; **Norway NCSC — Vulnerability Alerts**; **INCIBE-CERT — Security Advisories**; **INCIBE — Enterprise Security Advisories**; and **INCIBE — Citizen Fraud & Impersonation Warnings**.
- All nine returned HTTP 200 and parseable RSS/XML with valid dates and HTTPS article links. CCB Advisories returned 10 current items in a 6.8 KB body and is included in Air/Lite; the other eight remain Master-only because they are language-specific, episodic or specialist-focused. The three INCIBE streams are distinct technical, enterprise and citizen-fraud channels rather than duplicate translations.
- The additions expand national-CSIRT coverage across Belgium, Romania, Latvia, Slovenia, Norway, Spain, Czechia and Croatia while keeping the four existing interrupting notification feeds unchanged. They bring the Cyber section to 74 feeds and the complete bundle to 275 feeds; the current Air/Lite payload audits remain within budget.

## Latest expansion — Czech and Croatian national cyber coverage

- Added two official, notification-off, Master-only Cyber feeds after a live endpoint and XML/item-integrity screen: **NÚKIB — News (Czech)** and **CERT.hr — News (Croatian)**.
- NÚKIB returned HTTP 200 RSS/XML with 15 dated items through 13 August 2026 in a 17.3 KB body; CERT.hr returned HTTP 200 RSS/XML with 10 dated items through 14 August in a 63.9 KB body. Both had unique titles, HTTPS article links and a clear national-CERT signal.
- The [NÚKIB media page](https://nukib.gov.cz/cs/kontakty/pro-media/) publishes the Czech RSS endpoint, and the [CERT.hr site](https://www.cert.hr/) provides the Croatian national-CERT news stream. The two additions bring the manifest to 275 feeds / 74 Cyber Security sources while leaving the 84-feed Air and 76-feed Lite profiles unchanged.

## Latest expansion — OECD global macro-policy research

- Added **OECD Ecoscope — Economics Department Blog** (`https://oecdecoscope.blog/feed/`) as a Master-only, notification-off research stream. The [Ecoscope about page](https://oecdecoscope.blog/about/) describes OECD economists writing on current economic issues; it adds cross-country fiscal, growth, productivity, climate and structural-policy analysis.
- The live candidate screen returned HTTP 200 RSS/XML, 10 dated items through 28 July 2026, a 124.7 KB body, complete HTTPS item links, 10 unique titles and links, and zero exact or conservative fuzzy overlap with the cached corpus. The OECD’s [economic-policy page](https://www.oecd.org/en/topics/policy-issues/economic-policy.html) links to Ecoscope as a related OECD analysis stream.
- The Master profile rises to 253 feeds (190 Finance / 63 Cyber Security); iPhone Air and Lite remain at 83 and 75, preserving their payload budgets and notification surface.

## Latest expansion — Deutsche Bundesbank official central-bank coverage

- Added four **Master-only**, notification-off feeds from the [official Deutsche Bundesbank RSS directory](https://www.bundesbank.de/en/homepage/rss/deutsche-bundesbank-s-rss-feed-620440): **Discussion Papers**, **Latest Announcements**, **Speeches, Interviews & Contributions** and **Topics**.
- The live candidate audit returned HTTP 200 RSS/XML for all four: 10 discussion papers through 18 August 2026 (8.5 KB), 10 market/operations announcements through 18 August (7.8 KB), three speeches/interviews through 8 August (2.5 KB), and 10 topic items through 30 July (9.3 KB). All item titles, dates and links were valid; the feeds had unique links and no cached-corpus overlap, with Latest’s repeated-title rate at 10%.
- The four feeds add distinct German central-bank research, auction/operations, policy-commentary and financial-stability context without changing the 83-feed Air or 75-feed Lite profiles. The speeches stream is German-language despite its English directory path, so all four remain Master-only.
- The iPhone Air profile remains the recommended daily setup, with a 4 MB full-body budget, six mobile-review slots and four interrupting notifications. It inherits the Lite core and adds the Office for Budget Responsibility’s independent UK fiscal analysis, European Investment Bank news, EPPO financial-crime enforcement, EMA medicines-regulatory news, European Environment Agency indicator updates, Council of the EU sanctions and foreign-policy decisions, European Parliament committee decisions, European Commission competition, tax/customs and financial-services news, HMRC tax/customs activity, UK complex financial-crime and insolvency activity, Australian Treasury policy, Canadian and Indian central-bank context, Japan FSA English regulation, WTO global-trade policy news, UN economic-development, health, human-rights, peace-and-security and supply-chain context, FTC consumer-protection and competition releases, UK CMA competition-policy activity, DOJ Antitrust press releases, compact market, Ireland/EU/global data, OCC banking supervision, UK conduct, New Zealand national-cyber context and supply-chain/threat-intelligence coverage. The broad BBC Business feed, Bank of England Publications and FBI Cyber Podcast remain Master-only after the phone-layer rebalances.

## Latest expansion — German BSI, CEPR and Tax Foundation research

- Added five **Master-only** feeds after a live HTTP/XML and overlap audit: **BSI — Press, Short Communications & Events**; **BSI/CERT-Bund — IT Security Advisories**; **CEPR — VoxEU Research & Policy Analysis**; **CEPR — Discussion Papers**; and **Tax Foundation — Research & Commentary**. All are notification-off; iPhone Air and iPhone-lite remain at 83 and 75 feeds.
- BSI’s official RSS directory supplied two current German-language feeds: 40 press/policy/event items in a 31.7 KB body and 50 IT security advisories in a 21.1 KB body. Both were HTTP 200 XML with complete HTTPS links and zero internal title/link duplicates.
- CEPR’s current RSS directory supplied 50 dated VoxEU items in a 64.3 KB body and 50 Discussion Paper items in a 78.4 KB body, both current through 17 August 2026 with complete HTTPS links. The VoxEU stream had one exact cached title match but no link match or conservative duplicate-story cluster; Discussion Papers had no exact cached overlap.
- Tax Foundation returned 20 dated items through 14 August 2026 in a 20.2 KB RSS/XML body with complete HTTPS links and zero exact cached title/link overlap. These additions improve German national-CSIRT, independent macro/finance and tax-policy research without increasing mobile payloads or notification surface.

## Latest expansion — public-finance oversight and independent macro research

- Added seven **Master-only** Finance feeds after a live candidate pass: **UK National Audit Office — News**; **US GAO — Budget & Spending Reports**; **US GAO — Financial Markets & Institutions Reports**; **US GAO — Tax Policy & Administration Reports**; **US Congressional Budget Office — Publications**; **NIESR — News & Analysis**; and **Resolution Foundation — Research & Commentary**. The phone profiles remain 83 Air / 75 Lite, with all seven routed to the high-coverage collector and notification-off.
- The NAO Atom feed returned HTTP 200, 11 dated items through 2 July 2026, a 33.6 KB body, complete HTTPS item links and zero internal duplicate titles or links. Three consecutive fetches returned the same ETag, body size and item set; the official NAO describes itself as the UK’s independent public-spending watchdog.
- The three GAO topic feeds returned HTTP 200 RSS/XML with 30 dated items each: Budget & Spending through 31 July 2026 (128.2 KB), Financial Markets & Institutions through 23 July 2026 (103.9 KB) and Tax Policy & Administration through 10 August 2026 (110.3 KB). All item titles, dates and links were valid; the Financial Markets stream’s 26.7% repeated-title rate and the Tax stream’s 13.3% rate remain below the 50% noise gate.
- The CBO all-publications feed returned HTTP 200 RSS/XML with 30 dated items through 17 August 2026 and a 17.4 KB body. NIESR returned 10 dated items through 10 August 2026 with a 95.7 KB body; its approximately 5.9-second fetch is recorded as a Master-only slow-refresh advisory. Resolution Foundation returned 10 dated items through 14 August 2026 with a 112.2 KB body. All seven candidates had zero exact title/link overlap with the cached 240-feed corpus and no invalid item links.
- The additions fill the public-finance accountability, federal budget-analysis and independent UK macro-policy gaps without inflating the mobile profiles. The Irish Fiscal Advisory Council and ESRI endpoints were left out because their RSS archives were stale despite current websites; IFS remained blocked by HTTP 403, Bruegel’s current feed was dominated by event/session entries, and the CEPR root feed was stale.

## Latest expansion — UK independent fiscal analysis

- Added **Office for Budget Responsibility — News** (`https://obr.uk/feed/`) to Finance / Core / Official & Macro and to iPhone-lite/Air. The [official OBR site](https://obr.uk/) provides the source context; the feed adds independent UK fiscal forecasts, borrowing, fiscal-risk and public-finance releases alongside HM Treasury and Bank of England coverage.
- The direct feed passed the candidate screen with HTTP 200 RSS/XML, 10 dated items through 31 July 2026, a 32.5 KB body, complete HTTPS item links and no exact-title or exact-link overlap with the retained phone corpora. It remains notification-off for digest review.
- To keep the declared phone profiles bounded, Bank of England — Publications is retained in Master only; Japan FSA English News remains in both phone profiles. The resulting profile counts are 240 Master / 82 Air / 74 Lite.
- The high-value additions in this pass span EU securities and banking supervision, global financial stability, Federal Reserve and OCC regulatory streams, French and New Zealand official coverage, FDIC banking releases, Canadian and Indian central-bank/market infrastructure notices, Japan FSA English regulation, Hong Kong monetary supervision and data, Korean national-cyber coverage, national cyber advisories, incident reporting, technical research and vendor security notices; this pass adds 25 official Nordic/Iberian/Asia-Pacific Finance feeds and four official Japanese/Hong Kong Cyber Security feeds, all Master-only where mobile cost or language makes that the better fit.
- The latest phone-layer additions are European Parliament committee decisions, Council of the EU, UN News Health and FINTRAC’s official Canadian financial-intelligence news stream. Microsoft Security Blog moved to Master-only to make room for FINTRAC; the FBI Cyber Podcast and BBC Business now also remain Master-only to make room for more targeted primary-source coverage without increasing the Air/Lite feed counts. BIS Statistical Releases remains Master-only, EPPO remains in both phone profiles, and OLAF and Eurojust remain Master-only for deeper local-digest research. All are notification-off and the four interrupting notifications remain unchanged.
- Apple Intelligence remains an explicit Shortcut layer using selected Share Sheet items or prepared JSON/plain-text digest handoffs; NetNewsWire itself is not treated as a bulk unread exporter. The optional Master-profile collector now prepares an unattended 30-minute/hourly handoff through macOS `launchd`.

## Latest expansion — European Investment Bank news

- Promoted **European Investment Bank — News** (`https://www.eib.org/en/press/news/index.rss`) from Master-only into iPhone-lite and inherited iPhone Air. The [EIB newsroom](https://www.eib.org/en/press/) supplies primary-source European investment, infrastructure, climate, resilience and development-finance activity.
- The candidate screen passed with HTTP 200 RSS/XML, 10 dated items through 7 August 2026, a 21.7 KB body, 10 unique titles and links, all HTTPS item links and no exact-title or exact-link overlap with either retained phone corpus. It remains notification-off for Apple Intelligence digest review.
- This raises the explicit profile caps to 75 Lite and 83 Air while keeping the full-body budgets below 4 MiB; the Master set remains 247 feeds.

## Frozen snapshot audit — 18 August 2026

- A fresh live structural audit ran against the frozen manifest and committed OPML profiles with its cache, history and report outputs isolated in temporary storage. It did not add feeds, rewrite the manifest or alter any generated artifact.
- **Master:** 239/239 feeds returned HTTP 200 and parseable XML with zero failed feeds, noisy feeds, duplicate URLs, metadata mismatches, stale-review failures or future-dated feeds. The measured body payload was 36.27 MB; 22 feeds were in payload-review range, six exceeded 1 MB and eight exceeded the slow-refresh advisory.
- **iPhone Air:** 82/82 passed with zero hard quality or device-budget failures; the measured body payload was 4,174,640 bytes, leaving 19,664 bytes under the 4 MiB ceiling. **iPhone Lite:** 73/73 passed with zero hard quality or device-budget failures; the measured body payload was 3,607,694 bytes, leaving 586,610 bytes under the same ceiling.
- The isolated runs used no prior validation-history baseline, so their zero warning count is not a cross-run drift result. The committed validation reports remain the earlier 238/81/72 snapshot and were intentionally left untouched for the integration freeze; use the manifest and OPML counts above as the current collector input.
- Added `make check-frozen`, a non-mutating offline gate for the frozen handoff. It runs manifest/artifact lint, documentation, hygiene, tests and shell syntax checks without invoking `make package` or rewriting OPML, source-table, notification or validation-report artifacts.

## Current research pass — European environmental indicator coverage

- Added **European Environment Agency — Indicators** — `https://www.eea.europa.eu/en/newsroom/rss-feeds/indicators-rss/rss.xml` — to iPhone-lite and inherited iPhone Air. The official [EEA RSS directory](https://www.eea.europa.eu/en/newsroom/rss-feeds) publishes the indicator stream; the live endpoint returned HTTP 200 Atom/XML with 25 dated items through 14 August 2026, a 31.8 KB body, all HTTPS item links and zero internal title/link duplicates.
- The stream supplies direct EU climate, drought, emissions, marine-resource, ecosystem and environmental-risk indicators that complement the existing economic-development, health, trade and financial-policy sources. It is notification-off and routed through the Apple Intelligence digest.
- The candidate produced no exact-title or exact-link overlap against either retained phone corpus. It raises the explicit phone caps by one to 82 Air / 73 Lite while remaining inside both 4 MiB full-body budgets; the live three-profile audit below records the final headroom and regression checks.

## Current research pass — official Polish, ECB, US and Canadian statistics

- Added 15 Master-only feeds: National Bank of Poland **Table A**, **Table B** and **Table C** exchange rates; ECB **Blog**, **Working Papers** and **Research Bulletin**; BEA **News Releases**; US Census **Economic Indicators**; and seven subject-specific Statistics Canada streams covering economic accounts, labour, prices, housing, manufacturing, retail/wholesale and business performance/ownership.
- The official directories document the endpoints: [NBP RSS](https://rss.nbp.pl/), [ECB RSS](https://www.ecb.europa.eu/home/html/rss.en.html), [BEA News](https://www.bea.gov/news/), [US Census feeds](https://www.census.gov/about/contact-us/feeds.html) and [Statistics Canada RSS](https://www.statcan.gc.ca/en/sc/rss). All retained candidates passed current HTTP/XML, title/date/link and noise checks.
- Statistics Canada **International Trade** was tested but rejected because 70% of its current item links repeat the same destination; the broad All Subjects stream was also rejected as too large and less focused. The retained set therefore improves official statistical breadth without changing the 81/72 phone profiles.

## Current maintenance pass — Bank of Korea official coverage

- The manifest now retains ten official Bank of Korea English RSS streams in Master only: press releases, monetary-policy decisions, statistics and publications, payment and settlement systems, monetary-policy reports, Monetary Policy Board minutes, speeches, regional economic reports, economic analysis and the Financial Stability Report.
- These feeds add Korean monetary-policy, banking, payments, financial-stability and macro-financial research context without increasing the iPhone Air/Lite payload or notification surface. They are notification-off and remain available to the high-coverage Apple Intelligence collector.

## Current research pass — European medicines-regulatory coverage

- Added **European Medicines Agency — News and Press Releases** — `https://www.ema.europa.eu/en/news.xml` — to iPhone-lite and inherited iPhone Air. The official [EMA RSS directory](https://www.ema.europa.eu/en/news-events/rss-feeds) publishes the feed; the live endpoint returned HTTP 200 RSS/XML with `application/rss+xml`, two dated items through 30 July 2026 and a 7,540-byte body.
- The stream adds compact primary EU medicines-regulatory, pharmacovigilance, approvals and public-health regulatory signal distinct from the broad UN Health stream. It is event-driven and notification-off for the Apple Intelligence digest; the current title/link-only shape keeps article links available for follow-up without adding a large phone payload.
- The candidate produced no exact-title, exact-link or conservative fuzzy-story overlap against either retained phone corpus. It increases the explicit phone caps by one to 81 Air / 72 Lite while leaving both 4 MiB full-body ceilings unchanged.

## Current research pass — Nordic central banks, European data and Asia-Pacific cyber authorities

- Added 25 official Finance feeds from the Bank of Japan, Swiss National Bank, Norges Bank, Banco de España, Sveriges Riksbank, Czech National Bank and Danmarks Nationalbank. The set covers policy releases, statistics, regulatory circulars, speeches, minutes, financial stability, analysis, working papers and reports without adding another broad commercial-news stream.
- Added four official Cyber Security feeds: JPCERT/CC — All Updates, JVN — Vulnerability Notes, HKCERT — Security Bulletin and HKCERT — Security News. They add Japanese vulnerability coordination and Hong Kong regional-CSIRT coverage distinct from the existing Ireland/EU/US/UK/Canada sources.
- All 29 additions are Master-only and notification-off; the generated profiles remain 179 Master / 80 Air / 71 Lite. Candidate checks returned HTTP 200, parseable XML, dated items and usable web links, with zero duplicate-link failures and no noise-gate failures.
- The live Master run passed 179/179, Lite passed 71/71 and Air passed 80/80. Metadata, stale-review, future-date, noise and device-budget failures were zero. The validator now handles Norges Bank’s namespaced article links and Riksbank’s valid XML body with its malformed encoding label. One non-critical existing Krebs content-type regression warning remains.
- RBA’s official RSS directory was initially rechecked with the generic validator identity, whose direct endpoints returned WAF HTTP 403; a later anonymous/default-identity retest passed all six streams and superseded that earlier rejection with the narrow validator exception documented above.

## Current research pass — global trade and WTO coverage

- Added **WTO — Latest News** — `https://www.wto.org/library/rss/latest_news_e.xml` — to iPhone-lite and inherited iPhone Air. The official HTTP 200 RSS/XML response contains 10 dated items through 5 August 2026, a 65.1 KB body, all HTTPS article links and zero internal title/link duplicates.
- The feed adds multilateral trade disputes, safeguards, customs and market-access measures, accession, trade-and-technology policy and global-trade research that were not represented by a direct multilateral trade stream in the phone layer. It is event-driven, notification-off and intended for the daily Apple Intelligence digest.
- The official [WTO RSS gateway](https://www.wto.org/english/res_e/webcas_e/rss_e.htm) identifies the endpoint as the all-news feed. The live three-profile audit below records the final cross-feed duplicate and device-budget checks.

## Current research pass — UN economic-development and global context

- Added **UN News — Economic Development** — `https://news.un.org/feed/subscribe/en/news/topic/economic-development/feed/rss.xml` — to iPhone-lite and inherited iPhone Air. The official HTTP 200 RSS/XML response contains 30 dated items through 17 August 2026, a 33.9 KB decompressed body and a 7.1 KB gzip wire response, all HTTPS article links and zero internal title/link duplicates.
- The stream adds global growth, energy and food-price, supply-chain, critical-minerals, conflict and development-policy context around the WTO/trade and central-bank sources. It is notification-off and routed through the Apple Intelligence digest.
- The candidate produced no candidate-specific exact or conservative fuzzy duplicate cluster against the retained phone corpus. The live three-profile audit below records the final cross-feed, payload and budget checks.

## Current research pass — UN human-rights and governance context

- Added **UN News — Human Rights** — `https://news.un.org/feed/subscribe/en/news/topic/human-rights/feed/rss.xml` — to iPhone-lite and inherited iPhone Air. The official HTTP 200 RSS/XML response contains 30 dated items through 13 August 2026, a 34.0 KB body and 34.0 KB wire response, all HTTPS article links and zero internal title/link duplicates.
- The stream adds human-rights, accountability, civilian-impact, conflict and governance context that is distinct from the current finance, cyber and UN economic-development streams. It is notification-off and routed through the Apple Intelligence digest.
- The candidate produced no candidate-specific exact-title, fuzzy-story or duplicate-link cluster against the retained phone corpus. The live three-profile audit below records the final cross-feed, payload and budget checks.

## Current research pass — UN peace-and-security context

- Added **UN News — Peace and Security** — `https://news.un.org/feed/subscribe/en/news/topic/peace-and-security/feed/rss.xml` — to iPhone-lite and inherited iPhone Air. The official HTTP 200 RSS/XML response contains 30 dated items through 17 August 2026, a 34.6 KB decompressed body and a 7.1 KB gzip wire response, all HTTPS article links and zero internal title/link duplicates.
- The stream adds conflict, Security Council, geopolitical-risk and civilian-impact context that complements the UN economic-development and human-rights streams. It is notification-off and routed through the Apple Intelligence digest.
- The candidate produced no exact-title or conservative fuzzy-story cluster. Seven candidate-specific duplicate-link clusters are shared with existing UN topic streams and remain useful as corroborating labels for digest clustering. The live three-profile audit below records the final cross-feed and budget checks.

## Current research pass — UN health and biological-risk context

- Added **UN News — Health** — `https://news.un.org/feed/subscribe/en/news/topic/health/feed/rss.xml` — to iPhone-lite and inherited iPhone Air. The official HTTP 200 RSS/XML response contains 30 dated items through 17 August 2026, a 33.8 KB decompressed body and a 33.8 KB response, all HTTPS article links and zero internal title/link duplicates.
- The stream adds outbreaks, public-health capacity, health-system resilience and biological-risk context that was not represented by the retained Finance/Cyber phone feeds. It is notification-off and routed through the Apple Intelligence digest.
- The candidate produced no candidate-specific exact-title, conservative fuzzy-story or duplicate-link cluster against the retained phone corpus. At that pre-Council stage, the live audit recorded 33,825 added bytes in Air, with 5,808 bytes remaining under the 4 MiB full-body budget; the subsequent Council/FBI rebalance is recorded below.

## Current research pass — Council of the EU sanctions and foreign-policy coverage

- Added **Council of the EU — Press Releases** — `https://www.consilium.europa.eu/en/rss/pressreleases.ashx` — to iPhone-lite and inherited iPhone Air. The official HTTP 200 RSS/XML response contains 20 dated items through 14 August 2026, a 16.6 KB decompressed body and a 3.3 KB gzip wire response, all HTTPS article links and zero internal title/link duplicates. The stream is listed in the [official Council RSS directory](https://www.consilium.europa.eu/en/about-site/rss/).
- The feed adds compact EU sanctions, foreign-policy, security, economic and institutional decision context. It is event-driven, notification-off and routed through the Apple Intelligence digest.
- The candidate produced no candidate-specific exact-title, conservative fuzzy-story or duplicate-link cluster against the retained phone corpus. To keep the Air profile at 80 feeds and inside the 4 MiB full-body budget, **FBI — Ahead of the Threat Cyber Podcast** moved to Master-only; it remains available to the complete RSS bundle and hourly collector.

## Current research pass — European Parliament committee decision coverage

- Added **European Parliament — Committee Press Releases** — `https://www.europarl.europa.eu/rss/doc/press-releases-committees/en.xml` — to iPhone-lite and inherited iPhone Air. The official [European Parliament RSS directory](https://www.europarl.europa.eu/at-your-service/en/stay-informed/rss-feeds) lists committee and topic feeds; the direct response returned HTTP 200 RSS/XML with 20 dated items through 23 July 2026, about 23.4 KB, all HTTPS item links and zero internal title/link duplicates.
- The feed adds primary EU legislative, defence, digital, trade, health and economic-policy/oversight decisions that complement Council, Commission and regulator coverage. It is event-driven, notification-off and routed through the Apple Intelligence digest.
- The candidate produced no exact-title, exact-link or conservative fuzzy-story overlap against the retained phone corpus. To preserve the 80/71 phone counts and device budgets, BBC Business moved to Master-only; its broad business stream remains in the complete RSS bundle and local collector.

## Current research pass — Court of Justice of the European Union legal decisions

- Added **Court of Justice of the European Union — Press Releases** — `https://curia.europa.eu/site/rss.jsp?lang=en&secondLang=fr` — to iPhone-lite and inherited iPhone Air. The official [Curia media centre](https://curia.europa.eu/site/jcms/d2_5156/en/media-centre) documents RSS notifications for new judgments, Opinions and press releases.
- The live response returned HTTP 200 and parsed as RSS/XML with 10 dated items through 16 July 2026, a 7.5 KB body, all HTTPS item links and no exact-title, exact-link or conservative fuzzy overlap against the retained phone corpus. The endpoint labels the body as `text/html`, but the validator verifies the XML before accepting it.
- To keep the phone profiles at 80 Air / 71 Lite, **Financial Times — Markets** moved to Master-only. The phone layer now favors this compact primary EU legal-decision stream while the commercial market feed remains available in the 179-feed Master profile and hourly collector; Curia is notification-off for the Apple Intelligence digest.

## Current research pass — Canadian financial-intelligence coverage

- Added **FINTRAC — News** — `https://fintrac-canafe.canada.ca/rss/rss-eng.xml` — to iPhone-lite and inherited iPhone Air. The official HTTP 200 Atom/XML response contains 302 dated items through 6 August 2026 and a 240.6 KB body. All 302 item links pass as HTTPS after the shared parser resolves three relative links in older archive entries against the feed endpoint.
- FINTRAC’s internal repeated-title rate is 0.7% and repeated-link rate is 8.3%, below the 50% noise threshold, with no candidate-specific exact or conservative fuzzy duplicate cluster against the retained phone corpus. The feed adds Canadian AML/ATF, sanctions-evasion, financial-crime, guidance and supervisory-enforcement signal; it is notification-off for the Apple Intelligence digest.
- Moved **Microsoft Security Blog** to Master-only because its current full body is 311.4 KB and its broad vendor-research signal has lower marginal phone value than the distinct FINTRAC financial-intelligence stream. The swap preserved the phone-layer counts at that intermediate stage; subsequent validated additions bring the current bundle to 71-feed Lite / 80-feed Air, while Microsoft remains available in the 179-feed Master profile.
- Added regression coverage for resolving valid relative RSS/Atom item links in both the validation report and the hourly Apple Intelligence collector. The live Air and Lite audits pass the item-link integrity gates with no missing-link warnings for FINTRAC.

## Current research pass — UK tax/customs and Australian prudential supervision

- Added **HM Revenue & Customs — Activity on GOV.UK** to iPhone-lite/Air. The official Atom response returned HTTP 200 with 20 dated items through 17 August 2026, a 12.3 KB body, all HTTPS item links, zero internal title/link duplicates and zero exact/fuzzy overlap with the current manifest corpus; it adds UK tax administration, customs, compliance, fraud and fiscal-operational context. It is notification-off and sourced from the [HMRC GOV.UK organisation page](https://www.gov.uk/government/organisations/hm-revenue-customs/about).
- Added **APRA — News** to Master only. The official RSS response returned HTTP 200 with 10 dated items through 31 July 2026, a 221.0 KB body, all HTTPS item links, zero internal title/link duplicates and zero exact/fuzzy overlap with the current manifest corpus; it adds Australian banking, insurance, superannuation, operational-resilience and prudential-supervision coverage. It remains Master-only because adding it to the current Air set would push the measured full-body payload above the 4 MiB device budget. It is notification-off and sourced from the [APRA news page](https://www.apra.gov.au/news).

## Current research pass — UK financial crime, insolvency and specialist vulnerability research

- Added **Serious Fraud Office — Activity on GOV.UK** to iPhone-lite/Air. The official Atom response returned HTTP 200 with 20 dated items through 10 August 2026, an 11.1 KB body, all HTTPS item links, zero internal title/link duplicates and zero exact/fuzzy overlap with the retained manifest corpus; it adds UK complex fraud, bribery, corruption, proceeds-of-crime and economic-crime case activity. It is notification-off and sourced from the [official SFO page](https://www.gov.uk/government/organisations/serious-fraud-office/about).
- Added **Insolvency Service — Activity on GOV.UK** to iPhone-lite/Air. The official Atom response returned HTTP 200 with 20 dated items through 14 August 2026, a 13.2 KB body, all HTTPS item links, zero internal title/link duplicates and zero exact/fuzzy overlap; it adds UK company and individual insolvencies, director disqualification, fraud, money laundering, redundancy and creditor-recovery signals. It is notification-off and sourced from the [official Insolvency Service page](https://www.gov.uk/government/organisations/insolvency-service/about).
- Added **Google Project Zero — Research** to Master only. The official Atom response returned HTTP 200 with 10 dated items through 13 May 2026, a 13.2 MB decompressed body, all HTTPS item links, zero internal title/link duplicates and zero exact/fuzzy overlap; it adds high-value zero-day, exploit-chain, fuzzing and platform-security research. It remains outside Air/Lite because the archive is too large for a mobile single-feed payload, and is sourced from the [official Project Zero site](https://projectzero.google/).
- Rechecked **National Crime Agency — Activity on GOV.UK** but did not retain it: the valid 20-item window is dominated by corporate, workforce, remuneration and transparency publications rather than distinct operational financial-crime signal.
- Updated the live validator to fall back to the shared DTD-safe Python parser when `xmllint` rejects an otherwise valid feed because of an oversized CDATA section; the existing XML-size, content-type, title, date, link, duplication and freshness gates remain enforced.

## Current research pass — EU privacy, AI governance and data-protection enforcement

- Added **European Data Protection Board — News** to iPhone-lite/Air. Its official RSS response returned HTTP 200 with 10 dated items through 29 July 2026, a 21.2 KB body, all HTTPS item links, zero internal title/link duplicates and zero exact/fuzzy title or link overlap with the cached 133-feed corpus. It adds EU GDPR enforcement, AI and data-governance, breach/security and cross-regulatory context; notification-off for the daily Apple Intelligence digest. The feed is documented on the [official EDPB news page](https://www.edpb.europa.eu/news_en).
- Rechecked the Office of the Australian Information Commissioner’s media RSS but did not import it: its 230-item archive has no detectable item dates and 229 repeated item links. RBA’s official feeds were separately re-tested with the anonymous/default identity and are now retained under the narrow WAF exception; the UK ICO currently reports that its RSS feeds are unavailable after a site redesign.

## Current research pass — European Commission competition, tax and financial-services news

- Added **European Commission — Competition Policy News** to iPhone-lite/Air. Its official RSS response returned HTTP 200 with 30 dated items through 7 August 2026, a 43.7 KB body, all HTTPS item links, zero internal title/link duplicates and zero exact/fuzzy overlap with the cached 134-feed corpus; it adds EU antitrust, mergers, State aid and Digital Markets Act enforcement context. The feed is exposed by the [official Competition Policy news page](https://competition-policy.ec.europa.eu/about/news_en) and is notification-off.
- Added **European Commission — Taxation & Customs News** to iPhone-lite/Air. Its official RSS response returned HTTP 200 with 30 dated items through 14 August 2026, a 35.8 KB body, all HTTPS item links, zero internal title/link duplicates and zero exact/fuzzy overlap; it adds EU tax policy, customs, CBAM and compliance-implementation context. The feed is exposed by the [official Taxation and Customs news page](https://taxation-customs.ec.europa.eu/news_en) and is notification-off.
- Added **European Commission — Financial Services News (FISMA)** to iPhone-lite/Air. Its official RSS response returned HTTP 200 with 30 dated items through 3 August 2026, a 36.2 KB body, all HTTPS item links, zero internal title/link duplicates and zero exact/fuzzy overlap; it adds EU banking, capital-markets, sustainable-finance, payments and sanctions-policy context. The feed is exposed by the [official Finance news page](https://finance.ec.europa.eu/finance-news_en) and is notification-off.
- The three feeds add about 115.7 KB of full-body payload together and keep both phone profiles under the 4 MiB budget in the live validation below.

## Current research pass — EPPO, OLAF and Eurojust financial-crime coverage

- Added **European Public Prosecutor’s Office — News** to iPhone-lite/Air. Its official RSS response returned HTTP 200 with 30 dated items through 13 August 2026, a 43.1 KB body, all HTTPS item links, zero internal title/link duplicates and zero exact/fuzzy overlap with the cached 137-feed corpus; it adds EU-fund, VAT/customs, corruption and cross-border fraud enforcement context. The feed is exposed by the [official EPPO news page](https://www.eppo.europa.eu/media/news_en) and is notification-off.
- Added **European Anti-Fraud Office (OLAF) — News** to Master only. Its official RSS response returned HTTP 200 with 30 dated items through 7 August 2026, a 56.3 KB body, all HTTPS item links, zero internal title/link duplicates and zero exact/fuzzy overlap; it adds EU-budget fraud, corruption, customs, sanctions-circumvention and recovery activity. The feed is exposed by the [official OLAF news page](https://anti-fraud.ec.europa.eu/media-corner/news_en) and is notification-off.
- Added **Eurojust — Press Releases & News** to Master only. Its official RSS response returned HTTP 200 with 50 dated items through 11 August 2026, a 90.5 KB body, all HTTPS item links, zero internal title/link duplicates and zero exact/fuzzy overlap; it adds cross-border organised-crime, fraud, money-laundering, cybercrime and prosecution context. The feed is listed on the [official Eurojust RSS directory](https://www.eurojust.europa.eu/rss-feeds) and is notification-off.
- To fit EPPO into both phone profiles without weakening the 4 MiB gate, ECB Statistical Releases moved from Air to Master-only; the phone retains ECB press, operations, reference rates and Eurostat context.

## Current research pass — FBI cyber-resilience and fraud-response context

- Added **FBI — Ahead of the Threat Cyber Podcast** during the preceding phone-layer expansion. The official Atom-compatible RSS response returned HTTP 200 with 20 dated episodes through 23 July 2026 and a 27.4 KB body. Each entry supplies an HTTPS web permalink through its GUID, and the candidate had zero exact title/link and zero conservative fuzzy-title overlap with the cached 140-feed corpus. It later moved to Master-only to make room for the compact Council of the EU stream without increasing the phone profiles.
- The feed adds primary FBI Cyber Division discussion of cyber resilience, AI, critical infrastructure, cyber-enabled fraud response and law-enforcement operations. It remains notification-off and is sourced from the [official FBI Cyber Podcast page](https://www.fbi.gov/aheadofthethreat).
- The shared RSS parser now accepts an HTTPS GUID as an item permalink only when a feed omits a separate `<link>` element and the GUID is not marked as an opaque identifier. This keeps the feed’s article/audio links available to the Apple Intelligence handoff without weakening opaque-ID validation.
- The live report applies the explicit `Asia/Kolkata` source timezone to RBI’s timezone-less RSS timestamps; the global 90-minute future-date gate remains unchanged, so same-day RBI releases are not misclassified on the Dublin/UTC clock.
- **BIS — Statistical Releases** and **European Commission — Sanctions Guidance** remain in Master but are no longer in Air; the rebalance kept the then-current Air profile inside its 4 MiB full-body budget while Lite retained the compact FBI stream. Later validated additions bring the current profiles to 80 Air / 71 Lite.

## Current research pass — UK and US antitrust coverage

- Added **Competition and Markets Authority — Activity on GOV.UK** to iPhone-lite/Air. The official Atom response returned HTTP 200 with 20 dated items through 17 August 2026, a 12.7 KB body, all HTTPS item links, no exact title/link overlap with the current manifest corpus and only two repeated-title items; it adds UK competition, consumer-protection, market-investigation, digital-markets and merger-policy activity.
- Added **DOJ Antitrust Division — Press Releases** to iPhone-lite/Air. The official RSS response returned HTTP 200 with 25 dated items through 7 August 2026, a 6.9 KB body, all HTTPS item links, no exact title/link overlap with the current manifest corpus and only two repeated-title items; it adds US antitrust prosecutions, merger enforcement, settlements and competition-policy releases.
- The DOJ Antitrust Civil Case Filings and Criminal Case Filings feeds were rechecked but not retained: they are current and technically valid, yet their archives contain 142/156 and 35/83 repeated-title items respectively, so they fail the bundle’s noise gate and would weaken Apple Intelligence deduplication. All retained feeds are notification-off and sourced from the official [DOJ Antitrust news-feed directory](https://www.justice.gov/atr/news-feeds).

## Current research pass — US consumer protection, competition and merger notices

- Added **Federal Trade Commission — Consumer Protection Press Releases** to iPhone-lite/Air. The official RSS response returned HTTP 200 with 30 dated items through 17 August 2026, a 143.7 KB body, HTTPS item links, no internal title/link duplicates and no exact/fuzzy overlap with the current manifest corpus.
- Added **Federal Trade Commission — Competition Press Releases** to iPhone-lite/Air. The official RSS response returned HTTP 200 with 30 dated items through 17 August 2026, a 107.5 KB body, HTTPS item links, no internal title/link duplicates and no exact/fuzzy overlap with the current manifest corpus.
- Added **Federal Trade Commission — HSR Early Termination Notices** to Master only. Its official RSS response returned HTTP 200 with 20 dated, title-only merger notices through 14 August 2026, a 54.4 KB body, HTTPS item links and no internal title/link duplicates; it remains out of the phone profiles because the stream is specialized transaction-party intelligence.
- The broad FTC press-release feed was not retained because its current items duplicate the dedicated Consumer Protection and Competition streams. All three retained feeds are notification-off and sourced from the [FTC RSS directory](https://www.ftc.gov/stay-connected/rss).

## Current research pass — Australian Treasury policy and financial-services coverage

- Added **Australian Treasury — Treasurer’s Media Releases** to iPhone-lite/Air. Its HTTP 200 RSS/XML response contains 10 dated items through 14 August 2026, a 33.2 KB body, all HTTPS item links and zero exact/fuzzy or internal title/link duplicates.
- Added **Australian Treasury — Assistant Treasurer & Financial Services Releases** to iPhone-lite/Air. Its HTTP 200 RSS/XML response contains 10 dated items through 13 August 2026, a 28.6 KB body, all HTTPS item links and zero exact/fuzzy or internal title/link duplicates.
- Both streams are notification-off and add compact Australian fiscal, financial-system, consumer-protection, payments, scams and regulatory-policy context without breaching the Air/Lite payload budgets. AUSTRAC’s valid RSS stream was not retained because its official guidance says the feed is being replaced by email subscriptions.

## Current research pass — French and New Zealand official coverage

- Added **AMF — News** as a Master-only French financial-regulator stream. Its HTTP 200 response contains 200 dated RSS items through 4 August 2026 with zero exact/fuzzy overlap; the XML body is verified even though the server labels it `text/html`.
- Added **New Zealand NCSC — News** to iPhone-lite and inherited iPhone Air. Its HTTP 200 RSS response contains 53 dated items through 3 August 2026, with zero exact/fuzzy overlap and a 172.8 KB decompressed body.
- Rechecked JPCERT/CC and CNMV candidates but did not import them: JPCERT’s narrow feed repeats links heavily and overlaps existing vendor patch streams; CNMV’s press stream repeats non-descriptive section links and its other-relevant stream is too small and issuer-name-heavy for a stable slot.

## Current research pass — US banking supervision and Korean cyber authority

- Added **OCC — Bulletins** to iPhone-lite/Air for official national-bank supervision and regulatory coverage; its live feed passed with 10 dated bulletins and a 10.8 KB body.
- Added **FDIC — Press Releases** to Master-only for official deposit-insurance, bank-resolution and stability coverage; its current body is roughly 927 KB and remains outside the phone profiles.
- Added **KISA — Press Releases (Korean)** to Master-only for Korean national cyber and digital-security context; its live feed passed with 10 dated items, but its Korean-language content and legacy HTTP item links make it unsuitable for the default phone layer.

## Current research pass — Canadian central bank and Hong Kong monetary authority

- Added **Bank of Canada — Press Releases** and **Market Notices** to iPhone-lite/Air. Both are compact official RSS 1.0 streams with 10 dated items, zero exact/fuzzy overlap and distinct Canadian monetary-policy/market-infrastructure signal.
- Added **Bank of Canada — Regulatory News** and **Financial Stability Report** to Master-only. They add payment-service compliance, notices of violation, financial-stability assessments and Canada-specific vulnerability context without growing the phone payload.
- Added **HKMA — Circulars**, **Daily Monetary Statistics** and **Speeches** to Master-only from the official HKMA RSS directory. They provide Hong Kong banking-supervision, monetary-data and financial-stability/policy context; the broad 679-item HKMA Press stream was rejected for a 61.1% repeated-title rate.

## Current research pass — India and Japan official financial authorities

- Added **Reserve Bank of India — Press Releases** and **Notifications** to iPhone-lite/Air. Both are compact, current, dated official RSS/XML streams with zero exact or fuzzy title overlap; they add Indian market-operations, monetary, prudential, payments and regulated-entity signal.
- Added **Reserve Bank of India — Speeches** to iPhone Air. Its current ten-item body is 227.5 KB and adds compact English-language central-bank policy and supervisory context without exceeding the Air single-feed budget.
- Added **Reserve Bank of India — Publications & Surveys** to Master-only. Its current ten-item body is 668.1 KB, above the 600 KB mobile single-feed ceiling, but it adds useful official inflation-expectations, confidence, lending, manufacturing and payments-system research.
- Added **Japan Financial Services Agency — English News** to iPhone-lite/Air. Its current ten-item body is only 3.6 KB and adds English-language banking, securities, insurance, fintech and financial-policy coverage.
- Rechecked RBA feeds with the generic validator identity; that earlier HTTP 403 result was superseded by the focused anonymous/default-identity audit and six retained official streams. RBI Tenders was rejected as procurement/facilities noise; Japan FSA’s all-language feed was rejected as a duplicate-language layer against the English stream.

## Earlier live validation snapshot — 19 August 2026

- **Master:** **370/370** feed responses returned HTTP 200 and parseable RSS/XML, with zero failed transport/XML feeds, metadata mismatches, stale-review failures, hard future-date failures or noise failures. No future-date exception was triggered in this run; the scoped Nasdaq tolerance remains documented for recurrence. All 370 source-table rows matched the manifest and OPML. The fresh run has zero regression warnings; accepted item-link transport warnings for publishers whose feeds expose missing or legacy table links, including BoJ, remain non-fatal.
- FEMA News Releases and the six FDA streams passed the same direct HTTPS, XML, title, date, link, duplicate and freshness gates as the NRC, CDC MMWR, USGS, EIA, CDC travel/EID, ECDC, UK strategic/public-infrastructure, U.S. defense, IAEA, EASA, EUSPA, European Commission, EFSA, EPO, EEA, EUR-Lex, GFSC, DNB, NCA, PSFA, EIOPA, Finanstilsynet, Japan FSA, CSSF, FMA Austria, FSMA Belgium and NCSC-FI additions. FDA’s six feeds have legacy HTTP article permalinks; the verified HTTPS feed endpoints remain accepted with transport warnings.
- **iPhone Air:** **86/86** remains within its device budget at **4,128,115 bytes** and **1,980,811 wire bytes**, leaving 66,189 bytes below the 4 MiB full-body ceiling; **iPhone Lite:** **79/79** remains within its device budget at **3,978,274 bytes** and **1,936,979 wire bytes**, leaving 216,030 bytes below the same ceiling. Air has one payload-review feed and no slow-refresh advisory; Lite has two payload-review feeds and one slow-refresh advisory. Air and Lite both record zero regression warnings.
- Current Master payload telemetry is **47,114,780 bytes** (**27,209,973 wire bytes**), with 35 payload-review feeds, eight above 1 MiB and 12 slow-refresh advisories. The generated reports under `artifacts/validation/` are the authoritative evidence for payload, latency, item-link transport, the scoped timestamp exception, the RBA/DNB/CFP/NRC/FEMA neutral-identity exceptions and the structured-alert policies.

## Previous follow-up maintenance — feed recovery and official authority expansion

- Replaced the blocked Cisco Talos endpoint `https://blog.talosintelligence.com/rss/` with the working Cisco-content feed `https://feeds.feedburner.com/feedburner/Talos`; it now passes the live RSS/XML, freshness and item-integrity gates while retaining the Talos article page as its HTML source.
- Added six Master-only Finance feeds: EIOPA Risk-Free Rate Term Structures; Bank of England Bank Insights, Statistics, Speeches and Prudential Regulation Publications; and FINMA News. These fill insurance-rate, UK prudential/data/analysis and Swiss supervisory gaps without changing the phone profiles.
- Added two Master-only Cyber Security feeds from the Canadian Centre for Cyber Security: Alerts & Advisories, plus Guidance, News & Events. The latter is intentionally Master-only because its current full body is about 1.86 MB.
- Tested the official Australian ASD’s ACSC Advisories, Alerts, News, Advice and Publications endpoints. All five timed out with zero bytes from the validator-compatible local path, so they remain documented candidates rather than unverified imports.

## Previous follow-up live validation — 18 August 2026

- **Master:** 109/109 feeds passed the live HTTP/XML/integrity gates; 0 metadata mismatches, 0 stale-review failures, 0 future-date failures and 0 noisy feeds. One structured-alert exception is recorded for the Nasdaq Trade Halts stream; all 109 endpoints passed.
- All eight follow-up additions passed with HTTP 200, recognized RSS/Atom/XML roots, complete titles/dates/HTTPS item links and no noise-gate failures. The new feeds include 111 EIOPA items, current Bank of England streams, 50 FINMA items and two current Canadian Cyber Centre streams.
- **iPhone Air:** 57/57 passed in the current profile-specific run; **iPhone Lite:** 46/46 passed. Both had 0 metadata, stale-review, future-date, noise and device-budget failures; each recorded one non-critical regression warning from the expanded baseline.
- The Master audit measured 16.70 MB of full feed bodies, a 24.6 KB median and a 981.6 KB p95; five feeds exceed 1 MB, all remaining Master-only. Three feeds exceeded the two-second refresh advisory, so the generated reports remain the operational detail for payload and latency review.
- The working Cisco Talos replacement removed the previous Master-only Talos transport failure. The generated reports under `artifacts/validation/` are the authoritative current evidence.

## This maintenance pass — ESMA feed and embedded publication timestamps

### Added

- **European Securities and Markets Authority — News** — `https://www.esma.europa.eu/rss.xml`
  - Adds official EU securities-regulator coverage across market integrity, trading, supervision, digital finance and investor protection.
  - Live candidate check: HTTP 200, RSS/XML, 10 dated items through 14 August 2026, 54.2 KB body, 9.1 KB wire response, 0.22 s fetch and no exact or fuzzy title/link overlap with the retained bundle.
  - Included in iPhone-lite and inherited by iPhone Air; notification-off for daily digest review.

### Reliability improvements

- The shared RSS parser now accepts an explicit escaped HTML `<time datetime="…">` timestamp as a fallback when a feed omits standard RSS/Atom date fields; the ESMA format is covered by a deterministic regression test.
- The validator now treats repeated ticker titles in the existing Nasdaq Trade Halts structured-alert feed as alert structure rather than editorial noise, and allows a documented 90-minute publisher/server clock-skew tolerance for future-date checks.

## This maintenance pass — official supervision and financial-research batch

- Retained 17 additional official RSS sources after live candidate checks: ECB Banking Supervision press; Financial Stability Board news; Single Resolution Board news; three Federal Reserve regulatory streams; two additional ECB Banking Supervision streams; three Federal Reserve research streams; two BIS research/speech streams; and four European Investment Bank streams.
- ECB Banking Supervision press plus Federal Reserve Banking & Consumer Regulatory Policy and Enforcement Actions are in iPhone-lite/Air; the remaining additions are Master-only to keep the phone digest focused.
- The candidate fetches returned HTTP 200 and valid RSS/XML (including RSS 1.0/RDF) with dated current items; the final profile validation below is the authoritative integrity and budget result.

## This maintenance pass — official cyber alerts, research and vendor advisories

- Retained 16 additional cyber-security feeds after live structure, freshness, payload and overlap checks: CISA News; NCSC Netherlands advisories; CERT.at warnings; CERT Polska advisories; CERT-SE News; The DFIR Report; OWASP; Zero Day Initiative; Trail of Bits; MSRC Security Update Guide; Ubuntu Security Notices; Red Hat Security Advisories; Docker Security; Securelist; SentinelLabs; and Cloudflare Security.
- CISA News is included in iPhone-lite/Air as the fourth new compact official alert/context stream; the national-CSIRT, incident-response, technical-research and vendor-specialist additions remain Master-only to keep mobile refresh cost and language breadth deliberate.
- The live checks returned HTTP 200 and parseable RSS/XML with current dated items: CISA News (10 items through 12 August), NCSC Netherlands (25 through 15 August), CERT Polska (100 through 17 August), Ubuntu and Red Hat (current through 17 August), and the research feeds all within the configured freshness window.
- MSRC is retained despite its 5,000-item, roughly 2.5 MB archive because it is an authoritative vulnerability stream; Trail of Bits is also Master-only because its current XML body is about 1.06 MB. Neither is part of the phone payload budget.
- BSI CERT-Bund WID was rejected for a conservative 0.52 duplicate-title rate; CyberWire could not be reproduced through the validator because its Brotli response was not locally decodable; stale, redirecting or unstable specialist endpoints were not imported.

## Baseline live validation — 18 August 2026

- **Master:** 94/96 feeds passed the live HTTP/XML/integrity gates; 0 metadata mismatches, 0 stale-review failures, 0 future-date failures, 0 noisy feeds and 0 device-budget failures. The two failures are existing Nasdaq endpoints: Trade Halts (HTTP 403) and Equity Trader Alerts (HTTP 403).
- **iPhone Air:** 53/55 passed; both device-budget status and all non-transport quality gates passed. **iPhone Lite:** 42/44 passed with the same two existing Nasdaq 403 failures; its declared 44-feed budget passed.
- Every one of the 34 feeds added in this maintenance pass passed the Master live audit, including CERT-SE. The two Nasdaq failures remain documented transport limitations; Cisco Talos passed on its current feed URL.
- The generated reports are committed under `artifacts/validation/`; the deterministic gates remain green with `make check`, while live validation returns non-zero only for those two endpoint transport failures.

## This maintenance pass — public repository hardening

- Reworked the public README around the required app, optional Apple workflow, install paths and exact Air/Lite/Master feed membership so the project is understandable before opening any files.
- Added a manifest-backed profile coverage matrix and per-feed Air/Lite/notification table, plus a clearer AirDrop quick-start note.
- Added a safe `make help` default, a sequential `make validate-all` command, Dependabot updates for GitHub Actions and a `CODEOWNERS` review owner.
- Added a manifest-backed README check that validates local links, all 238 feed names and every profile count before a change can pass `make check`.
- Added a tracked-file hygiene gate for credentials, machine-specific paths and local runtime state, and documented the `curl`/`xmllint` requirements for live audits.
- Reorganized public materials into `docs/`, `artifacts/` and `examples/`, with the manifest and maintenance scripts remaining discoverable at the root.
- Added README previews showing the imported NetNewsWire feed view and the selected-article → Shortcuts → Apple Intelligence → Notes result.
- Added an AirDrop handoff comparison so the ready-to-send iPhone Air OPML cannot drift from the generated artifact.
- Fixed validation-report temporary-output naming so each Markdown report links to its real committed JSON companion.
- Updated CI to run the deterministic gate when Markdown documentation changes, and added public pull-request, feed-request, validation-failure and security-reporting workflows.
- Corrected the GitHub publication guide to reflect the live public repository, existing `origin`, default branch, draft PR and remaining license decision.

## Today’s import-readiness verification — 16 August 2026

- Refreshed the new ESMA manifest validation date to **2026-08-17** after a live candidate check; regenerated all OPML, source-table and notification artifacts.
- Confirmed OPML 2.0 XML validity and profile sizes of **96 / 55 / 44** feeds with unique HTTPS feed URLs and matching manifest/source-table order.
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

- Air: **50/50** HTTP/XML/integrity pass, 0 noisy feeds, 0 metadata mismatches, 0 stale-review failures, 0 budget failures, 2.57 MB full-body payload, 1.16 MB measured wire bytes, 5 advisory review feeds, 3 fetches over 2 seconds and 0 feeds over 1 MB.
- Lite: **39/39** pass and remains within the same 4 MB/600 KB device limits.
- Master: **62/62** pass; its larger 5.65 MB full-body payload is intentionally not the default phone profile.

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
- FINRA’s official RSS endpoints remain HTTP-only and were not imported under the HTTPS/reproducibility policy. CFPB Newsroom is now retained through the exact neutral-identity exception documented in the latest maintenance section.

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
- Generated [notification/profile matrix](./artifacts/notifications/NetNewsWire-Notification-Profile.md) plus machine-readable [JSON](./artifacts/notifications/NetNewsWire-Notification-Profile.json), derived from the manifest and covering all 51 feeds across master and iPhone Lite.
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
- **`prepare-rss-digest-input.py`** and [NetNewsWire-Daily-Digest-Workflow.md](./docs/NetNewsWire-Daily-Digest-Workflow.md) for stateful, link-canonicalized daily digest input preparation.
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

- Added [NetNewsWire-RSS-Feed-Discovery-and-Addition-Prompt.md](./docs/NetNewsWire-RSS-Feed-Discovery-and-Addition-Prompt.md), a copy-paste prompt for finding new Finance and Cyber Security candidates without feed-count inflation.
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

The detailed decisions are in [Coverage-Gap-Assessment.md](./docs/Coverage-Gap-Assessment.md).

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
- Added [Apple-Intelligence-RSS-Summary-Prompt.md](./docs/Apple-Intelligence-RSS-Summary-Prompt.md) with deduplication, confidence, Dublin-time, source-classification and confirmed-versus-speculative guardrails.

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
