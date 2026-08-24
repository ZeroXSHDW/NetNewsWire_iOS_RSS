#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
RUNTIME_DIR=${NETNEWSWIRE_DIGEST_DIR:-"$ROOT/.runtime/hourly"}
PYTHON_BIN=${PYTHON_BIN:-python3}
SOURCE_PROFILE=${NETNEWSWIRE_SOURCE_PROFILE:-master}
DIGEST_PROFILE=${NETNEWSWIRE_DIGEST_PROFILE:-master}
SHORTCUT_NAME=${SHORTCUT_NAME:-"Daily Finance + Cyber Digest"}
AI_OUTPUT_PATH=${NETNEWSWIRE_AI_OUTPUT:-"$RUNTIME_DIR/apple-intelligence-output.txt"}
HEALTH_PATH=${NETNEWSWIRE_HEALTH_PATH:-"$RUNTIME_DIR/health.json"}
LOG_PATH=${NETNEWSWIRE_LOG_PATH:-}
LOG_MAX_BYTES=${NETNEWSWIRE_LOG_MAX_BYTES:-1048576}
# The macOS Shortcuts command has a smaller practical request ceiling than
# the raw file argument suggests. Keep a wide margin for the shortcut wrapper
# and Apple Intelligence's input envelope; override only after testing locally.
SHORTCUT_MAX_INPUT_BYTES=${NETNEWSWIRE_SHORTCUT_MAX_INPUT_BYTES:-4000}
SHORTCUT_TIMEOUT_SECONDS=${NETNEWSWIRE_SHORTCUT_TIMEOUT_SECONDS:-900}

RUN_SHORTCUT=0
case "${1:-}" in
  "") ;;
  --run-shortcut) RUN_SHORTCUT=1 ;;
  --help|-h)
    cat <<'USAGE'
Usage: run-hourly-digest.sh [--run-shortcut]

Prepare the bounded hourly digest in the configured runtime directory.
With --run-shortcut, pass each bounded batch to the named macOS Shortcut and
write the combined Apple Intelligence output.

Environment overrides:
  NETNEWSWIRE_DIGEST_DIR, NETNEWSWIRE_SOURCE_PROFILE, NETNEWSWIRE_DIGEST_PROFILE
  NETNEWSWIRE_HEALTH_PATH, NETNEWSWIRE_LOG_PATH, NETNEWSWIRE_LOG_MAX_BYTES
  SHORTCUT_NAME, PYTHON_BIN, NETNEWSWIRE_SHORTCUT_MAX_INPUT_BYTES
  NETNEWSWIRE_SHORTCUT_TIMEOUT_SECONDS
USAGE
    exit 0
    ;;
  *)
    echo "hourly digest: unknown option '$1' (try --help)" >&2
    exit 2
    ;;
esac

FETCH_STATE_PATH="$RUNTIME_DIR/fetch-state.json"
DIGEST_STATE_PATH="$RUNTIME_DIR/digest-state.json"
RUN_LOCK_DIR="$RUNTIME_DIR/.hourly-run.lock"
STATE_BACKUP_DIR=""
SHORTCUT_BATCH_DIR=""
AI_OUTPUT_TMP=""
HAD_FETCH_STATE=0
HAD_DIGEST_STATE=0
STATE_BACKUP_FAILED=0
RUN_LOCK_HELD=0
HEALTH_ACTIVE=0
HEALTH_FINALIZED=0
RUN_ID=""
RUN_STARTED_AT=""

validate_python() {
  if ! "$PYTHON_BIN" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)' >/dev/null 2>&1; then
    echo "hourly digest: Python 3.11 or newer is required; set PYTHON_BIN to a supported interpreter" >&2
    exit 2
  fi
}

acquire_run_lock() {
  if mkdir "$RUN_LOCK_DIR" 2>/dev/null; then
    RUN_LOCK_HELD=1
    printf '%s\n' "$$" > "$RUN_LOCK_DIR/pid"
    return 0
  fi

  owner_pid=$(sed -n '1p' "$RUN_LOCK_DIR/pid" 2>/dev/null || true)
  case "$owner_pid" in
    ''|*[!0-9]*)
      echo "hourly digest: run lock has no valid owner; inspect before removing: $RUN_LOCK_DIR" >&2
      exit 75
      ;;
    *)
      if kill -0 "$owner_pid" 2>/dev/null; then
        echo "hourly digest: another run is active (pid $owner_pid)" >&2
        exit 75
      fi
      ;;
  esac

  rm -f "$RUN_LOCK_DIR/pid"
  if ! rmdir "$RUN_LOCK_DIR" 2>/dev/null; then
    echo "hourly digest: could not clear stale run lock: $RUN_LOCK_DIR" >&2
    exit 75
  fi
  if ! mkdir "$RUN_LOCK_DIR" 2>/dev/null; then
    echo "hourly digest: another run acquired the lock" >&2
    exit 75
  fi
  RUN_LOCK_HELD=1
  printf '%s\n' "$$" > "$RUN_LOCK_DIR/pid"
}

release_run_lock() {
  if [ "$RUN_LOCK_HELD" -eq 1 ]; then
    rm -f "$RUN_LOCK_DIR/pid" || true
    rmdir "$RUN_LOCK_DIR" 2>/dev/null || true
    RUN_LOCK_HELD=0
  fi
}

prune_runtime_temporary_directories() {
  for stale in \
    "$RUNTIME_DIR"/.shortcut-batches.* \
    "$RUNTIME_DIR"/.hourly-state.* \
    "$RUNTIME_DIR"/.hourly-rss-*; do
    [ -d "$stale" ] || continue
    rm -rf "$stale"
  done
}

rotate_log_and_redirect() {
  [ -n "$LOG_PATH" ] || return 0
  case "$LOG_MAX_BYTES" in
    ''|*[!0-9]*) echo "hourly digest: NETNEWSWIRE_LOG_MAX_BYTES must be numeric" >&2; exit 2 ;;
  esac
  if [ "$LOG_MAX_BYTES" -lt 1 ]; then
    echo "hourly digest: NETNEWSWIRE_LOG_MAX_BYTES must be positive" >&2
    exit 2
  fi
  mkdir -p "$(dirname "$LOG_PATH")"
  if [ -f "$LOG_PATH" ]; then
    current_bytes=$(wc -c < "$LOG_PATH" | tr -d '[:space:]')
    if [ "$current_bytes" -gt "$LOG_MAX_BYTES" ]; then
      rm -f "$LOG_PATH.2"
      if [ -f "$LOG_PATH.1" ]; then
        mv -f "$LOG_PATH.1" "$LOG_PATH.2"
      fi
      mv -f "$LOG_PATH" "$LOG_PATH.1"
    fi
  fi
  exec >> "$LOG_PATH" 2>&1
}

trim_active_log() {
  [ -n "$LOG_PATH" ] || return 0
  case "$LOG_MAX_BYTES" in
    ''|*[!0-9]*) return 0 ;;
  esac
  PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}" "$PYTHON_BIN" - "$LOG_PATH" "$LOG_MAX_BYTES" <<'PY' || true
import sys
from pathlib import Path

from state_utils import atomic_write_bytes

path = Path(sys.argv[1])
limit = int(sys.argv[2])
if path.is_file():
    data = path.read_bytes()
    if len(data) > limit:
        atomic_write_bytes(path, data[-limit:])
PY
}

write_health_running() {
  "$PYTHON_BIN" "$ROOT/runtime_health.py" \
    --path "$HEALTH_PATH" \
    --status running \
    --run-id "$RUN_ID" \
    --started-at "$RUN_STARTED_AT"
}

write_health_failed() {
  failure_status=$1
  "$PYTHON_BIN" "$ROOT/runtime_health.py" \
    --path "$HEALTH_PATH" \
    --status failed \
    --run-id "$RUN_ID" \
    --started-at "$RUN_STARTED_AT" \
    --exit-code "$failure_status" \
    --message "hourly digest exited with status $failure_status" || true
}

write_health_succeeded() {
  "$PYTHON_BIN" "$ROOT/runtime_health.py" \
    --path "$HEALTH_PATH" \
    --status succeeded \
    --run-id "$RUN_ID" \
    --started-at "$RUN_STARTED_AT" \
    --package "$RUNTIME_DIR/hourly-digest-input.json"
}

restore_state_file() {
  backup_path=$1
  destination_path=$2
  if [ -f "$backup_path" ]; then
    restore_tmp="$destination_path.restore.$$"
    if cp -p "$backup_path" "$restore_tmp" && mv -f "$restore_tmp" "$destination_path"; then
      :
    else
      rm -f "$restore_tmp" || true
    fi
  else
    rm -f "$destination_path" || true
  fi
}

backup_state_file() {
  source_path=$1
  destination_path=$2
  backup_tmp="$destination_path.tmp.$$"
  if cp -p "$source_path" "$backup_tmp" && mv -f "$backup_tmp" "$destination_path"; then
    return 0
  fi
  rm -f "$backup_tmp" || true
  return 1
}

cleanup() {
  status=$?
  if [ "$HEALTH_ACTIVE" -eq 1 ] && [ "$HEALTH_FINALIZED" -eq 0 ] && [ "$status" -ne 0 ]; then
    write_health_failed "$status"
  fi
  if [ "$RUN_SHORTCUT" -eq 1 ] && [ "$status" -ne 0 ] && [ "$STATE_BACKUP_FAILED" -eq 0 ] && [ -n "$STATE_BACKUP_DIR" ]; then
    if [ "$HAD_FETCH_STATE" -eq 1 ]; then
      restore_state_file "$STATE_BACKUP_DIR/fetch-state.json" "$FETCH_STATE_PATH"
    else
      rm -f "$FETCH_STATE_PATH" || true
    fi
    if [ "$HAD_DIGEST_STATE" -eq 1 ]; then
      restore_state_file "$STATE_BACKUP_DIR/digest-state.json" "$DIGEST_STATE_PATH"
    else
      rm -f "$DIGEST_STATE_PATH" || true
    fi
  fi
  if [ -n "$AI_OUTPUT_TMP" ]; then
    rm -f "$AI_OUTPUT_TMP" || true
  fi
  if [ -n "$SHORTCUT_BATCH_DIR" ]; then
    rm -rf "$SHORTCUT_BATCH_DIR" || true
  fi
  if [ -n "$STATE_BACKUP_DIR" ]; then
    rm -rf "$STATE_BACKUP_DIR" || true
  fi
  trim_active_log
  release_run_lock
  exit "$status"
}

trap cleanup EXIT
trap 'exit 143' HUP INT TERM
DIGEST_MAX_ITEMS=${NETNEWSWIRE_DIGEST_MAX_ITEMS:-36}
DIGEST_MAX_ITEM_CHARS=${NETNEWSWIRE_DIGEST_MAX_ITEM_CHARS:-5000}
DIGEST_MAX_TOTAL_CHARS=${NETNEWSWIRE_DIGEST_MAX_TOTAL_CHARS:-110000}

mkdir -p "$RUNTIME_DIR"
validate_python
case "$SHORTCUT_TIMEOUT_SECONDS" in
  ''|*[!0-9.]*) echo "hourly digest: NETNEWSWIRE_SHORTCUT_TIMEOUT_SECONDS must be numeric" >&2; exit 2 ;;
esac
if ! "$PYTHON_BIN" -c 'import sys; raise SystemExit(0 if float(sys.argv[1]) > 0 else 1)' "$SHORTCUT_TIMEOUT_SECONDS" >/dev/null 2>&1; then
  echo "hourly digest: NETNEWSWIRE_SHORTCUT_TIMEOUT_SECONDS must be positive" >&2
  exit 2
fi
acquire_run_lock
NETNEWSWIRE_RUN_LOCK_OWNER=$$
export NETNEWSWIRE_RUN_LOCK_OWNER
RUN_ID="$$-$(date +%s)"
RUN_STARTED_AT=$(
  "$PYTHON_BIN" -c 'from datetime import datetime, timezone; print(datetime.now(timezone.utc).isoformat(timespec="seconds"))'
)
prune_runtime_temporary_directories
rotate_log_and_redirect
HEALTH_ACTIVE=1
if ! write_health_running; then
  echo "hourly digest: could not write running health record" >&2
  exit 5
fi

if [ "$RUN_SHORTCUT" -eq 1 ]; then
  if ! command -v shortcuts >/dev/null 2>&1; then
    echo "hourly digest: the macOS shortcuts command is unavailable" >&2
    exit 3
  fi
  if ! shortcuts list | grep -Fqx "$SHORTCUT_NAME"; then
    echo "hourly digest: create the '$SHORTCUT_NAME' Shortcut before enabling the launch agent" >&2
    exit 3
  fi
  STATE_BACKUP_DIR=$(mktemp -d "$RUNTIME_DIR/.hourly-state.XXXXXX")
  if [ -e "$FETCH_STATE_PATH" ]; then
    HAD_FETCH_STATE=1
    if ! backup_state_file "$FETCH_STATE_PATH" "$STATE_BACKUP_DIR/fetch-state.json"; then
      STATE_BACKUP_FAILED=1
      echo "hourly digest: could not create an atomic fetch-state backup" >&2
      exit 5
    fi
  fi
  if [ -e "$DIGEST_STATE_PATH" ]; then
    HAD_DIGEST_STATE=1
    if ! backup_state_file "$DIGEST_STATE_PATH" "$STATE_BACKUP_DIR/digest-state.json"; then
      STATE_BACKUP_FAILED=1
      echo "hourly digest: could not create an atomic digest-state backup" >&2
      exit 5
    fi
  fi
fi

"$PYTHON_BIN" "$ROOT/run-hourly-rss-digest.py" \
  --manifest "$ROOT/feed-manifest.json" \
  --source-profile "$SOURCE_PROFILE" \
  --digest-profile "$DIGEST_PROFILE" \
  --fetch-state "$FETCH_STATE_PATH" \
  --digest-state "$DIGEST_STATE_PATH" \
  --output "$RUNTIME_DIR/hourly-digest-input.json" \
  --shortcut-output "$RUNTIME_DIR/shortcut-digest.txt" \
  --digest-max-items "$DIGEST_MAX_ITEMS" \
  --digest-max-item-chars "$DIGEST_MAX_ITEM_CHARS" \
  --digest-max-total-chars "$DIGEST_MAX_TOTAL_CHARS"

if [ "$RUN_SHORTCUT" -eq 1 ]; then
  ARTICLE_COUNT=$(
    "$PYTHON_BIN" - "$RUNTIME_DIR/hourly-digest-input.json" <<'PY'
import json
import sys
from pathlib import Path

payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
print(int(payload.get("article_count", 0)))
PY
  )

  SHORTCUT_BATCH_DIR=$(mktemp -d "$RUNTIME_DIR/.shortcut-batches.XXXXXX")
  BATCH_COUNT=$(
    "$PYTHON_BIN" - "$RUNTIME_DIR/shortcut-digest.txt" "$SHORTCUT_BATCH_DIR" "$SHORTCUT_MAX_INPUT_BYTES" <<'PY'
import re
import sys
from pathlib import Path


source_path = Path(sys.argv[1])
output_dir = Path(sys.argv[2])
limit = int(sys.argv[3])
if limit < 1:
    raise SystemExit("NETNEWSWIRE_SHORTCUT_MAX_INPUT_BYTES must be positive")

text = source_path.read_text(encoding="utf-8")


def encoded_length(value: str) -> int:
    return len(value.encode("utf-8"))


def write_chunks(chunks: list[str]) -> None:
    for index, chunk in enumerate(chunks, start=1):
        (output_dir / f"input-{index:03d}.txt").write_text(chunk, encoding="utf-8")
    print(len(chunks))


if encoded_length(text) <= limit:
    write_chunks([text])
    raise SystemExit(0)

lines = text.splitlines(keepends=True)
item_starts = [
    index
    for index, line in enumerate(lines)
    if re.match(r"^\d+\.\s+", line)
]
if not item_starts:
    raise SystemExit("shortcut digest exceeds the Apple Intelligence input limit and has no article boundaries")

guardrail_start = next(
    (index for index, line in enumerate(lines) if line.startswith("Guardrail: ")),
    len(lines),
)
item_starts = [index for index in item_starts if index < guardrail_start]
if not item_starts:
    raise SystemExit("shortcut digest contains no complete article blocks")

header = "".join(lines[: item_starts[0]])
tail = "".join(lines[guardrail_start:])
items = []
for offset, start in enumerate(item_starts):
    end = item_starts[offset + 1] if offset + 1 < len(item_starts) else guardrail_start
    items.append("".join(lines[start:end]))


def render(selected: list[str]) -> str:
    adjusted_header = re.sub(
        r"(?m)^Articles: \d+[ \t]*$",
        f"Articles: {len(selected)}",
        header,
    )
    return adjusted_header + "".join(selected) + tail


chunks: list[str] = []
current: list[str] = []
for item in items:
    candidate = render([*current, item])
    if current and encoded_length(candidate) > limit:
        chunks.append(render(current))
        current = [item]
        candidate = render(current)
    if encoded_length(candidate) > limit:
        raise SystemExit("a single article block exceeds the Apple Intelligence input limit")
    current.append(item)
if current:
    chunks.append(render(current))

write_chunks(chunks)
PY
  )

  AI_OUTPUT_DIR=$(dirname "$AI_OUTPUT_PATH")
  mkdir -p "$AI_OUTPUT_DIR"
  AI_OUTPUT_TMP="$AI_OUTPUT_PATH.tmp.$$"
  : > "$AI_OUTPUT_TMP"
  BATCH_INDEX=0
  for BATCH_INPUT in "$SHORTCUT_BATCH_DIR"/input-*.txt; do
    [ -f "$BATCH_INPUT" ] || continue
    BATCH_INDEX=$((BATCH_INDEX + 1))
    BATCH_OUTPUT="$SHORTCUT_BATCH_DIR/output-$(printf '%03d' "$BATCH_INDEX").txt"
    BATCH_BYTES=$(wc -c < "$BATCH_INPUT" | tr -d ' ')
    echo "hourly digest: sending Apple Intelligence batch $BATCH_INDEX/$BATCH_COUNT (${BATCH_BYTES} bytes)"
    "$PYTHON_BIN" "$ROOT/automation/run-shortcut.py" \
      "$SHORTCUT_NAME" \
      "$BATCH_INPUT" \
      "$BATCH_OUTPUT" \
      --timeout "$SHORTCUT_TIMEOUT_SECONDS"
    if [ ! -s "$BATCH_OUTPUT" ]; then
      echo "hourly digest: the Shortcut produced no Apple Intelligence output for batch $BATCH_INDEX/$BATCH_COUNT" >&2
      exit 4
    fi
    if [ "$BATCH_INDEX" -gt 1 ]; then
      printf '\n--- Apple Intelligence batch %s of %s ---\n\n' "$BATCH_INDEX" "$BATCH_COUNT" >> "$AI_OUTPUT_TMP"
    fi
    cat "$BATCH_OUTPUT" >> "$AI_OUTPUT_TMP"
  done
  if [ "$BATCH_INDEX" -eq 0 ] || [ ! -s "$AI_OUTPUT_TMP" ]; then
    echo "hourly digest: the Shortcut produced no Apple Intelligence output" >&2
    exit 4
  fi
  mv "$AI_OUTPUT_TMP" "$AI_OUTPUT_PATH"
  AI_OUTPUT_TMP=""
  if [ "$ARTICLE_COUNT" -gt 0 ] && ! grep -Eq 'https?://' "$AI_OUTPUT_PATH"; then
    echo "hourly digest: the Shortcut output contains no source link; the input may not have reached Apple Intelligence" >&2
    exit 4
  fi
fi

if ! write_health_succeeded; then
  echo "hourly digest: could not write successful health record" >&2
  exit 5
fi
HEALTH_FINALIZED=1
