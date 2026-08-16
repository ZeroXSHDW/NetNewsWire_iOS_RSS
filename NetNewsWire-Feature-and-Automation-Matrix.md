# NetNewsWire feature and Apple Intelligence automation matrix

Checked: 16 August 2026 (Europe/Dublin)

## What the iPhone stack can do

| Capability | NetNewsWire | Apple Intelligence / Shortcuts | Recommended use |
|---|---|---|---|
| Import subscriptions | OPML import/export | Not needed | Import the 50-feed iPhone Air OPML as the default; keep Lite for constrained connections and Master for deep research. |
| Refresh feeds | Direct downloading and iOS Background App Refresh | A time-of-day automation can run a Shortcut | Let NetNewsWire refresh feeds; do not treat a Shortcut timer as proof that NetNewsWire has refreshed. |
| Read triage | Today, All Unread, Starred, folders, search, Reader View | Receive selected article text/links from the Share Sheet | Select only the items that deserve a digest. |
| Urgent alerts | Per-feed notifications and badges | Optional notification or Note output | Enable notifications only for the four official alert feeds listed below. |
| Share article | Share Sheet to other apps | Shortcut can receive shared input | Use this as the privacy-first digest path. |
| AI summary | No documented native Apple Intelligence digest action | `Use Model` can summarize supplied text and pass the result to later actions; Apple provides On-Device, Private Cloud Compute and Extension Model choices | Summarize source material supplied by the user or a prepared export; do not ask the model to invent live news. |
| Profile-aware digest handoff | No direct bulk unread export to Shortcuts | `prepare-rss-digest-input.py --profile iphone-air` filters recognized Air feeds and can write compact `shortcut-digest.txt` text | Use the 30-item/90,000-character Air budget before passing material to Apple Intelligence. |
| Scheduled digest | No documented bulk unread export to Shortcuts | Personal automations can trigger at a time of day | A scheduled Shortcut needs a real input source. A timer alone cannot read NetNewsWire’s unread database. |
| Live prices and execution | Not provided by RSS | Not provided by a supplied-text summary | Use a broker or market-data terminal for quotes, order books, positions and execution. |

Official references: [NetNewsWire iOS help](https://netnewswire.com/help/ios/6.0/en/), [NetNewsWire OPML import](https://netnewswire.com/help/ios/6.1/en/import-opml.html), [NetNewsWire notifications](https://netnewswire.com/help/ios/6.1/en/notifications.html), [Apple Intelligence in Shortcuts](https://support.apple.com/guide/iphone/use-apple-intelligence-in-shortcuts-iph78c41eaf8/26/ios/26), and [Apple personal automations](https://support.apple.com/guide/shortcuts/intro-to-personal-automation-apd690170742/9.0/ios/26).

## Recommended profiles

### iPhone Air: 50 feeds

Use this as the default profile. It inherits the Lite alert and triage core, then adds one strong market source, Ireland/EU/global data, UK conduct coverage and compact supply-chain/threat-intelligence research. It is capped at 50 feeds, 4 MB of full feed bodies, 600 KB per feed and six mobile-review feeds; the four urgent alert feeds remain the only default notifications.

### iPhone-lite: 39 feeds

Use this when travelling or when refresh cost matters more than context breadth. It includes Ireland, EU, UK and US official alerts, selected market coverage, CFTC enforcement, CyberScoop and a small technical-research layer. Keep all feeds in Optional folders notification-off unless a topic is actively relevant.

### Master: 62 feeds

Use this when doing a deeper research pass. It adds commercial market coverage, specialist EU/French sources, vendor research, industrial-control advisories, AWS security bulletins, additional macro context and Schneier on Security. It is not the best default notification profile.

## Notification policy

Enable **On** only for:

- Nasdaq Trader — Trade Halts
- Ireland NCSC — Alerts & Advisories
- CISA — All Advisories
- CERT-EU — Security Advisories

Consider **Optional** for Federal Reserve Monetary Policy, ECB Press, Central Bank of Ireland News, Bank of England News, NCSC UK News/All Updates, CISA ICS Advisories, SANS Internet Storm Center, Cisco PSIRT and CFTC Enforcement. Leave everything else off and summarize it in batches.

## Shortcut specification

Create a Shortcut called `Daily Finance + Cyber Digest` with this sequence:

1. In Shortcut Details, enable **Show in Share Sheet** and accept text, URLs or article input.
2. Receive the Share Sheet input; if there is no input, show `Open NetNewsWire, select the relevant unread items, and share them here.` and stop.
3. Extract or preserve the supplied title, publisher, publication time, article link and article text/summary. For `shortcut-digest.txt`, pass the text directly; for JSON, read the file as text first.
4. Add the contents of `Apple-Intelligence-RSS-Summary-Prompt.md`, including the Europe/Dublin timezone and the requirement to separate confirmed facts from speculation.
5. Use the **Use Model** action. Choose **On-Device** for short batches, **Private Cloud Compute** for larger supplied batches when available, or **Extension Model** (ChatGPT) only when the user deliberately chooses it.
6. Show the digest, then save it to an Apple Note named `Finance + Cyber Digest — YYYY-MM-DD`.
7. Keep the source links in the saved output. Do not delete the source articles or mark them read automatically until the user has reviewed the digest.

## Suggested time windows

Create optional personal automations at:

- 07:30 — morning scan
- 12:30 — midday update
- 17:30 — end-of-day scan

These are suggested Dublin-time windows, not pre-created automations. With the current documented NetNewsWire feature set, the reliable privacy-first sequence is: open NetNewsWire → filter Today/All Unread → select relevant articles → Share → run the Shortcut. A fully unattended workflow requires a separate prepared RSS/JSON fetcher or service to supply the Shortcut input.

## Safety and quality controls

- RSS publication time is not automatically event time.
- Never infer exploitation, attribution, market impact or a trading opportunity from a headline.
- Never convert the digest into buy/sell advice, a price target, an execution command or an incident-response command.
- Verify urgent claims against official advisories, exchange notices, regulator releases or primary technical research.
- Keep the source link beside every material claim.
- If the supplied batch is empty, report `no material change` rather than searching for filler.
