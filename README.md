# NetNewsWire Finance + Cyber subscriptions

This directory contains a manifest-driven Finance and Cyber Security RSS bundle for NetNewsWire, focused on Ireland, the EU, the UK and the US.

## Profiles

- `NetNewsWire-Finance-Cyber.opml` — 51-feed master bundle.
- `NetNewsWire-Finance-Cyber-iPhone-Lite.opml` — 30-feed lower-burden phone bundle.
- `feed-manifest.json` — the source of truth for titles, folders, URLs, metadata, notification recommendations, freshness policy and profile membership.

Regenerate the OPML and source tables after changing the manifest:

```sh
make generate
```

The OPML does not reliably carry NetNewsWire notification settings. Use the notification column in the generated source table and the post-import checklist in [NetNewsWire-Setup-and-Notification-Plan.md](NetNewsWire-Setup-and-Notification-Plan.md).
The `eventDriven` attribute is validator metadata, not a required NetNewsWire feature; if the app re-exports OPML and drops custom attributes, regenerate the bundle from the manifest.

## Validation

Run deterministic tests and then the live endpoint audit:

```sh
make test
make validate
make validate-lite
```

The validator checks HTTPS transport and redirects, HTTP status, XML roots, MIME safety, every item title/date/link, event-driven stale-review deadlines, manifest/OPML/source-table metadata alignment, duplicate/noise rates and compressed/wire versus full-body mobile telemetry.

Each live run also maintains an ignored `.validation-history.json` file. It records the last 20 runs per profile and reports when the same profile has failed three consecutive checks.

The live reports are generated as [Markdown](NetNewsWire-Finance-Cyber-VALIDATION-REPORT.md) and [JSON](NetNewsWire-Finance-Cyber-VALIDATION-REPORT.json). A healthy run has no failed feeds, metadata mismatches, noisy feeds, future-dated items or stale-review deadlines due.

## Daily digest preparation

Export selected NetNewsWire articles as a JSON array (or JSON lines) with at least `title` and `link`, then run:

```sh
python3 prepare-rss-digest-input.py \
  --input selected-articles.json \
  --output digest-input.json \
  --state .digest-state.json
```

The tool canonicalizes links, removes already processed items, sorts by publication time and maintains a local state file. Feed the resulting `digest-input.json` to [Apple-Intelligence-RSS-Summary-Prompt.md](Apple-Intelligence-RSS-Summary-Prompt.md). Use `--dry-run` to inspect input without advancing state.

## Maintenance

Run the live audit monthly or after a source reports a failed refresh. Keep the manifest, generated artifacts, validation report and changelog together. Coverage additions still require a documented gap, a direct validated HTTPS RSS/Atom endpoint and a clear marginal-value case; a larger feed count is not a success by itself.
