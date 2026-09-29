#!/usr/bin/env bash
# Lightweight offline CI for NetNewsWire Finance + Cyber RSS (Python bundle tooling).
# Mirrors make check-frozen without requiring make/zsh: lint, docs, hygiene, tests, syntax.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PYTHON="${PYTHON:-python3}"

echo "== required files =="
test -f README.md
test -f LICENSE
test -f Makefile
test -f feed-manifest.json
test -f generate-bundle.py
test -f validate-manifest.py
test -f validate-docs.py
test -f check-repository-hygiene.py
test -f validate-rss-bundle.sh
test -d artifacts/opml
test -d tests

echo "== JSON parse =="
"$PYTHON" -c "import json; json.load(open('feed-manifest.json'))"
"$PYTHON" -c "import json; json.load(open('marketplace/netnewswire-finance-cyber-rss.json'))"

echo "== python compile =="
"$PYTHON" -m compileall -q .

echo "== shell syntax (POSIX) =="
for f in automation/run-hourly-digest.sh automation/install-hourly-digest-launch-agent.sh scripts/ci-validate.sh; do
  echo "bash -n $f"
  bash -n "$f"
done

echo "== manifest lint =="
"$PYTHON" validate-manifest.py --manifest feed-manifest.json --root .

echo "== docs check =="
"$PYTHON" validate-docs.py --root .

echo "== repository hygiene =="
"$PYTHON" check-repository-hygiene.py --root .

echo "== unit tests =="
PYTHONPATH=. "$PYTHON" -m unittest discover -s tests -q

echo "== README relative links =="
"$PYTHON" scripts/ci-check-readme-links.py

echo "== validate OK =="
