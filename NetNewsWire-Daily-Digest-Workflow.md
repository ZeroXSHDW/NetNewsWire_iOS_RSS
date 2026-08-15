# NetNewsWire daily digest workflow

This workflow turns a selected or unread NetNewsWire export into one stateful Apple Intelligence digest. It does not schedule a digest or access NetNewsWire directly; it keeps the input and deduplication step repeatable.

## 1. Export selected items

Create a JSON array like this:

```json
[
  {
    "title": "Example headline",
    "link": "https://example.com/article",
    "feed": "Example source",
    "published": "2026-08-15T09:30:00Z",
    "summary": "Optional RSS summary",
    "source_class": "official",
    "language": "en"
  }
]
```

`title` and an HTTP(S) `link` are required. `published`, `summary`, `content`, `feed`, `feed_url`, `source_class` and `language` are optional. When `feed` or `feed_url` matches `feed-manifest.json`, the preparation step adds the canonical source, folder, signal type, notification policy and profile membership.

## 2. Prepare only new items

```sh
python3 prepare-rss-digest-input.py \
  --input selected-articles.json \
  --output digest-input.json \
  --state .digest-state.json
```

The first run includes all supplied items. Later runs skip canonicalized links already recorded in `.digest-state.json`, sort newest first and include the coverage window in the output. Article text is bounded to 6,000 characters per item and 180,000 characters per package by default; the package reports truncation and budget skips. Use `--max-item-chars` or `--max-total-chars` for a different prompt budget, and use `--dry-run` when checking an export. Keep the state file local; it is ignored by Git.

## 3. Summarize

Give `digest-input.json` to Apple Intelligence with [Apple-Intelligence-RSS-Summary-Prompt.md](Apple-Intelligence-RSS-Summary-Prompt.md). Ask for one digest, not one summary per article. The output should cluster duplicate events, preserve original publication times, convert important event times to Europe/Dublin, distinguish confirmed facts from claims and end with `No action recommendation`.

## 4. Review the safety boundaries

- RSS publication time is not necessarily event time.
- A headline does not establish exploitation, attribution, market impact or a trading opportunity.
- Use official advisories or releases for confirmation and source-backed mitigation.
- Do not turn the digest into financial advice, an execution instruction or an unsupported incident-response command.
- If an export is empty, report `no material change` rather than inventing coverage.
