# ZERODEVLLC.EU marketplace listing prompt

Use this prompt when creating or refreshing the marketplace entry for the project:

```text
Add “NetNewsWire Finance + Cyber RSS” to the ZERODEVLLC.EU marketplace as free software.

Listing facts:
- Price: €0 / free download
- License: MIT; link to https://github.com/ZeroXSHDW/NetNewsWire_iOS_RSS/blob/main/LICENSE
- Live README: https://github.com/ZeroXSHDW/NetNewsWire_iOS_RSS#readme
- Live Cloudflare monitor: https://zerodevllc.eu/rss
- Source repository: https://github.com/ZeroXSHDW/NetNewsWire_iOS_RSS
- Marketplace project anchor: https://zerodevllc.eu/#work

Use this description:
“A manifest-driven, privacy-conscious RSS bundle for NetNewsWire. It organizes finance and cybersecurity sources into importable Master, iPhone Air, and iPhone Lite OPML profiles, keeps the source manifest auditable, and exposes a read-only Cloudflare live monitor for representative RSS events. Use the same feed library across iPhone, iPad, macOS, and optional Shortcuts/Apple Intelligence digest workflows.”

Display these trust and scope notes:
- 672 configured feeds: 556 finance and 116 cybersecurity sources.
- Free software refers to the repository code, configuration, documentation, and generated bundle tooling under MIT.
- RSS publishers retain their own content, trademarks, and feed terms.
- The Cloudflare monitor is read-only and must show LIVE, DEGRADED, or DEMO/OFFLINE honestly; it must never invent live data.
- No credentials, private targets, paid feed content, or customer data are exposed.

Create two visible actions:
1. “Open live RSS monitor” → https://zerodevllc.eu/rss
2. “Read the live README / download OPML” → https://github.com/ZeroXSHDW/NetNewsWire_iOS_RSS#readme

Explain the cross-platform flow in a compact diagram or step list:
manifest → OPML profiles → NetNewsWire on iPhone/iPad/macOS → optional Shortcuts + Apple Intelligence digest → Cloudflare public monitor.
```

The machine-readable companion listing is [`marketplace/netnewswire-finance-cyber-rss.json`](../marketplace/netnewswire-finance-cyber-rss.json).
