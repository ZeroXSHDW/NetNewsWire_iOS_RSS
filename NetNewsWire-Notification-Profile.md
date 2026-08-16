# NetNewsWire notification and profile matrix

Generated from `feed-manifest.json`; regenerate with `make generate` after manifest changes.

OPML imports carry the feed structure but do not reliably carry NetNewsWire notification settings. Apply the policy below manually after import.

## Profile summary

| Profile | Recommended | Feeds | On | Optional | Optional French | Off |
|---|---|---:|---:|---:|---:|---:|
| Master | No | 62 | 4 | 12 | 1 | 45 |
| iPhone Lite | No | 39 | 4 | 9 | 1 | 25 |
| iPhone Air | Yes | 50 | 4 | 9 | 1 | 36 |

## Policy meanings

| Policy | Meaning |
|---|---|
| On | Enable immediate notifications for urgent, high-signal alerts. |
| Optional | Keep off by default; enable when the topic is actively relevant. |
| Optional French | Same as Optional; translate/summarize in the daily digest when useful. |
| Off | Do not interrupt; include in the daily Apple Intelligence digest. |

## Per-feed matrix

| Section | Folder | Feed | Master | iPhone Lite | iPhone Air | Notification policy | Signal type |
|---|---|---|---|---|---|---|---|
| Finance | 01 — Core — Market & Trading | Nasdaq Trader — Trade Halts | Yes | Yes | Yes | **On** | alert |
| Finance | 01 — Core — Market & Trading | Nasdaq Trader — Equity Trader Alerts | Yes | Yes | Yes | Off; summarize | regulatory/event |
| Finance | 01 — Core — Market & Trading | BBC — Business | Yes | Yes | Yes | Off; summarize | context |
| Finance | 01 — Core — Market & Trading | Bloomberg — Markets | Yes | No | Yes | Off; summarize | market |
| Finance | 01 — Core — Market & Trading | Financial Times — Markets | Yes | Yes | Yes | Off; summarize | market/research |
| Finance | 01 — Core — Market & Trading | MarketWatch — Top Stories | Yes | No | No | Off; summarize | market |
| Finance | 01 — Core — Market & Trading | RTÉ — Business | Yes | Yes | Yes | Off; summarize | context |
| Finance | 01 — Core — Market & Trading | The Wall Street Journal — Markets | Yes | No | No | Off; summarize | market |
| Finance | 02 — Core — Official & Macro | Central Bank of Ireland — News | Yes | Yes | Yes | Optional on | policy/regulatory |
| Finance | 02 — Core — Official & Macro | European Central Bank — Press | Yes | Yes | Yes | Optional on | policy/event |
| Finance | 02 — Core — Official & Macro | European Banking Authority — News | Yes | Yes | Yes | Off; summarize | regulatory/policy |
| Finance | 02 — Core — Official & Macro | European Systemic Risk Board — Press | Yes | Yes | Yes | Off; summarize | macroprudential/research |
| Finance | 02 — Core — Official & Macro | AMLA — News & Press | Yes | Yes | Yes | Off; summarize | aml/enforcement/regulatory |
| Finance | 02 — Core — Official & Macro | Bank of England — News | Yes | Yes | Yes | Optional on | policy/event |
| Finance | 02 — Core — Official & Macro | HM Treasury — News & Communications | Yes | Yes | Yes | Off; summarize | policy/event |
| Finance | 02 — Core — Official & Macro | Federal Reserve — Monetary Policy | Yes | Yes | Yes | Optional on | policy/event |
| Finance | 02 — Core — Official & Macro | SEC — Press Releases | Yes | Yes | Yes | Optional on | regulatory/event |
| Finance | 02 — Core — Official & Macro | CFTC — General Press Releases | Yes | Yes | Yes | Off; summarize | regulatory/event |
| Finance | 02 — Core — Official & Macro | CFTC — Enforcement | Yes | Yes | Yes | Optional on | enforcement/regulatory |
| Finance | 02 — Core — Official & Macro | ECB — Market Operations | Yes | Yes | Yes | Off; summarize | market-data/event |
| Finance | 02 — Core — Official & Macro | Federal Reserve — Speeches | Yes | Yes | Yes | Off; summarize | policy/research |
| Finance | 03 — Optional — Data, Ireland, EU & UK | ECB — USD Reference Rate | Yes | Yes | Yes | Off; summarize | daily-data |
| Finance | 03 — Optional — Data, Ireland, EU & UK | ECB — GBP Reference Rate | Yes | Yes | Yes | Off; summarize | daily-data |
| Finance | 03 — Optional — Data, Ireland, EU & UK | ECB — Statistical Releases | Yes | No | Yes | Off; summarize | data/event |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Central Bank of Ireland — Markets Update | Yes | No | Yes | Off; summarize | regulatory/event |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Eurostat — Economy & Finance Releases | Yes | No | Yes | Off; summarize | data/event |
| Finance | 03 — Optional — Data, Ireland, EU & UK | European Commission — Sanctions Guidance | Yes | No | Yes | Off; summarize | regulatory/event |
| Finance | 03 — Optional — Data, Ireland, EU & UK | UK ONS — Release Calendar | Yes | Yes | Yes | Off; summarize | calendar/data |
| Finance | 04 — Optional — Global Data & Research | BIS — Statistical Releases | Yes | No | Yes | Off; summarize | data/research |
| Finance | 04 — Optional — Global Data & Research | BIS — Press Releases | Yes | No | No | Off; summarize | policy/research |
| Finance | 04 — Optional — Global Data & Research | Bank of England — Publications | Yes | No | Yes | Off; summarize | research |
| Finance | 05 — Optional — UK Regulation & Warnings | FCA — News | Yes | No | Yes | Off; summarize | regulatory/news |
| Finance | 05 — Optional — UK Regulation & Warnings | FCA — Scam Warnings | Yes | Yes | Yes | Off; summarize | regulatory/alert |
| Finance | 05 — Optional — UK Regulation & Warnings | OFSI — Financial Sanctions Blog | Yes | Yes | Yes | Off; summarize | sanctions/policy |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | Ireland NCSC — Alerts & Advisories | Yes | Yes | Yes | **On** | alert |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | CISA — All Advisories | Yes | Yes | Yes | **On** | advisory |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | CERT-EU — Security Advisories | Yes | Yes | Yes | **On** | advisory |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | CERT-FR — Security Alerts (French) | Yes | Yes | Yes | Optional on; French | alert/advisory |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | NCSC UK — News | Yes | Yes | Yes | Optional on | alert/news |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | NCSC UK — All Updates | Yes | Yes | Yes | Optional on | alert/context |
| Cyber Security | 02 — Core — News & Incident Reporting | BleepingComputer | Yes | Yes | Yes | Off; summarize | news |
| Cyber Security | 02 — Core — News & Incident Reporting | Dark Reading | Yes | No | No | Off; summarize | news |
| Cyber Security | 02 — Core — News & Incident Reporting | Krebs on Security | Yes | Yes | Yes | Off; summarize | news/research |
| Cyber Security | 02 — Core — News & Incident Reporting | CyberScoop | Yes | Yes | Yes | Off; summarize | news/policy |
| Cyber Security | 02 — Core — News & Incident Reporting | SecurityWeek | Yes | No | No | Off; summarize | news |
| Cyber Security | 02 — Core — News & Incident Reporting | The Record — Cybersecurity News | Yes | Yes | Yes | Off; summarize | news |
| Cyber Security | 03 — Core — Technical Research | SANS Internet Storm Center | Yes | Yes | Yes | Optional on | research/alert |
| Cyber Security | 03 — Core — Technical Research | CERT/CC — Vulnerability Notes | Yes | Yes | Yes | Off; summarize | advisory/research |
| Cyber Security | 03 — Core — Technical Research | NIST — Cybersecurity Insights | Yes | Yes | Yes | Off; summarize | research/guidance |
| Cyber Security | 03 — Core — Technical Research | Google Threat Intelligence — Mandiant | Yes | No | No | Off; summarize | research |
| Cyber Security | 03 — Core — Technical Research | Microsoft Security Blog | Yes | Yes | Yes | Off; summarize | research/advisory |
| Cyber Security | 03 — Core — Technical Research | Unit 42 — Threat Research | Yes | Yes | Yes | Off; summarize | research |
| Cyber Security | 03 — Core — Technical Research | GitHub Security Blog | Yes | Yes | Yes | Off; summarize | research/advisory |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | CISA — ICS Advisories | Yes | No | No | Optional on | advisory |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | AWS Security Bulletins | Yes | No | No | Optional on | advisory |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | CERT-EU — Threat Intelligence | Yes | No | Yes | Off; summarize | research |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | CERT-FR — Security Advisories (French) | Yes | No | No | Off; summarize | advisory |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | Cisco PSIRT — Security Advisories | Yes | No | No | Optional on | advisory |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | Schneier on Security | Yes | No | No | Off; summarize | research/context |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | Cisco Talos | Yes | No | No | Off; summarize | research |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | CrowdStrike — Cybersecurity Research | Yes | No | Yes | Off; summarize | research |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | OpenSSF — Supply Chain Security | Yes | No | Yes | Off; summarize | research/guidance |

## Import checklist

1. Import exactly one profile: the **iPhone Air** OPML as the default, the Lite OPML for constrained connections, or the **Master** OPML for full coverage.
2. NetNewsWire adds imported feeds to the current subscription list; remove or separate an older copy before importing if you are replacing a previous bundle.
3. Apply **On** only to the four urgent official alert feeds unless your operating needs justify more interruptions.
4. Review **Optional** feeds after import; leave them off during normal use.
5. Leave **Off** feeds notification-disabled and process them in the daily digest.
6. Re-check this matrix after any manifest change; the generated OPML and source tables should be regenerated together.

See [NetNewsWire setup and notification plan](NetNewsWire-Setup-and-Notification-Plan.md) for the operating rationale and [daily digest workflow](NetNewsWire-Daily-Digest-Workflow.md) for batch review.
