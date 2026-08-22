#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
TEMPLATE="$SCRIPT_DIR/com.netnewswire.finance-cyber.hourly-digest.plist.template"
PYTHON_BIN=${PYTHON_BIN:-$(command -v python3)}
RUNTIME_DIR=${NETNEWSWIRE_DIGEST_DIR:-"$ROOT/.runtime/hourly"}
INTERVAL=${NETNEWSWIRE_DIGEST_INTERVAL:-1800}
SHORTCUT_NAME=${SHORTCUT_NAME:-"Daily Finance + Cyber Digest"}
USER_HOME=$(python3 -c 'from pathlib import Path; print(Path.home())')
LABEL=com.netnewswire.finance-cyber.hourly-digest
LAUNCH_AGENTS_DIR="$USER_HOME/Library/LaunchAgents"
PLIST_PATH="$LAUNCH_AGENTS_DIR/$LABEL.plist"
STAGED_ROOT=${NETNEWSWIRE_STAGED_ROOT:-"$USER_HOME/Library/Application Support/NetNewsWireSubscriptions/hourly-app"}
LAUNCH_RUNTIME_DIR=${NETNEWSWIRE_LAUNCH_RUNTIME_DIR:-"$USER_HOME/Library/Application Support/NetNewsWireSubscriptions/hourly-runtime"}

case "$INTERVAL" in
  ''|*[!0-9]*) echo "NETNEWSWIRE_DIGEST_INTERVAL must be a positive number of seconds" >&2; exit 2 ;;
esac
if [ "$INTERVAL" -lt 60 ]; then
  echo "NETNEWSWIRE_DIGEST_INTERVAL must be at least 60 seconds" >&2
  exit 2
fi
if ! command -v shortcuts >/dev/null 2>&1; then
  echo "the macOS shortcuts command is unavailable" >&2
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
  state_utils.py; do
  cp "$ROOT/$relative_path" "$STAGED_ROOT/$relative_path"
done
cp "$ROOT/automation/run-hourly-digest.sh" "$STAGED_ROOT/automation/run-hourly-digest.sh"
cp "$ROOT/docs/Apple-Intelligence-RSS-Summary-Prompt.md" \
  "$STAGED_ROOT/docs/Apple-Intelligence-RSS-Summary-Prompt.md"
chmod 0755 "$STAGED_ROOT/automation/run-hourly-digest.sh"

python3 - "$TEMPLATE" "$PLIST_PATH" "$STAGED_ROOT" "$LAUNCH_RUNTIME_DIR" "$PYTHON_BIN" "$INTERVAL" "$SHORTCUT_NAME" <<'PY'
import plistlib
import sys
from pathlib import Path

template_path, output_path, staged_root, runtime_dir, python_bin, interval, shortcut_name = sys.argv[1:]
text = Path(template_path).read_text(encoding="utf-8")
for marker, value in {
    "__STAGED_ROOT__": staged_root,
    "__RUNTIME_DIR__": runtime_dir,
    "__PYTHON_BIN__": python_bin,
    "__INTERVAL__": interval,
    "__SHORTCUT_NAME__": shortcut_name,
}.items():
    text = text.replace(marker, value)
payload = plistlib.loads(text.encode("utf-8"))
Path(output_path).write_bytes(plistlib.dumps(payload, fmt=plistlib.FMT_XML, sort_keys=False))
PY

GUI_DOMAIN="gui/$(id -u)"
launchctl bootout "$GUI_DOMAIN/$LABEL" >/dev/null 2>&1 || true
launchctl bootstrap "$GUI_DOMAIN" "$PLIST_PATH"
launchctl enable "$GUI_DOMAIN/$LABEL"

echo "installed $PLIST_PATH"
echo "interval_seconds=$INTERVAL runtime_dir=$RUNTIME_DIR"
