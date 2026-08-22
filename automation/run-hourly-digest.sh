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
# The macOS Shortcuts command has a smaller practical request ceiling than
# the raw file argument suggests. Keep a wide margin for the shortcut wrapper
# and Apple Intelligence's input envelope; override only after testing locally.
SHORTCUT_MAX_INPUT_BYTES=${NETNEWSWIRE_SHORTCUT_MAX_INPUT_BYTES:-4000}

RUN_SHORTCUT=0
if [ "${1:-}" = "--run-shortcut" ]; then
  RUN_SHORTCUT=1
fi

FETCH_STATE_PATH="$RUNTIME_DIR/fetch-state.json"
DIGEST_STATE_PATH="$RUNTIME_DIR/digest-state.json"
STATE_BACKUP_DIR=""
SHORTCUT_BATCH_DIR=""
AI_OUTPUT_TMP=""
HAD_FETCH_STATE=0
HAD_DIGEST_STATE=0

cleanup() {
  status=$?
  if [ "$RUN_SHORTCUT" -eq 1 ] && [ "$status" -ne 0 ] && [ -n "$STATE_BACKUP_DIR" ]; then
    if [ "$HAD_FETCH_STATE" -eq 1 ]; then
      cp -p "$STATE_BACKUP_DIR/fetch-state.json" "$FETCH_STATE_PATH"
    else
      rm -f "$FETCH_STATE_PATH"
    fi
    if [ "$HAD_DIGEST_STATE" -eq 1 ]; then
      cp -p "$STATE_BACKUP_DIR/digest-state.json" "$DIGEST_STATE_PATH"
    else
      rm -f "$DIGEST_STATE_PATH"
    fi
  fi
  if [ -n "$AI_OUTPUT_TMP" ]; then
    rm -f "$AI_OUTPUT_TMP"
  fi
  if [ -n "$SHORTCUT_BATCH_DIR" ]; then
    rm -rf "$SHORTCUT_BATCH_DIR"
  fi
  if [ -n "$STATE_BACKUP_DIR" ]; then
    rm -rf "$STATE_BACKUP_DIR"
  fi
  exit "$status"
}

trap cleanup EXIT
DIGEST_MAX_ITEMS=${NETNEWSWIRE_DIGEST_MAX_ITEMS:-36}
DIGEST_MAX_ITEM_CHARS=${NETNEWSWIRE_DIGEST_MAX_ITEM_CHARS:-5000}
DIGEST_MAX_TOTAL_CHARS=${NETNEWSWIRE_DIGEST_MAX_TOTAL_CHARS:-110000}

mkdir -p "$RUNTIME_DIR"

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
    cp -p "$FETCH_STATE_PATH" "$STATE_BACKUP_DIR/fetch-state.json"
    HAD_FETCH_STATE=1
  fi
  if [ -e "$DIGEST_STATE_PATH" ]; then
    cp -p "$DIGEST_STATE_PATH" "$STATE_BACKUP_DIR/digest-state.json"
    HAD_DIGEST_STATE=1
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
    shortcuts run "$SHORTCUT_NAME" \
      --input-path "$BATCH_INPUT" \
      --output-path "$BATCH_OUTPUT"
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
