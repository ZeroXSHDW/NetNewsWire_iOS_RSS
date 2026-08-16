# Generated artifacts

Everything in this directory is generated from [`../feed-manifest.json`](../feed-manifest.json) or refreshed by live validation. Edit the manifest or the generator scripts, then run `make package` or `make check`; do not hand-edit the generated files.

| Folder | Contents |
| --- | --- |
| [`opml/`](opml/) | Master, iPhone Air and iPhone Lite subscription files for NetNewsWire |
| [`sources/`](sources/) | Manifest-backed source tables with URLs, purpose, cadence and notification policy |
| [`notifications/`](notifications/) | Machine-readable and human-readable notification/profile matrix |
| [`validation/`](validation/) | Committed live validation reports and JSON details |
| [`AirDrop/`](AirDrop/) | Ready-to-send iPhone Air handoff |

The root README is the public starting point. This folder is the reproducible delivery layer behind its download links.
