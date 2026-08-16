# NetNewsWire Finance + Cyber RSS

[![Validate RSS bundles](https://github.com/ZeroXSHDW/NetNewsWire_iOS_RSS/actions/workflows/rss-validation.yml/badge.svg)](https://github.com/ZeroXSHDW/NetNewsWire_iOS_RSS/actions/workflows/rss-validation.yml)

A manifest-driven, privacy-conscious RSS workflow for **NetNewsWire on iPhone**. It combines Ireland, EU, UK and US finance sources with official cybersecurity alerts, incident reporting and technical research—and adds an optional Apple Intelligence digest layer for articles you deliberately provide.

> **The short version:** NetNewsWire collects and organizes the feeds. The manifest defines what belongs in each profile. Apple Intelligence summarizes only the selected, prepared article text; it does not fetch news, trade, or make decisions for you.
>
> This repository is **not a standalone iOS app**. It is a ready-to-import OPML/feed bundle plus optional Shortcuts and Apple Intelligence instructions.

## At a glance

| Profile | Feeds | Best for | Download |
| --- | ---: | --- | --- |
| **iPhone Air** | 50 | Recommended daily profile with broad coverage and a 4 MB full-body budget | [Download for iPhone](artifacts/opml/NetNewsWire-Finance-Cyber-iPhone-Air.opml?raw=1) · [inspect OPML](artifacts/opml/NetNewsWire-Finance-Cyber-iPhone-Air.opml) · [source table](artifacts/sources/NetNewsWire-Finance-Cyber-iPhone-Air-Source-Table.md) |
| **iPhone Lite** | 39 | Lower-noise mobile reading and smaller refreshes | [Download for iPhone](artifacts/opml/NetNewsWire-Finance-Cyber-iPhone-Lite.opml?raw=1) · [inspect OPML](artifacts/opml/NetNewsWire-Finance-Cyber-iPhone-Lite.opml) · [source table](artifacts/sources/NetNewsWire-Finance-Cyber-iPhone-Lite-Source-Table.md) |
| **Master** | 62 | Full research coverage and rebuilding the other profiles | [Download for iPhone](artifacts/opml/NetNewsWire-Finance-Cyber.opml?raw=1) · [inspect OPML](artifacts/opml/NetNewsWire-Finance-Cyber.opml) · [source table](artifacts/sources/NetNewsWire-Finance-Cyber-Source-Table.md) |

The repository contains **34 finance feeds** and **28 cybersecurity feeds**. Four official alert feeds are configured for interrupting notifications; the remaining sources are intended for normal reading, optional notifications or digest review.

## What you need

| App or tool | Needed? | What it does |
| --- | --- | --- |
| **NetNewsWire for iOS** | Required | Imports the OPML bundle, refreshes feeds, organizes folders, sends selected notifications and shares articles. |
| **Apple Shortcuts** | Optional | Receives selected articles from NetNewsWire and passes them to the digest workflow. |
| **Apple Intelligence** | Optional | Runs the Shortcuts **Use Model** step on supplied article text; it is not required for reading RSS. |
| **Apple Notes** | Optional | Stores a dated copy of the reviewed digest. |
| **Mac + Python 3.11/3.12, `make` and zsh** | Maintainer only | Regenerates bundles, prepares digest input and runs offline checks. |
| **`curl` + `xmllint` (libxml2)** | Live validation only | Fetches direct feed endpoints and verifies their XML. |

You can use the project with **NetNewsWire alone**. Add Shortcuts, Apple Intelligence and Notes only if you want the optional digest workflow.

## Install directly from this GitHub page

If you are reading this README on your iPhone, you do not need a Mac or AirDrop:

1. Install [NetNewsWire for iPhone and iPad](https://netnewswire.com/) if it is not already installed.
2. Tap [Download the recommended iPhone Air profile](artifacts/opml/NetNewsWire-Finance-Cyber-iPhone-Air.opml?raw=1). Use [iPhone Lite](artifacts/opml/NetNewsWire-Finance-Cyber-iPhone-Lite.opml?raw=1) for a smaller bundle, or [Master](artifacts/opml/NetNewsWire-Finance-Cyber.opml?raw=1) for all feeds.
3. If Safari shows the OPML text, tap **Share → Save to Files**. If it downloads automatically, find it in **Files → Downloads**. Keep the `.opml` extension.
4. In NetNewsWire, open **Feeds → Settings → Import Subscriptions**, choose the downloaded file, and select the account that should receive the feeds.
5. Refresh once and confirm the **Finance** and **Cyber Security** folders. Import only one profile: OPML imports are additive and can duplicate an older copy.

For the official explanation of this import flow, see [NetNewsWire’s OPML instructions](https://netnewswire.com/help/ios/6.1/en/import-opml.html).

## Choose your path

| If you want to… | Use this |
| --- | --- |
| Read the recommended daily mix | NetNewsWire + **iPhone Air** OPML |
| Reduce refresh cost while travelling | NetNewsWire + **iPhone Lite** OPML |
| Search or research every configured source | NetNewsWire + **Master** OPML |
| Create a reviewed daily digest | NetNewsWire + Shortcuts + optional Apple Intelligence |
| Maintain or publish the project | Mac toolchain + `feed-manifest.json` + GitHub Actions |

## What this project does

- Keeps the feed inventory, folders, profile membership and notification policy in [`feed-manifest.json`](feed-manifest.json).
- Generates importable OPML files and human-readable source tables from that manifest.
- Provides iPhone Air and iPhone Lite bundles so the phone gets useful signal without importing every research feed.
- Prepares selected RSS articles for a repeatable Apple Intelligence workflow with deduplication, sanitization, time handling and size limits.
- Validates feed URLs, metadata, profile budgets and generated artifacts in CI.

The generated files are delivery artifacts. Edit the manifest first, then run `make generate` or `make package` to rebuild them.

```mermaid
flowchart LR
    MANIFEST["feed-manifest.json\nsource of truth"] --> GENERATE["generate-bundle.py"]
    GENERATE --> BUNDLES["Master / Air / Lite OPML"]
    BUNDLES --> NNW["NetNewsWire for iOS\nread · refresh · notify"]
    NNW --> SHARE["Share selected articles"]
    SHARE --> SHORTCUT["Apple Shortcuts\noptional"]
    SHORTCUT --> MODEL["Apple Intelligence\noptional Use Model"]
    MODEL --> NOTES["Apple Notes\noptional reviewed digest"]
    GENERATE --> CHECKS["make check + GitHub Actions"]
```

## What the result looks like

These repository-authored previews make the deliverable visible before you import anything. They use the current iPhone Air folders, alert policy and Apple Intelligence handoff described by the manifest; they are interface illustrations, not screenshots or NetNewsWire source code.

![NetNewsWire iPhone Air feed view preview](docs/previews/netnewswire-feed-preview.svg)

*NetNewsWire result: organized Finance and Cyber Security folders, four interrupting alert feeds, and quieter sources available for reading or digest review.*

![Apple Intelligence RSS digest preview](docs/previews/apple-intelligence-preview.svg)

*Apple Intelligence result: selected evidence passes through Shortcuts, then becomes a reviewed digest with provenance, uncertainty labels and no action recommendation.*

## Feed coverage

### Finance — 34 feeds

| Group | Count | Coverage |
| --- | ---: | --- |
| Market & Trading | 8 | Trade halts, trader alerts, business headlines and market reporting |
| Official & Macro | 13 | Central banks, regulators, monetary policy, enforcement and market operations |
| Data, Ireland, EU & UK | 7 | Reference rates, statistical releases, sanctions guidance and release calendars |
| Global Data & Research | 3 | BIS and Bank of England research and releases |
| UK Regulation & Warnings | 3 | FCA news, scam warnings and OFSI sanctions updates |

### Cyber Security — 28 feeds

| Group | Count | Coverage |
| --- | ---: | --- |
| Ireland, EU & official alerts | 6 | Ireland NCSC, CISA, CERT-EU, CERT-FR and NCSC UK alerts |
| News & incident reporting | 6 | BleepingComputer, Dark Reading, Krebs, CyberScoop, SecurityWeek and The Record |
| Technical research | 7 | SANS ISC, CERT/CC, NIST, Mandiant, Microsoft, Unit 42 and GitHub Security |
| Specialist alerts & research | 9 | ICS, cloud, PSIRT, supply-chain, threat-intelligence and vendor research |

### Profile coverage matrix

Master includes every feed. Air and Lite are curated subsets of the same manifest:

| Feed group | Master | iPhone Air | iPhone Lite |
| --- | ---: | ---: | ---: |
| Finance — Market & Trading | 8 | 6 | 5 |
| Finance — Official & Macro | 13 | 13 | 13 |
| Finance — Data, Ireland, EU & UK | 7 | 7 | 3 |
| Finance — Global Data & Research | 3 | 2 | 0 |
| Finance — UK Regulation & Warnings | 3 | 3 | 2 |
| Cyber — Ireland, EU & Official Alerts | 6 | 6 | 6 |
| Cyber — News & Incident Reporting | 6 | 4 | 4 |
| Cyber — Technical Research | 7 | 6 | 6 |
| Cyber — Specialist Alerts & Research | 9 | 3 | 0 |
| **Total** | **62** | **50** | **39** |

<details>
<summary>Show all 62 feed names</summary>

#### Finance

**Market & Trading**

- Nasdaq Trader — Trade Halts
- Nasdaq Trader — Equity Trader Alerts
- BBC — Business
- Bloomberg — Markets
- Financial Times — Markets
- MarketWatch — Top Stories
- RTÉ — Business
- The Wall Street Journal — Markets

**Official & Macro**

- Central Bank of Ireland — News
- European Central Bank — Press
- European Banking Authority — News
- European Systemic Risk Board — Press
- AMLA — News & Press
- Bank of England — News
- HM Treasury — News & Communications
- Federal Reserve — Monetary Policy
- SEC — Press Releases
- CFTC — General Press Releases
- CFTC — Enforcement
- ECB — Market Operations
- Federal Reserve — Speeches

**Data, Ireland, EU & UK**

- ECB — USD Reference Rate
- ECB — GBP Reference Rate
- ECB — Statistical Releases
- Central Bank of Ireland — Markets Update
- Eurostat — Economy & Finance Releases
- European Commission — Sanctions Guidance
- UK ONS — Release Calendar

**Global Data & Research**

- BIS — Statistical Releases
- BIS — Press Releases
- Bank of England — Publications

**UK Regulation & Warnings**

- FCA — News
- FCA — Scam Warnings
- OFSI — Financial Sanctions Blog

#### Cyber Security

**Ireland, EU & Official Alerts**

- Ireland NCSC — Alerts & Advisories
- CISA — All Advisories
- CERT-EU — Security Advisories
- CERT-FR — Security Alerts (French)
- NCSC UK — News
- NCSC UK — All Updates

**News & Incident Reporting**

- BleepingComputer
- Dark Reading
- Krebs on Security
- CyberScoop
- SecurityWeek
- The Record — Cybersecurity News

**Technical Research**

- SANS Internet Storm Center
- CERT/CC — Vulnerability Notes
- NIST — Cybersecurity Insights
- Google Threat Intelligence — Mandiant
- Microsoft Security Blog
- Unit 42 — Threat Research
- GitHub Security Blog

**Specialist Alerts & Research**

- CISA — ICS Advisories
- AWS Security Bulletins
- CERT-EU — Threat Intelligence
- CERT-FR — Security Advisories (French)
- Cisco PSIRT — Security Advisories
- Schneier on Security
- Cisco Talos
- CrowdStrike — Cybersecurity Research
- OpenSSF — Supply Chain Security

</details>

<details>
<summary>Show profile membership and notification policy for every feed</summary>

The **Master** profile contains every feed. `Yes` means the feed is included in the selected iPhone profile; `—` means it stays in Master only.

#### Finance

##### 01 — Core — Market & Trading

| Feed | Air | Lite | Notifications |
| --- | :---: | :---: | --- |
| Nasdaq Trader — Trade Halts | Yes | Yes | On |
| Nasdaq Trader — Equity Trader Alerts | Yes | Yes | Off · digest |
| BBC — Business | Yes | Yes | Off · digest |
| Bloomberg — Markets | Yes | — | Off · digest |
| Financial Times — Markets | Yes | Yes | Off · digest |
| MarketWatch — Top Stories | — | — | Off · digest |
| RTÉ — Business | Yes | Yes | Off · digest |
| The Wall Street Journal — Markets | — | — | Off · digest |

##### 02 — Core — Official & Macro

| Feed | Air | Lite | Notifications |
| --- | :---: | :---: | --- |
| Central Bank of Ireland — News | Yes | Yes | Optional |
| European Central Bank — Press | Yes | Yes | Optional |
| European Banking Authority — News | Yes | Yes | Off · digest |
| European Systemic Risk Board — Press | Yes | Yes | Off · digest |
| AMLA — News & Press | Yes | Yes | Off · digest |
| Bank of England — News | Yes | Yes | Optional |
| HM Treasury — News & Communications | Yes | Yes | Off · digest |
| Federal Reserve — Monetary Policy | Yes | Yes | Optional |
| SEC — Press Releases | Yes | Yes | Optional |
| CFTC — General Press Releases | Yes | Yes | Off · digest |
| CFTC — Enforcement | Yes | Yes | Optional |
| ECB — Market Operations | Yes | Yes | Off · digest |
| Federal Reserve — Speeches | Yes | Yes | Off · digest |

##### 03 — Optional — Data, Ireland, EU & UK

| Feed | Air | Lite | Notifications |
| --- | :---: | :---: | --- |
| ECB — USD Reference Rate | Yes | Yes | Off · digest |
| ECB — GBP Reference Rate | Yes | Yes | Off · digest |
| ECB — Statistical Releases | Yes | — | Off · digest |
| Central Bank of Ireland — Markets Update | Yes | — | Off · digest |
| Eurostat — Economy & Finance Releases | Yes | — | Off · digest |
| European Commission — Sanctions Guidance | Yes | — | Off · digest |
| UK ONS — Release Calendar | Yes | Yes | Off · digest |

##### 04 — Optional — Global Data & Research

| Feed | Air | Lite | Notifications |
| --- | :---: | :---: | --- |
| BIS — Statistical Releases | Yes | — | Off · digest |
| BIS — Press Releases | — | — | Off · digest |
| Bank of England — Publications | Yes | — | Off · digest |

##### 05 — Optional — UK Regulation & Warnings

| Feed | Air | Lite | Notifications |
| --- | :---: | :---: | --- |
| FCA — News | Yes | — | Off · digest |
| FCA — Scam Warnings | Yes | Yes | Off · digest |
| OFSI — Financial Sanctions Blog | Yes | Yes | Off · digest |

#### Cyber Security

##### 01 — Core — Ireland, EU & Official Alerts

| Feed | Air | Lite | Notifications |
| --- | :---: | :---: | --- |
| Ireland NCSC — Alerts & Advisories | Yes | Yes | On |
| CISA — All Advisories | Yes | Yes | On |
| CERT-EU — Security Advisories | Yes | Yes | On |
| CERT-FR — Security Alerts (French) | Yes | Yes | Optional · French |
| NCSC UK — News | Yes | Yes | Optional |
| NCSC UK — All Updates | Yes | Yes | Optional |

##### 02 — Core — News & Incident Reporting

| Feed | Air | Lite | Notifications |
| --- | :---: | :---: | --- |
| BleepingComputer | Yes | Yes | Off · digest |
| Dark Reading | — | — | Off · digest |
| Krebs on Security | Yes | Yes | Off · digest |
| CyberScoop | Yes | Yes | Off · digest |
| SecurityWeek | — | — | Off · digest |
| The Record — Cybersecurity News | Yes | Yes | Off · digest |

##### 03 — Core — Technical Research

| Feed | Air | Lite | Notifications |
| --- | :---: | :---: | --- |
| SANS Internet Storm Center | Yes | Yes | Optional |
| CERT/CC — Vulnerability Notes | Yes | Yes | Off · digest |
| NIST — Cybersecurity Insights | Yes | Yes | Off · digest |
| Google Threat Intelligence — Mandiant | — | — | Off · digest |
| Microsoft Security Blog | Yes | Yes | Off · digest |
| Unit 42 — Threat Research | Yes | Yes | Off · digest |
| GitHub Security Blog | Yes | Yes | Off · digest |

##### 04 — Optional — Specialist Alerts & Research

| Feed | Air | Lite | Notifications |
| --- | :---: | :---: | --- |
| CISA — ICS Advisories | — | — | Optional |
| AWS Security Bulletins | — | — | Optional |
| CERT-EU — Threat Intelligence | Yes | — | Off · digest |
| CERT-FR — Security Advisories (French) | — | — | Off · digest |
| Cisco PSIRT — Security Advisories | — | — | Optional |
| Schneier on Security | — | — | Off · digest |
| Cisco Talos | — | — | Off · digest |
| CrowdStrike — Cybersecurity Research | Yes | — | Off · digest |
| OpenSSF — Supply Chain Security | Yes | — | Off · digest |

</details>


The complete URL, folder, notification and profile metadata for every feed is in the generated [Master source table](artifacts/sources/NetNewsWire-Finance-Cyber-Source-Table.md). The [notification profile](artifacts/notifications/NetNewsWire-Notification-Profile.md) explains why a feed is interrupting, optional or quiet.

## Profiles and notification policy

- **iPhone Air** is the default: broad enough for daily finance and cyber awareness, while keeping full article bodies under a 4 MB profile budget.
- **iPhone Lite** is the smaller, lower-noise option for constrained mobile use.
- **Master** includes every feed and is useful for research, maintenance and rebuilding the derived profiles.

The four interrupting alert feeds are:

1. Ireland NCSC — Alerts & Advisories
2. CISA — All Advisories
3. CERT-EU — Security Advisories
4. Nasdaq Trader — Trade Halts

Other official sources can be enabled as optional notifications. News, research and duplicate-prone sources are intentionally quieter so the feed reader remains usable.

## Install from a Mac or with AirDrop

1. Run `make package` on the Mac, or use the committed **iPhone Air** handoff in [`artifacts/AirDrop/`](artifacts/AirDrop/).
2. AirDrop the selected `.opml` file to the iPhone, save it in Files, and follow the NetNewsWire import steps above.
3. Refresh once, then review the notification settings against [`NetNewsWire-Notification-Profile.md`](artifacts/notifications/NetNewsWire-Notification-Profile.md).

NetNewsWire remains the reading and collection layer. The bundle does not claim to provide live quotes, order books, positions, execution, incident-response commands or financial advice.

## How Apple Intelligence is used

Apple Intelligence is an **optional summarization step after collection**. It receives the article material that you selected in NetNewsWire—or the prepared JSON/text export created by this repository—and applies the fixed instructions in [`Apple-Intelligence-RSS-Summary-Prompt.md`](docs/Apple-Intelligence-RSS-Summary-Prompt.md).

```mermaid
flowchart LR
    NNW["NetNewsWire: Today / All Unread"] -->|Share selected articles| SC["Shortcut: Daily Finance + Cyber Digest"]
    JSON["Selected article JSON"] --> PREP["prepare-rss-digest-input.py"]
    PREP -->|digest-input.json or shortcut-digest.txt| SC
    PROMPT["Fixed RSS summary prompt"] --> MODEL["Shortcut: Use Model"]
    SC --> MODEL
    MODEL --> REVIEW["Review the digest"]
    REVIEW --> NOTE["Save a dated Apple Note"]
```

The workflow is deliberately bounded:

- **Input is explicit.** NetNewsWire does not silently hand over its entire unread database. Select Today, All Unread or individual articles and share them, or prepare a known JSON input file.
- **The preparation script is deterministic.** [`prepare-rss-digest-input.py`](prepare-rss-digest-input.py) canonicalizes fields, removes duplicate items, sanitizes article text, applies the chosen profile and enforces item/body/total-size budgets.
- **The model uses supplied evidence only.** The prompt tells Apple Intelligence not to browse, fill gaps, invent CVEs, prices, tickers, actors or impacts, or turn a headline into a confirmed event.
- **The output is a review aid.** The Shortcut shows the digest and can save `Finance + Cyber Digest — YYYY-MM-DD` to Apple Notes. It does not automatically mark articles read or recommend trades.
- **Model routing is intentional.** Use the on-device model for short/private batches, Private Cloud Compute for larger supported batches, or a ChatGPT extension only when deliberately selected in Shortcuts.

For the full Shortcut contract, scheduling limits and privacy/safety notes, see [`NetNewsWire-Daily-Digest-Workflow.md`](docs/NetNewsWire-Daily-Digest-Workflow.md) and [`NetNewsWire-Feature-and-Automation-Matrix.md`](docs/NetNewsWire-Feature-and-Automation-Matrix.md).

## Prepare a digest input

For a prepared article export, use the same profile you imported on the phone:

```bash
python3 prepare-rss-digest-input.py \
  --input selected-articles.json \
  --output digest-input.json \
  --shortcut-output shortcut-digest.txt \
  --profile iphone-air \
  --state .digest-state.json
```

The generated `shortcut-digest.txt` is convenient for a Shortcut text action. The JSON output is useful when you want to preserve structured fields such as publisher, publication time, link, summary and source metadata. The fixed prompt expects Dublin time for the daily view and clearly separates confirmed reporting from claims, speculation and missing context.

## Validate before sharing or publishing

```bash
make help           # show the project commands
make check          # offline generation, lint, docs, hygiene, tests and syntax checks
make hygiene        # scan tracked files for secrets, local paths and runtime state
make validate-all   # live validation for Master, iPhone Lite and iPhone Air
```

You can also run `make validate`, `make validate-lite` or `make validate-air` when you only need one profile.

Validation checks include:

- feed URLs, titles, folders, notification metadata and duplicate identities;
- generated OPML and source-table consistency;
- profile membership and full-body download budgets;
- redirect handling, XML validity, cache reuse and regression history;
- Python compilation, shell syntax and the repository test suite;
- tracked-file hygiene, including high-confidence credential, local-path and runtime-state checks.

Committed validation snapshots live under [`artifacts/validation/`](artifacts/validation/); the feed cache is kept outside the repository by default. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the maintainer workflow.

## Repository map

| Path | Purpose |
| --- | --- |
| [`feed-manifest.json`](feed-manifest.json) | Source of truth for feeds and profile policy |
| [`generate-bundle.py`](generate-bundle.py) | Generates OPML, source tables and notification metadata |
| [`validate-manifest.py`](validate-manifest.py) | Lints the manifest and generated artifacts |
| [`prepare-rss-digest-input.py`](prepare-rss-digest-input.py) | Prepares bounded article input for the Shortcut |
| [`validate-docs.py`](validate-docs.py) | Checks README links, feed names and profile counts against the manifest |
| [`check-repository-hygiene.py`](check-repository-hygiene.py) | Prevents tracked runtime state, credentials and machine-specific paths |
| [`docs/`](docs/) | Setup guides, Apple Intelligence instructions, research notes and visual previews |
| [`artifacts/`](artifacts/) | Generated OPML, source tables, notification matrix, reports and AirDrop handoff |
| [`examples/`](examples/) | Safe example input for digest preparation |
| [`artifacts/AirDrop/`](artifacts/AirDrop/) | Ready-to-send iPhone Air OPML and handoff notes |
| [Validation reports](artifacts/validation/NetNewsWire-Finance-Cyber-VALIDATION-REPORT.md) | Committed profile evidence and live-feed snapshots |
| [`NetNewsWire-Finance-Cyber-CHANGELOG.md`](NetNewsWire-Finance-Cyber-CHANGELOG.md) | Feed-selection, maintenance and validation history |
| [`.github/`](.github/) | CI, Dependabot, ownership and contribution workflows |
| [`.github/workflows/rss-validation.yml`](.github/workflows/rss-validation.yml) | Deterministic CI and scheduled live validation |
| [`SECURITY.md`](SECURITY.md) | Security reporting and sensitive-data handling |

## Publishing and maintenance

The repository is public at [github.com/ZeroXSHDW/NetNewsWire_iOS_RSS](https://github.com/ZeroXSHDW/NetNewsWire_iOS_RSS). The publishing checklist is in [`GITHUB-PUBLISHING.md`](GITHUB-PUBLISHING.md); contribution and feed-change rules are in [`CONTRIBUTING.md`](CONTRIBUTING.md).

No license file is included yet. Public visibility does not grant reuse rights; choose the intended license before calling this a finished public release.

When changing a feed, edit [`feed-manifest.json`](feed-manifest.json), regenerate the bundle, run the checks, inspect the generated diff and commit the source plus derived artifacts together.
