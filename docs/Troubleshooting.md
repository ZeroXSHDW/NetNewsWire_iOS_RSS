# Troubleshooting

## The OPML file opens as text instead of importing

On iPhone, use the **Download for iPhone** link in the root README, then choose **Share → Save to Files** if Safari displays the XML. Keep the `.opml` extension. In NetNewsWire, use **Feeds → Settings → Import Subscriptions** and select the saved file. If the file was renamed to `.xml` or downloaded without an extension, rename it back to `.opml` before importing.

Import one profile at a time. NetNewsWire treats OPML import as additive, so importing a newer copy over an older copy can create duplicate subscriptions.

## The feeds imported, but notifications are missing

Notification settings are not reliably carried by OPML. Apply the generated [notification/profile matrix](../artifacts/notifications/NetNewsWire-Notification-Profile.md) after the import. Start with the four feeds marked **On**; leave the rest off unless you have a specific reason to receive interruptions.

## Offline checks and live validation behave differently

For a compact read-only overview of the current manifest, generated-file presence and committed validation snapshots, run:

```sh
make status
```

This command does not fetch feeds or rewrite artifacts. It is useful before choosing between the offline `make check-frozen` gate and the network-backed profile audits below.

Use `make doctor` to check the local toolchain, then `make check` for deterministic generation, documentation, hygiene, tests and shell syntax. These checks do not need network access. Use `make doctor-live` before `make validate-all` when you want to verify that `curl` and `xmllint` are installed. Live validation depends on third-party feed servers and can report a feed failure even when the manifest and generated artifacts are correct.

When a live run fails, open the matching report under [`artifacts/validation/`](../artifacts/validation/) and check the feed URL, HTTP status, XML result and error detail. Do not hand-edit the report, OPML or source table; fix the manifest or validator rule, then regenerate with `make package`.

The committed validation report is a snapshot, not a live service monitor. A
single HTTP 5xx, WAF response or malformed publisher payload should be
rechecked before removing a feed. The report distinguishes hard feed failures
from tolerated future-date and other attention entries.

## The digest is empty or repeats an article

An empty digest means no new valid items were selected within the supplied input and profile budget. Confirm that the export contains an HTTP(S) `link` and a `title`, and run the preparation command with `--dry-run` while testing. The ignored state file records canonicalized items that have already been processed; use a new temporary `--state` path to test an export without changing your normal history.

If an article repeats across feeds, the preparation step may group it as a conservative duplicate story. The digest keeps the source links so you can compare the original reporting rather than treating the repetition as independent confirmation.

## The hourly Shortcut handoff does not run

Run `make hourly-digest` first and inspect `.runtime/hourly/shortcut-digest.txt`. The Shortcut must be named `Daily Finance + Cyber Digest`, accept **Shortcut Input**, convert the input to text, and produce output containing source links when articles are present. Test it manually before installing the launch agent:

```sh
shortcuts run "Daily Finance + Cyber Digest" \
  --input-path ".runtime/hourly/shortcut-digest.txt" \
  --output-path ".runtime/hourly/apple-intelligence-output.txt"
```

The launch agent needs a logged-in, awake Mac with network access. Review
`.runtime/hourly/hourly.log` (plus its rotated copies) for scheduler
diagnostics. The collector intentionally does not read NetNewsWire’s private
iPhone unread database; use the Share Sheet workflow when the digest must
contain only reader-selected items.

The installed job requires Python 3.11 or newer. Check the exact interpreter
that will be staged with:

```sh
PYTHON_BIN=/opt/homebrew/bin/python3.12 make doctor
```

The unattended runtime writes `.runtime/hourly/health.json` (or the configured
runtime directory) with `running`, `succeeded` or `failed` status, the last
successful run and bounded collection counts. It also uses a process-wide run
lock, so a second manual or launchd-triggered invocation exits without touching
state. A stale lock from a crashed process is cleared only when its recorded
PID is no longer alive. If the lock has no readable PID, the wrapper refuses to
steal it because another process may be between creating the directory and
recording its PID; verify no digest process is running before removing
`.hourly-run.lock`. Runtime temporary directories are pruned at the next
start. If a process dies during the two-state commit, the next run replays the
hidden state-transaction journal before collecting again. `hourly.log`,
`hourly.log.1` and `hourly.log.2` are rotated at the configured size limit.

If a run fails after collection but before Apple Intelligence completes, the
last fetch and digest state are restored. The prepared files may still show
the attempted batch; rerun after fixing the Shortcut and verify `health.json`
before relying on the output.

If a state file reports an unsupported schema version or invalid structure,
keep a copy for diagnosis and test with a new state path. Do not delete the
normal state blindly; an explicit state reset is a recovery decision because
it can cause previously processed articles to be delivered again.
