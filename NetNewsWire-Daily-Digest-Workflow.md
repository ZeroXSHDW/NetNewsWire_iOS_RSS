# NetNewsWire daily digest workflow

This workflow turns selected NetNewsWire items, or a prepared external JSON/text export, into one stateful Apple Intelligence digest. It does not schedule a digest or access NetNewsWire’s unread database directly; it keeps the input and deduplication step repeatable.

## Optional iPhone Shortcut layer

For a practical semi-automated workflow, create a Shortcut named `Daily Finance + Cyber Digest` and enable **Show in Share Sheet**:

1. Accept text, URLs or article input from the Share Sheet, or receive a prepared `shortcut-digest.txt` file from Files.
2. If the input is empty, show `Open NetNewsWire, select the relevant unread items, and share them here.` and stop.
3. Preserve the supplied article titles, links, publication times and summaries; do not ask the model to fetch missing articles.
4. Add the fixed instructions from `Apple-Intelligence-RSS-Summary-Prompt.md` and pass the supplied digest text as the input variable to **Use Model**.
5. Choose **On-Device**, **Private Cloud Compute** or **Extension Model** (ChatGPT) deliberately, then show the response and save it to a dated Apple Note.

Create optional time-of-day personal automations for 07:30, 12:30 and 17:30 Europe/Dublin only when a prepared input source will be available. A time trigger does not create article input by itself: NetNewsWire’s documented iOS features include sharing and background refresh, but no direct Shortcut action that exports its entire unread database. Fully unattended summaries therefore need a prepared text/JSON source or a separate feed-fetching service; selected-article Share Sheet input is the simplest privacy-first option.

## 1. Provide the article input

On iPhone, use NetNewsWire’s **Today** or **All Unread** view, select the material worth summarizing and use the Share Sheet to send it to the Shortcut. A bulk unread JSON export is not supplied by NetNewsWire itself; use the JSON route below only when another exporter or a prepared file provides the input.

Create a JSON array like this:

```json
[
  {
    "title": "Example headline",
    "link": "https://example.com/article",
    "feed": "Example source",
    "published": "2026-08-16T09:30:00+01:00",
    "summary": "Optional RSS summary",
    "source_class": "official",
    "language": "en"
  }
]
```

`title` and an HTTP(S) `link` are required. `published`, `summary`, `content`, `feed`, `feed_url`, `source_class` and `language` are optional. When `feed` or `feed_url` matches `feed-manifest.json`, the preparation step adds the canonical source, folder, signal type, notification policy and profile membership; otherwise it records the source as unmatched for review.

## 2. Prepare only new items

```sh
python3 prepare-rss-digest-input.py \
  --input selected-articles.json \
  --output digest-input.json \
  --shortcut-output shortcut-digest.txt \
  --profile iphone-air \
  --state .digest-state.json
```

The first run includes all supplied Air-profile items. Later runs skip canonicalized links already recorded in `.digest-state.json`, assign conservative duplicate-story groups within a three-day publication window, sort newest first and include the coverage window in the output. The Air profile budgets 30 items, 6,000 characters per item and 90,000 text characters per package; Lite budgets 24 items, 5,000 per item and 75,000 total. The plain-text handoff keeps each source link beside its material and can be passed directly to a Shortcut or clipboard action. Use `--max-items`, `--max-item-chars`, `--max-total-chars`, `--max-seen-items` or `--duplicate-window-days` for explicit overrides, and use `--dry-run` when checking an export. The state timestamp is audit telemetry only; it does not implicitly exclude older unprocessed items. For today’s Dublin-time lower bound, use `--since 2026-08-16T00:00:00+01:00`; omit `--since` when the supplied file itself is the complete intended batch. Keep the state file local; it is ignored by Git.

The preparation command serializes access to the state file and writes both the digest package and state atomically. Invalid zero/negative budgets, invalid `--since` values and corrupt state fail with a diagnostic before output is published. If a previous process was interrupted, inspect the ignored `.digest-state.json.lock` metadata and rerun; the operating-system lock is released automatically when the process exits.

## 3. Summarize

Pass `shortcut-digest.txt` as the Shortcut’s input variable, or give `digest-input.json` to the Shortcut after reading it as text. Add the instructions from [Apple-Intelligence-RSS-Summary-Prompt.md](Apple-Intelligence-RSS-Summary-Prompt.md) to **Use Model**. Ask for one digest, not one summary per article. The output should cluster duplicate events, preserve original publication times, convert important event times to Europe/Dublin, distinguish confirmed facts from claims and end with `No action recommendation`.

## 4. Review the safety boundaries

- RSS publication time is not necessarily event time.
- A headline does not establish exploitation, attribution, market impact or a trading opportunity.
- Use official advisories or releases for confirmation and source-backed mitigation.
- Do not turn the digest into financial advice, an execution instruction or an unsupported incident-response command.
- If an export is empty, report `no material change` rather than inventing coverage.
