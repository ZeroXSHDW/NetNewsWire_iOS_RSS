.DEFAULT_GOAL := help

.PHONY: help generate package lint docs-check test compile syntax validate validate-lite validate-air validate-all check

PYTHON ?= python3

help:
	@printf '%s\n' \
		'NetNewsWire Finance + Cyber bundle' \
		'  make package       Generate all profiles and refresh the AirDrop handoff' \
		'  make check         Run offline generation, lint, docs checks and tests' \
		'  make validate-all  Run live validation for Master, iPhone Lite and Air' \
		'  make validate      Run live validation for the Master profile' \
		'  make validate-lite Run live validation for iPhone Lite' \
		'  make validate-air  Run live validation for iPhone Air' \
		'  make generate      Regenerate OPML and source-table artifacts only'

generate:
	$(PYTHON) generate-bundle.py --manifest feed-manifest.json --all \
		--notification-table NetNewsWire-Notification-Profile.md \
		--notification-json NetNewsWire-Notification-Profile.json

package: generate
	mkdir -p AirDrop
	cp NetNewsWire-Finance-Cyber-iPhone-Air.opml AirDrop/NetNewsWire-Finance-Cyber-iPhone-Air.opml

test:
	PYTHONPATH=. $(PYTHON) -m unittest discover -s tests -v

compile:
	$(PYTHON) -m compileall -q .

syntax:
	zsh -n validate-rss-bundle.sh

lint:
	$(PYTHON) validate-manifest.py --manifest feed-manifest.json --root .

docs-check:
	$(PYTHON) validate-docs.py --root .

validate:
	./validate-rss-bundle.sh

validate-lite:
	VALIDATION_PROFILE=iphone-lite \
	SOURCE_TABLE_FILE=NetNewsWire-Finance-Cyber-iPhone-Lite-Source-Table.md \
	REPORT_MARKDOWN_FILE=NetNewsWire-Finance-Cyber-iPhone-Lite-VALIDATION-REPORT.md \
	REPORT_JSON_FILE=NetNewsWire-Finance-Cyber-iPhone-Lite-VALIDATION-REPORT.json \
	./validate-rss-bundle.sh NetNewsWire-Finance-Cyber-iPhone-Lite.opml

validate-air:
	VALIDATION_PROFILE=iphone-air \
	SOURCE_TABLE_FILE=NetNewsWire-Finance-Cyber-iPhone-Air-Source-Table.md \
	REPORT_MARKDOWN_FILE=NetNewsWire-Finance-Cyber-iPhone-Air-VALIDATION-REPORT.md \
	REPORT_JSON_FILE=NetNewsWire-Finance-Cyber-iPhone-Air-VALIDATION-REPORT.json \
	./validate-rss-bundle.sh NetNewsWire-Finance-Cyber-iPhone-Air.opml

validate-all:
	$(MAKE) validate
	$(MAKE) validate-lite
	$(MAKE) validate-air

check: package lint docs-check compile test syntax
