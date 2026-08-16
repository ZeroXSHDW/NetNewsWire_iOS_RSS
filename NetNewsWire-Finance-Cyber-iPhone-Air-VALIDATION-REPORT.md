# NetNewsWire Finance + Cyber Validation Report — iphone-air

Validation date: 16 August 2026 10:29 IST (Europe/Dublin)

Command:

```text
validate-rss-bundle.sh
```

## Results

| Check | Result |
|---|---:|
| Feed elements in OPML | 50 |
| Unique feed URLs | 50 |
| Duplicate URLs | 0 |
| HTTPS feed URLs | 50/50 |
| Effective URLs remain HTTPS | 50/50 |
| HTTP 200 responses | 50/50 |
| Conditional 304 responses reused from cache | 0 |
| Successful responses including cached 304s | 50/50 |
| Feed bodies verified as RSS/XML (not JSON) | 50/50 |
| MIME labels explicitly XML/RSS/Atom | 49/50 |
| MIME-labelled HTML but verified XML body | 1 |
| Feed payload measured | 50/50 |
| Maximum accepted response body | 16.00 MB |
| Responses over maximum size | 0 |
| Total feed payload in this audit | 2.57 MB |
| Median feed payload | 17.0 KB |
| 95th-percentile feed payload | 218.8 KB |
| Compressed/wire bytes measured | 50/50 |
| Total measured wire bytes | 1.07 MB |
| 95th-percentile wire bytes | 119.3 KB |
| Feed parse time measured | 50/50 |
| Total feed parse time | 0.064 seconds |
| Slowest feed parse | 0.005 seconds |
| Feeds over mobile review threshold (256 KB) | 3 |
| Feeds over 1 MB | 0 |
| Fetches over 2 seconds | 1 |
| Slowest measured fetch | 2.88 seconds |
| Device budget configured | Yes |
| Device budget status | Pass |
| Device budget failures | 0 |
| Parseable XML documents | 50/50 |
| RSS/Atom/RSS 1.0 roots | 50/50 |
| Non-empty feed titles | 50/50 |
| Valid item URLs | 49/50 |
| Structured alert identity | 1/50 |
| Item titles with text | 1198/1198 |
| Feeds with all item titles valid | 50/50 |
| Item dates with valid timestamps | 1198/1198 |
| Feeds with all item dates valid | 50/50 |
| Feeds with all item URLs valid (exception-aware) | 50/50 |
| Item URLs with HTTP(S) links | 1180/1198 |
| Item URLs using HTTPS | 1098/1198 |
| Item URLs using legacy HTTP | 82 |
| Items without a per-item URL | 18 |
| Feeds with any legacy HTTP item links | 4 |
| Feeds with any missing item links | 1 |
| Recent content, default max age 180 days | 49/50 |
| Feeds marked event-driven in OPML | 32/50 |
| Stale feeds allowed by event-driven policy | 1 |
| Recent or allowed event-driven content | 50/50 |
| Oldest detected current item | 212.9 days |
| Cross-feed duplicate title clusters | 7 |
| Cross-feed duplicate link clusters | 6 |
| Fuzzy duplicate title clusters | 0 |
| Feeds over noise review threshold | 0 |
| OPML/source-table URL sets | Match |
| Manifest feeds | 50 |
| Manifest/OPML URL order | Match |
| Manifest/source-table URL order | Match |
| Source-table rows | 50/50 |
| Source-table rows with complete metadata | 50/50 |
| Metadata mismatches | 0 |
| Source-table duplicate URLs | 0 |
| Stale-review deadlines due | 0 |
| Future-dated items | 0 |
| Failed feeds | 0 |
| Cross-run drift baseline available | No — this run establishes it |
| Cross-run drift warnings | 0 (0 critical) |

Duplicate-story clusters are reported for Apple Intelligence deduplication within a 3-day publication window. A feed crosses the noise gate when it has at least 10 items and more than 50% repeated item titles or links.

Every retained item must have a non-empty title and a parseable publication/update date. Item-link transport is reported separately: direct feed endpoints must remain HTTPS, while legacy HTTP article links are warnings rather than hard failures when the feed itself is a verified HTTPS RSS/XML source. The Nasdaq Trade Halts feed is a deliberate structured-alert exception only for per-item URLs: its entries contain halt fields and titles but no per-item URLs.
Mobile refresh telemetry measures the full response body and compressed/wire transfer separately. Feed bodies over 256 KB are flagged for review, bodies over 1 MB are marked large, and fetches over 2 seconds are flagged as slow. The validator also reuses a local ETag/Last-Modified cache and reports conditional 304 responses; NetNewsWire refreshes can be smaller when servers honor validators.
When a profile declares a device budget, the current audit enforces its feed-count, full-body payload, mobile-review and interrupting-notification limits. The payload budget uses full response bodies so conditional 304 responses cannot hide a profile that has grown too large.
Normal feeds must have a detectable item date within the configured age window. Event-driven feeds require a documented freshness reason and have a manifest-level stale-review deadline; they still must pass every other structural and integrity check.
The manifest is the source of truth for feed identity, folder, profile, freshness and notification policy. The validator compares it with both the OPML and the source table, including ordered metadata fields.

## Feed health

| Feed | HTTP | Cache | Root | Final HTTPS | Content type | Body | Wire | Encoding | Fetch s | Parse s | Freshness policy | Recent | Items | Missing titles | Missing dates | HTTPS item links | HTTP item links | Missing item links | Latest age | Duplicate titles | Duplicate links | Redirected | ETag / Last-Modified |
|---|---:|---|---|---|---|---:|---:|---|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| NASDAQTrader.com | 200 | no | rss | yes | text/xml | 23.6 KB (small) | 3.4 KB | gzip | 0.36 | 0.001 | standard | yes | 18 | 0 | 0 | 0 | 0 | 18 | 2.2 | 0.0% | 0.0% | no |    / Sun, 16 Aug 2026 09 |
| NASDAQTrader.com | 200 | no | rss | yes | text/xml | 34.7 KB (small) | 4.7 KB | gzip | 0.73 | 0.001 | event-driven | yes | 40 | 0 | 0 | 0 | 40 | 0 | 5.5 | 0.0% | 0.0% | no |    / Sun, 16 Aug 2026 09 |
| BBC News | 200 | no | rss | yes | text/xml; charset=utf-8 | 38.0 KB (small) | 8.0 KB | gzip | 0.15 | 0.002 | standard | yes | 53 | 0 | 0 | 53 | 0 | 0 | 0.1 | 7.5% | 3.8% | no |    /    |
| Bloomberg Markets | 200 | no | rss | yes | text/xml; charset=utf-8 | 17.0 KB (small) | 5.6 KB | gzip | 0.24 | 0.001 | standard | yes | 20 | 0 | 0 | 20 | 0 | 0 | 0.1 | 0.0% | 0.0% | no | W/"43fc-PJ4uL1SwMLVZq7c6hzrGkjk6bhQ" /   |
| Markets | 200 | no | rss | yes | text/xml; charset=utf-8 | 11.5 KB (small) | 3.7 KB | gzip | 0.20 | 0.001 | standard | yes | 25 | 0 | 0 | 25 | 0 | 0 | 0.2 | 0.0% | 0.0% | no | W/"2dd5-2+jE41+XAFQabzbX0dROppCdB/E" /    |
| Business | 200 | no | rss | yes | application/rss+xml; charset=utf-8 | 25.9 KB (small) | 6.2 KB | gzip | 0.13 | 0.001 | standard | yes | 40 | 0 | 0 | 40 | 0 | 0 | 0.1 | 0.0% | 0.0% | no |    / Sun, 16 Aug 2026 07 |
| News and Media | 200 | no | rss | yes | application/rss+xml | 143.8 KB (small) | 32.4 KB | gzip | 0.19 | 0.002 | event-driven | yes | 25 | 0 | 0 | 25 | 0 | 0 | 1.9 | 0.0% | 0.0% | no |    /    |
| ECB - European Central Bank | 200 | no | rss | yes | text/xml | 5.8 KB (small) | 1.5 KB | gzip | 1.55 | 0.001 | event-driven | yes | 15 | 0 | 0 | 15 | 0 | 0 | 3.0 | 0.0% | 0.0% | no |    / Fri, 14 Aug 2026 12 |
| European Banking Authority | 200 | no | rss | yes | application/rss+xml; charset=utf-8 | 11.2 KB (small) | 11.2 KB |    | 0.21 | 0.001 | event-driven | yes | 10 | 0 | 0 | 10 | 0 | 0 | 9.9 | 0.0% | 0.0% | no |    /    |
| ECB - European Central Bank | 200 | no | rss | yes | text/xml | 5.9 KB (small) | 1.5 KB | gzip | 0.26 | 0.001 | event-driven | yes | 15 | 0 | 0 | 15 | 0 | 0 | 40.0 | 0.0% | 0.0% | no |    / Tue, 07 Jul 2026 08 |
| Authority for Anti-Money Laundering and Countering the Financing of Terrorism \| News articles | 200 | no | rss | yes | application/rss+xml; charset=utf-8 | 39.6 KB (small) | 5.6 KB | gzip | 0.10 | 0.001 | event-driven | yes | 30 | 0 | 0 | 30 | 0 | 0 | 10.1 | 0.0% | 0.0% | no |    /    |
| News | 200 | no | rss | yes | text/xml; charset=utf-8 | 24.6 KB (small) | 6.5 KB | gzip | 0.67 | 0.001 | event-driven | yes | 50 | 0 | 0 | 50 | 0 | 0 | 4.9 | 0.0% | 0.0% | no |    /    |
| News and communications from HM Treasury (HMT) | 200 | no | feed | yes | application/atom+xml; charset=utf-8 | 12.6 KB (small) | 12.6 KB |    | 0.11 | 0.001 | event-driven | yes | 20 | 0 | 0 | 20 | 0 | 0 | 9.0 | 0.0% | 0.0% | no | W/"7913ee7c3ce8674aaf03d62f49ba9432" /    |
| FRB: Press Release - Monetary Policy | 200 | no | rss | yes | text/xml | 9.4 KB (small) | 0.9 KB | gzip | 0.12 | 0.001 | event-driven | yes | 15 | 0 | 0 | 15 | 0 | 0 | 17.6 | 26.7% | 0.0% | no | W/"e950b61b841fdd1 / Wed, 29 Jul 2026 18 |
| Press Releases | 200 | no | rss | yes | application/rss+xml; charset=utf-8 | 17.7 KB (small) | 5.0 KB | gzip | 0.26 | 0.001 | event-driven | yes | 25 | 0 | 0 | 25 | 0 | 0 | 1.6 | 0.0% | 0.0% | no | "1786872519" / Sun, 16 Aug 2026 09 |
| Press Releases | 200 | no | rss | yes | application/rss+xml; charset=utf-8 | 4.6 KB (small) | 1.2 KB | gzip | 1.19 | 0.001 | event-driven | yes | 10 | 0 | 0 | 10 | 0 | 0 | 2.8 | 0.0% | 0.0% | no | W/"1786855736" / Sun, 16 Aug 2026 04 |
| Press Releases | 200 | no | rss | yes | application/rss+xml; charset=utf-8 | 4.4 KB (small) | 1.1 KB | gzip | 0.17 | 0.001 | event-driven | yes | 10 | 0 | 0 | 10 | 0 | 0 | 4.6 | 0.0% | 0.0% | no | W/"1786842603" / Sun, 16 Aug 2026 01 |
| ECB - Monetary policy tender operations and ad-hoc communications | 200 | no | rss | yes | application/rss+xml | 11.4 KB (small) | 1.1 KB | gzip | 0.16 | 0.001 | event-driven | yes | 32 | 0 | 0 | 0 | 32 | 0 | 4.0 | 0.0% | 0.0% | no | "myra-4184defa" /    |
| FRB: Speeches | 200 | no | rss | yes | text/xml | 9.5 KB (small) | 1.7 KB | gzip | 0.22 | 0.001 | event-driven | yes | 15 | 0 | 0 | 15 | 0 | 0 | 10.6 | 0.0% | 0.0% | no | W/"db4d36b91525dd1 / Wed, 05 Aug 2026 20 |
| ECB \| US dollar (USD) - Euro foreign exchange reference rates | 200 | no | rdf:RDF | yes | application/rss+xml | 7.1 KB (small) | 1.2 KB | gzip | 2.88 | 0.000 | standard | yes | 5 | 0 | 0 | 0 | 5 | 0 | 1.8 | 0.0% | 0.0% | no | "myra-9a99e52a" /    |
| ECB \| Pound sterling (GBP) - Euro foreign exchange reference rates | 200 | no | rdf:RDF | yes | application/rss+xml | 7.2 KB (small) | 1.2 KB | gzip | 1.45 | 0.000 | standard | yes | 5 | 0 | 0 | 0 | 5 | 0 | 1.8 | 0.0% | 0.0% | no | "myra-6769cc18" /    |
| ECB - European Central Bank | 200 | no | rss | yes | application/rss+xml | 5.4 KB (small) | 1.2 KB | gzip | 0.16 | 0.001 | event-driven | yes | 15 | 0 | 0 | 15 | 0 | 0 | 16.1 | 0.0% | 0.0% | no | "myra-9810a5fd" /   |
| Markets Updates Feed | 200 | no | rss | yes | application/rss+xml | 7.9 KB (small) | 1.0 KB | gzip | 0.23 | 0.001 | event-driven | yes | 25 | 0 | 0 | 25 | 0 | 0 | 17.1 | 0.0% | 0.0% | no |   /   |
| Eurostat - Custom RSS Feed | 200 | no | feed | yes | application/atom+xml;charset=UTF-8 | 10.1 KB (small) | 1.9 KB | gzip | 0.16 | 0.000 | event-driven | yes | 11 | 0 | 0 | 11 | 0 | 0 | 2.0 | 0.0% | 0.0% | no |   /   |
| Finance \| Guidance documents | 200 | no | rss | yes | application/rss+xml; charset=utf-8 | 24.7 KB (small) | 3.5 KB | gzip | 0.11 | 0.001 | event-driven | event-driven | 19 | 0 | 0 | 19 | 0 | 0 | 212.9 | 0.0% | 0.0% | no |   /   |
| ONS Release Calendar RSS Feed. | 200 | no | rss | yes | application/rss+xml | 5.7 KB (small) | 1.5 KB | gzip | 0.10 | 0.000 | standard | yes | 10 | 0 | 0 | 10 | 0 | 0 | 2.0 | 0.0% | 0.0% | no |    / Sun, 16 Aug 2026 09 |
| BIS statistical releases | 200 | no | rdf:RDF | yes | application/rss+xml | 35.3 KB (small) | 5.4 KB | gzip | 0.15 | 0.001 | event-driven | yes | 25 | 0 | 0 | 25 | 0 | 0 | 16.0 | 0.0% | 0.0% | no | "8d32-657e3932b61c3-gzip" / Fri, 31 Jul 2026 07 |
| Publications | 200 | no | rss | yes | text/xml; charset=utf-8 | 22.7 KB (small) | 5.5 KB | gzip | 0.43 | 0.002 | event-driven | yes | 50 | 0 | 0 | 50 | 0 | 0 | 1.9 | 0.0% | 0.0% | no |   /   |
| Financial Conduct Authority (FCA) | 200 | no | rss | yes | application/rss+xml; charset=utf-8 | 65.2 KB (small) | 21.7 KB | gzip | 0.14 | 0.005 | event-driven | yes | 20 | 0 | 0 | 20 | 0 | 0 | 2.0 | 0.0% | 0.0% | no | W/"1786860034" / Sun, 16 Aug 2026 06 |
| Financial Conduct Authority (FCA) | 200 | no | rss | yes | application/rss+xml; charset=utf-8 | 58.7 KB (small) | 5.3 KB | gzip | 0.11 | 0.005 | event-driven | yes | 20 | 0 | 0 | 20 | 0 | 0 | 1.8 | 0.0% | 0.0% | no | W/"1786860941" / Sun, 16 Aug 2026 06 |
| Office of Financial Sanctions Implementation | 200 | no | feed | yes | application/atom+xml; charset=UTF-8 | 97.5 KB (small) | 97.5 KB |    | 0.15 | 0.001 | event-driven | yes | 10 | 0 | 0 | 10 | 0 | 0 | 53.8 | 0.0% | 0.0% | no | "9d4467bd806020319f01466daffe2c1e" / Wed, 24 Jun 2026 11 |
| NCSC Alerts & Advisories | 200 | no | rss | yes | application/rss+xml | 119.3 KB (small) | 119.3 KB |    | 0.24 | 0.005 | event-driven | yes | 225 | 0 | 0 | 225 | 0 | 0 | 25.4 | 1.8% | 1.8% | no | "6a7f18bb-1dd23" / Fri, 14 Aug 2026 13 |
| All CISA Advisories | 200 | no | rss | yes | application/rss+xml; charset=utf-8 | 496.4 KB (review) | 59.5 KB | gzip | 0.21 | 0.005 | event-driven | yes | 30 | 0 | 0 | 30 | 0 | 0 | 2.9 | 16.7% | 0.0% | no |    /    |
| Latest publications of type Security Advisories | 200 | no | rss | yes | text/xml; charset=utf-8 | 9.1 KB (small) | 9.1 KB |    | 0.29 | 0.000 | event-driven | yes | 10 | 0 | 0 | 10 | 0 | 0 | 24.0 | 0.0% | 0.0% | no |    /    |
| CERT-FR | 200 | no | rss | yes | application/xml | 25.5 KB (small) | 25.5 KB |    | 0.10 | 0.001 | event-driven | yes | 40 | 0 | 0 | 40 | 0 | 0 | 25.4 | 0.0% | 0.0% | no | "0be3967825899f6c231265373e818eda" / Fri, 14 Aug 2026 13 |
| News Feed | 200 | no | rss | yes | application/rss+xml; charset=utf-8 | 11.9 KB (small) | 2.9 KB | gzip | 0.12 | 0.001 | standard | yes | 20 | 0 | 0 | 20 | 0 | 0 | 11.9 | 0.0% | 0.0% | no | W/"1786716944" / Fri, 14 Aug 2026 14 |
| All Feed | 200 | no | rss | yes | application/rss+xml; charset=utf-8 | 11.2 KB (small) | 2.9 KB | gzip | 0.14 | 0.001 | event-driven | yes | 20 | 0 | 0 | 20 | 0 | 0 | 2.9 | 0.0% | 0.0% | no | W/"1786716704" / Fri, 14 Aug 2026 14 |
| BleepingComputer | 200 | no | rss | yes | text/xml; charset=utf-8 | 12.7 KB (small) | 3.2 KB | gzip | 0.12 | 0.001 | standard | yes | 15 | 0 | 0 | 15 | 0 | 0 | 0.8 | 0.0% | 0.0% | no | 3e71fc49bec24c5d3a0cdca11c682919 / Sun, 16 Aug 2026 09 |
| Krebs on Security | 200 | no | rss | yes | text/html; charset=UTF-8 | 123.0 KB (small) | 36.5 KB | gzip | 0.12 | 0.002 | standard | yes | 10 | 0 | 0 | 10 | 0 | 0 | 1.9 | 0.0% | 0.0% | no |    / Sun, 16 Aug 2026 09 |
| CyberScoop | 200 | no | rss | yes | application/rss+xml; charset=UTF-8 | 66.1 KB (small) | 21.9 KB | gzip | 0.11 | 0.001 | standard | yes | 10 | 0 | 0 | 10 | 0 | 0 | 2.5 | 0.0% | 0.0% | no | W/"1f39778779f5d97122e2057c3c8820d5" / Thu, 13 Aug 2026 22 |
| The Record from Recorded Future News | 200 | no | rss | yes | text/xml | 5.2 KB (small) | 1.6 KB | gzip | 0.18 | 0.000 | standard | yes | 5 | 0 | 0 | 5 | 0 | 0 | 1.5 | 0.0% | 0.0% | no |    /    |
| SANS Internet Storm Center, InfoCON: green | 200 | no | rss | yes | text/xml; charset=utf-8 | 8.7 KB (small) | 2.4 KB | gzip | 0.56 | 0.000 | standard | yes | 10 | 0 | 0 | 10 | 0 | 0 | 2.3 | 0.0% | 0.0% | no | W/"22b5-659269d3f4355" / Sun, 16 Aug 2026 09 |
| CERT Recently Published Vulnerability Notes | 200 | no | feed | yes | application/atom+xml; charset=utf-8 | 164.9 KB (small) | 164.9 KB |    | 0.19 | 0.002 | event-driven | yes | 15 | 0 | 0 | 15 | 0 | 0 | 4.8 | 0.0% | 0.0% | no |    / Fri, 14 Aug 2026 14 |
| Cybersecurity Insights | 200 | no | rss | yes | application/rss+xml; charset=utf-8 | 42.3 KB (small) | 11.1 KB | gzip | 0.42 | 0.001 | event-driven | yes | 40 | 0 | 0 | 40 | 0 | 0 | 3.9 | 20.0% | 0.0% | no | "1786871446-gzip" / Sun, 16 Aug 2026 09 |
| Microsoft Security Blog | 200 | no | rss | yes | application/rss+xml; charset=UTF-8 | 304.1 KB (review) | 78.9 KB | gzip | 0.27 | 0.003 | standard | yes | 10 | 0 | 0 | 10 | 0 | 0 | 5.7 | 0.0% | 0.0% | no | "c8f0c308c3fb485beed7fba1ccf23b95-gzip" / Fri, 14 Aug 2026 15 |
| Unit 42 | 200 | no | feed | yes | application/atom+xml; charset=UTF-8 | 23.7 KB (small) | 23.7 KB |    | 0.19 | 0.001 | standard | yes | 15 | 0 | 0 | 15 | 0 | 0 | 5.0 | 0.0% | 0.0% | no | "e4a53e9a8ba0a587ae382a50355d14d7" / Fri, 14 Aug 2026 19 |
| The latest security news for developers - The GitHub Blog | 200 | no | rss | yes | application/rss+xml; charset=UTF-8 | 174.9 KB (small) | 46.5 KB | gzip | 0.19 | 0.002 | standard | yes | 10 | 0 | 0 | 10 | 0 | 0 | 2.7 | 0.0% | 0.0% | no | W/"0ffc969d63a81f91449cbbdf2490f590" / Fri, 14 Aug 2026 23 |
| Latest publications of type Threat Intelligence | 200 | no | rss | yes | text/xml; charset=utf-8 | 6.7 KB (small) | 6.7 KB |   | 0.26 | 0.000 | event-driven | yes | 10 | 0 | 0 | 10 | 0 | 0 | 12.7 | 0.0% | 0.0% | no |   /   |
| Blog | 200 | no | rss | yes | application/rss+xml;charset=utf-8 | 5.1 KB (small) | 1.5 KB | gzip | 0.35 | 0.001 | standard | yes | 10 | 0 | 0 | 10 | 0 | 0 | 5.2 | 0.0% | 0.0% | no | "1497-65926704e6e35-gzip" / Sun, 16 Aug 2026 09 |
| Open Source Security Foundation | 200 | no | rss | yes | application/rss+xml; charset=UTF-8 | 218.8 KB (small) | 218.8 KB |   | 0.19 | 0.003 | event-driven | yes | 10 | 0 | 0 | 10 | 0 | 0 | 1.7 | 0.0% | 0.0% | no | "6f40e5147e2f3af6911d158a3158edba" / Fri, 14 Aug 2026 17 |

## Cross-run drift review

No prior per-feed snapshot was available; this run establishes the baseline for the next maintenance check.

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
- **ECB \| US dollar (USD) - Euro foreign exchange reference rates** — body 7.1 KB; wire 1.2 KB; encoding `gzip`; fetch 2.88s; class `small`; cached 304 `False`.
- **All CISA Advisories** — body 496.4 KB; wire 59.5 KB; encoding `gzip`; fetch 0.21s; class `review`; cached 304 `False`.
- **Microsoft Security Blog** — body 304.1 KB; wire 78.9 KB; encoding `gzip`; fetch 0.27s; class `review`; cached 304 `False`.

## Device budget

Configured limits: 50 feeds, 4.00 MB total full-body payload, 600.0 KB per feed, 6 mobile-review feeds and 4 interrupting notification feeds.
The profile is within all declared device limits in this audit.

## Coverage audit

- **Finance**: US, UK, Irish, euro-area and global market context; SEC, CFTC, Federal Reserve speeches and monetary policy, ECB press, market operations and statistical releases, Central Bank of Ireland, EBA, AMLA, ESRB, Bank of England, HM Treasury, FCA, Eurostat, ONS, BIS and European Commission sanctions guidance; Nasdaq trade halts and Equity Trader Alerts; EUR/USD and EUR/GBP reference data. BEA was tested but rejected for one malformed historical item link.
- **Cyber**: Ireland NCSC, CISA, CISA ICS, CERT-EU, UK NCSC, CERT/CC, NIST, Microsoft, Mandiant, Unit 42, GitHub Security Blog, Cisco PSIRT, Cisco Talos, OpenSSF and CrowdStrike, plus independent incident reporting and technical research.
- **Ireland/EU/UK/US scope**: present in official alerts, regulation, macro data and market coverage.
- **Coverage-gap decisions**: see [Coverage-Gap-Assessment.md](Coverage-Gap-Assessment.md) for tested candidates, exact rejection reasons and next-addition triggers.

## Notification recommendation

**On:** Nasdaq Trade Halts, Ireland NCSC Alerts, CISA All Advisories and CERT-EU Security Advisories.

**Optional:** Central Bank of Ireland News, Federal Reserve Monetary Policy, ECB Press, Bank of England News, EBA News, AMLA News & Press, ESRB Press, UK NCSC All Updates, CISA ICS Advisories and Cisco PSIRT.

**Off and summarize in batches:** commercial market news, RTÉ/BBC business news, CFTC regulatory releases, ECB market operations and statistical releases, Eurostat/ONS/BIS data, EBA/AMLA/ESRB context, European Commission sanctions guidance, Federal Reserve speeches, Bank of England Publications, CERT/CC vulnerability notes, incident reporting, research feeds including GitHub Security Blog, exchange-rate data and broad regulatory context.

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

Full per-feed JSON: [report.json](report.json)
