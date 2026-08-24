#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
TEMPLATE="$SCRIPT_DIR/com.netnewswire.finance-cyber.hourly-digest.plist.template"
PYTHON_BIN=${PYTHON_BIN:-}
if [ -z "$PYTHON_BIN" ]; then
  PYTHON_BIN=$(command -v python3 || true)
elif case "$PYTHON_BIN" in */*) false ;; *) true ;; esac; then
  PYTHON_BIN=$(command -v "$PYTHON_BIN" || true)
fi
INTERVAL=${NETNEWSWIRE_DIGEST_INTERVAL:-1800}
JOB_TIMEOUT=${NETNEWSWIRE_DIGEST_TIMEOUT:-3600}
SHORTCUT_NAME=${SHORTCUT_NAME:-"Daily Finance + Cyber Digest"}
SHORTCUT_TIMEOUT_SECONDS=${NETNEWSWIRE_SHORTCUT_TIMEOUT_SECONDS:-900}
LOG_MAX_BYTES=${NETNEWSWIRE_LOG_MAX_BYTES:-1048576}
if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
  cat <<'USAGE'
Usage: install-hourly-digest-launch-agent.sh

Install or replace the per-user launchd job for the hourly digest.
The named Shortcut must already exist and be tested manually.

Environment overrides:
  NETNEWSWIRE_DIGEST_INTERVAL (minimum 60 seconds)
  NETNEWSWIRE_DIGEST_TIMEOUT (launchd hard timeout, minimum 60 seconds)
  NETNEWSWIRE_DIGEST_DIR, NETNEWSWIRE_STAGED_ROOT, NETNEWSWIRE_LAUNCH_RUNTIME_DIR
  NETNEWSWIRE_SHORTCUT_TIMEOUT_SECONDS, NETNEWSWIRE_LOG_MAX_BYTES
  SHORTCUT_NAME, PYTHON_BIN
USAGE
  exit 0
fi
if [ "$#" -gt 0 ]; then
  echo "unknown option '$1' (try --help)" >&2
  exit 2
fi
if [ -z "$PYTHON_BIN" ] || [ ! -x "$PYTHON_BIN" ]; then
  echo "a usable Python 3 executable is required; set PYTHON_BIN if needed" >&2
  exit 2
fi
if ! "$PYTHON_BIN" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)' >/dev/null 2>&1; then
  echo "Python 3.11 or newer is required; set PYTHON_BIN to a supported interpreter" >&2
  exit 2
fi
USER_HOME=$("$PYTHON_BIN" -c 'from pathlib import Path; print(Path.home())')
LABEL=com.netnewswire.finance-cyber.hourly-digest
LAUNCH_AGENTS_DIR="$USER_HOME/Library/LaunchAgents"
PLIST_PATH="$LAUNCH_AGENTS_DIR/$LABEL.plist"
STAGED_ROOT=${NETNEWSWIRE_STAGED_ROOT:-"$USER_HOME/Library/Application Support/NetNewsWireSubscriptions/hourly-app"}
LAUNCH_RUNTIME_DIR=${NETNEWSWIRE_LAUNCH_RUNTIME_DIR:-${NETNEWSWIRE_DIGEST_DIR:-"$USER_HOME/Library/Application Support/NetNewsWireSubscriptions/hourly-runtime"}}
RUNTIME_DIR="$LAUNCH_RUNTIME_DIR"

case "$INTERVAL" in
  ''|*[!0-9]*) echo "NETNEWSWIRE_DIGEST_INTERVAL must be a positive number of seconds" >&2; exit 2 ;;
esac
if [ "$INTERVAL" -lt 60 ]; then
  echo "NETNEWSWIRE_DIGEST_INTERVAL must be at least 60 seconds" >&2
  exit 2
fi
case "$JOB_TIMEOUT" in
  ''|*[!0-9]*) echo "NETNEWSWIRE_DIGEST_TIMEOUT must be a positive number of seconds" >&2; exit 2 ;;
esac
if [ "$JOB_TIMEOUT" -lt 60 ]; then
  echo "NETNEWSWIRE_DIGEST_TIMEOUT must be at least 60 seconds" >&2
  exit 2
fi
case "$SHORTCUT_TIMEOUT_SECONDS" in
  ''|*[!0-9.]*) echo "NETNEWSWIRE_SHORTCUT_TIMEOUT_SECONDS must be numeric" >&2; exit 2 ;;
esac
if ! "$PYTHON_BIN" -c 'import sys; raise SystemExit(0 if float(sys.argv[1]) > 0 else 1)' "$SHORTCUT_TIMEOUT_SECONDS" >/dev/null 2>&1; then
  echo "NETNEWSWIRE_SHORTCUT_TIMEOUT_SECONDS must be positive" >&2
  exit 2
fi
case "$LOG_MAX_BYTES" in
  ''|*[!0-9]*) echo "NETNEWSWIRE_LOG_MAX_BYTES must be numeric" >&2; exit 2 ;;
esac
if [ "$LOG_MAX_BYTES" -lt 1 ]; then
  echo "NETNEWSWIRE_LOG_MAX_BYTES must be positive" >&2
  exit 2
fi
if ! command -v launchctl >/dev/null 2>&1; then
  echo "the macOS launchctl command is unavailable" >&2
  exit 2
fi
if ! command -v shortcuts >/dev/null 2>&1; then
  echo "the macOS shortcuts command is unavailable" >&2
  exit 2
fi
if [ ! -f "$TEMPLATE" ]; then
  echo "launch-agent template not found: $TEMPLATE" >&2
  exit 2
fi
if ! shortcuts list | grep -Fqx "$SHORTCUT_NAME"; then
  echo "create and test the '$SHORTCUT_NAME' Shortcut before installing the launch agent" >&2
  exit 2
fi

mkdir -p "$LAUNCH_AGENTS_DIR" "$RUNTIME_DIR" "$STAGED_ROOT/docs" "$STAGED_ROOT/automation" "$LAUNCH_RUNTIME_DIR"

# launchd cannot read an executable located under Desktop on this Mac. Stage
# the small, self-contained collector bundle under Library so the recurring
# job can run without granting a broad Desktop/Files permission to launchd.
for relative_path in \
  feed-manifest.json \
  run-hourly-rss-digest.py \
  fetch-rss-digest-input.py \
  prepare-rss-digest-input.py \
  bundle_config.py \
  rss_validation.py \
  state_utils.py \
  runtime_health.py; do
  cp "$ROOT/$relative_path" "$STAGED_ROOT/$relative_path"
done
cp "$ROOT/automation/run-hourly-digest.sh" "$STAGED_ROOT/automation/run-hourly-digest.sh"
cp "$ROOT/automation/run-shortcut.py" "$STAGED_ROOT/automation/run-shortcut.py"
cp "$ROOT/docs/Apple-Intelligence-RSS-Summary-Prompt.md" \
  "$STAGED_ROOT/docs/Apple-Intelligence-RSS-Summary-Prompt.md"
chmod 0755 "$STAGED_ROOT/automation/run-hourly-digest.sh"
chmod 0755 "$STAGED_ROOT/automation/run-shortcut.py"

"$PYTHON_BIN" - "$TEMPLATE" "$PLIST_PATH" "$STAGED_ROOT" "$LAUNCH_RUNTIME_DIR" "$PYTHON_BIN" "$INTERVAL" "$JOB_TIMEOUT" "$SHORTCUT_NAME" "$SHORTCUT_TIMEOUT_SECONDS" "$LOG_MAX_BYTES" <<'PY'
import os
import plistlib
import sys
import tempfile
from pathlib import Path

template_path, output_path, staged_root, runtime_dir, python_bin, interval, job_timeout, shortcut_name, shortcut_timeout, log_max_bytes = sys.argv[1:]
text = Path(template_path).read_text(encoding="utf-8")
for marker, value in {
    "__STAGED_ROOT__": staged_root,
    "__RUNTIME_DIR__": runtime_dir,
    "__PYTHON_BIN__": python_bin,
    "__INTERVAL__": interval,
    "__JOB_TIMEOUT__": job_timeout,
    "__SHORTCUT_NAME__": shortcut_name,
    "__SHORTCUT_TIMEOUT__": shortcut_timeout,
    "__LOG_MAX_BYTES__": log_max_bytes,
}.items():
    text = text.replace(marker, value)
payload = plistlib.loads(text.encode("utf-8"))
destination = Path(output_path)
destination.parent.mkdir(parents=True, exist_ok=True)
descriptor, temporary_name = tempfile.mkstemp(prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent)
try:
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(plistlib.dumps(payload, fmt=plistlib.FMT_XML, sort_keys=False))
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary_name, destination)
except BaseException:
    try:
        os.unlink(temporary_name)
    except FileNotFoundError:
        pass
    raise
PY

GUI_DOMAIN="gui/$(id -u)"
launchctl bootout "$GUI_DOMAIN/$LABEL" >/dev/null 2>&1 || true
launchctl bootstrap "$GUI_DOMAIN" "$PLIST_PATH"
launchctl enable "$GUI_DOMAIN/$LABEL"

echo "installed $PLIST_PATH"
echo "interval_seconds=$INTERVAL runtime_dir=$LAUNCH_RUNTIME_DIR python=$PYTHON_BIN"
