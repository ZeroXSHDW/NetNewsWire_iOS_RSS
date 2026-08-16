# NetNewsWire Finance + Cyber subscriptions

This repository contains a manifest-driven Finance and Cyber Security RSS bundle for NetNewsWire, focused on Ireland, the EU, the UK and the US.

## Requirements

The offline checks require Python 3.11 or 3.12, `make` and zsh. Live validation additionally requires `curl` and `xmllint`. The project uses only Python standard-library modules; local cache, digest state, lock files and generated temporary files are ignored by Git.

## Profiles

- `NetNewsWire-Finance-Cyber.opml` — 62-feed master bundle.
- `NetNewsWire-Finance-Cyber-iPhone-Air.opml` — 50-feed recommended daily iPhone Air bundle, kept within an explicit 4 MB full-body refresh budget.
- `NetNewsWire-Finance-Cyber-iPhone-Lite.opml` — 39-feed lowest-burden fallback bundle.
- `feed-manifest.json` — the source of truth for titles, folders, URLs, metadata, notification recommendations, freshness policy and manifest-defined profiles.

The manifest is the editable source. OPML bundles, source tables, the notification matrix and the AirDrop copy are generated artifacts; regenerate them together after changing the manifest.

## AirDrop handoff

The ready-to-send package is in [AirDrop](AirDrop/). Send [NetNewsWire-Finance-Cyber-iPhone-Air.opml](AirDrop/NetNewsWire-Finance-Cyber-iPhone-Air.opml) to the iPhone and open it with NetNewsWire. It is the recommended 50-feed profile; the folder contains no caches, reports or development files. Run `make package` after changing the manifest to refresh the handoff copy.

Regenerate the OPML and source tables after changing the manifest:

```sh
make generate
make lint
```

The OPML does not reliably carry NetNewsWire notification settings. Use the notification column in the generated source table and the post-import checklist in [NetNewsWire-Setup-and-Notification-Plan.md](NetNewsWire-Setup-and-Notification-Plan.md).
Import one profile at a time: NetNewsWire adds OPML subscriptions to the current account, so remove or separate an older copy before importing if you are replacing it.
The generated [notification/profile matrix](NetNewsWire-Notification-Profile.md) is the quickest per-feed checklist; its JSON companion is [NetNewsWire-Notification-Profile.json](NetNewsWire-Notification-Profile.json).
The `eventDriven` attribute is validator metadata, not a required NetNewsWire feature; if the app re-exports OPML and drops custom attributes, regenerate the bundle from the manifest.

NetNewsWire supplies the feeds, background refresh, notifications, Smart Feeds and sharing; Apple Intelligence summaries are a separate iPhone Shortcuts layer. The Shortcut receives selected article text/links or a prepared JSON/plain-text digest handoff, then uses Apple Intelligence’s `Use Model` action and saves the digest to Notes. The setup plan documents the three suggested Dublin-time runs and the limitation that NetNewsWire has no documented direct “export all unread items to Shortcuts” action; for a direct iPhone run, select articles in Today/All Unread and share them to the Shortcut.
See [NetNewsWire-Feature-and-Automation-Matrix.md](NetNewsWire-Feature-and-Automation-Matrix.md) for the feature map, notification policy and exact Shortcut sequence.

## Validation

Run deterministic checks and then the live endpoint audit:

```sh
make check
make validate
make validate-lite
make validate-air
```

The validator checks HTTPS transport and redirects, HTTP status, XML roots, MIME safety, every item title/date/link, event-driven stale-review deadlines, manifest/OPML/source-table metadata alignment, duplicate/noise rates and compressed/wire versus full-body mobile telemetry.

`make lint` validates manifest invariants and byte-compares every committed OPML, source table and notification matrix against freshly generated artifacts. `make check` runs generation, linting, Python compilation, deterministic tests and zsh syntax validation together.

Each live run also maintains an ignored `.validation-history.json` file. It records the last 20 runs per profile, stores the latest per-feed baseline and reports cross-run drift such as title/root changes, item-count collapse, payload growth, freshness regression, new legacy/missing item links or a newly noisy feed. It also reports when the same profile has failed three consecutive checks.
The scheduled GitHub Actions workflow persists the feed cache and this baseline between runs, so monthly automation can detect drift rather than starting from an empty history.

The live reports are generated as [Markdown](NetNewsWire-Finance-Cyber-VALIDATION-REPORT.md) and [JSON](NetNewsWire-Finance-Cyber-VALIDATION-REPORT.json), with matching reports for the Lite and Air profiles. They are tracked Dublin-time snapshots locally and CI also uploads each run as an artifact; paths inside the reports are repository-relative so the files remain portable across machines. A healthy run has no failed feeds, metadata mismatches, noisy feeds, future-dated items or stale-review deadlines due; device profiles must also remain inside their declared budget.

`make check` is the offline pre-commit gate: it regenerates artifacts, validates the manifest, compiles Python, runs the test suite and checks the zsh validator syntax. Live validation reads all thresholds and feed-specific policies from `feed-manifest.json`, uses a bounded conditional-request cache, and serializes concurrent runs. Digest state and validation history use atomic writes plus local advisory locks; a terminated process releases the lock automatically, while the lock metadata can be inspected if a run is unexpectedly contended.

## Daily digest preparation

Export selected NetNewsWire articles as a JSON array (or JSON lines) with at least `title` and `link`, then run:

```sh
python3 prepare-rss-digest-input.py \
  --input selected-articles.json \
  --output digest-input.json \
  --shortcut-output shortcut-digest.txt \
  --profile iphone-air \
  --state .digest-state.json
```

The tool canonicalizes links, removes already processed items, sanitizes HTML article text, enriches recognized feed names/URLs with manifest section, folder, signal and notification metadata, and marks unmatched or ambiguous sources. It assigns conservative duplicate-story groups within a three-day publication window before sorting by publication time and maintaining a bounded local state file. `--profile iphone-air` filters to Air feeds and applies the Air handoff budget of 30 items, 6,000 characters per item and 90,000 text characters per package; Lite uses 24 items, 5,000 per item and 75,000 total. `--shortcut-output` also writes a compact link-preserving text handoff for a Shortcut or clipboard. Without `--profile`, the existing 100-item/180,000-character defaults remain available; explicit budget flags override a profile. State records the last run for audit purposes, but it never silently advances a publication cursor: use an explicit `--since` when a time lower bound is intended. Feed the resulting `digest-input.json` or `shortcut-digest.txt` to [Apple-Intelligence-RSS-Summary-Prompt.md](Apple-Intelligence-RSS-Summary-Prompt.md). Use `--dry-run` to inspect input without advancing state.

For the iPhone Air, keep NetNewsWire on the Air OPML, use the four interrupting alert feeds only, and process all other feeds through the selected-article digest. Use Lite when travelling or on a constrained connection; use Master only for a deliberate research pass.

## Publishing to GitHub

The repository has a reproducible release gate and a GitHub Actions workflow. See [GITHUB-PUBLISHING.md](GITHUB-PUBLISHING.md) for the release goal, a reusable publishing prompt and the safe publishing sequence. See [CONTRIBUTING.md](CONTRIBUTING.md) for feed and artifact change rules.

Choose a license before public publication; this project intentionally does not assume one on the owner’s behalf.

## Maintenance

Run the live audit monthly or after a source reports a failed refresh. Keep the manifest, generated artifacts, validation report and changelog together. Coverage additions still require a documented gap, a direct validated HTTPS RSS/Atom endpoint and a clear marginal-value case; a larger feed count is not a success by itself.
