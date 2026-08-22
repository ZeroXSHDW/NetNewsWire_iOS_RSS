.DEFAULT_GOAL := help

.PHONY: help generate package hourly-digest lint docs-check hygiene test compile syntax validate validate-lite validate-air validate-all check check-frozen

PYTHON ?= python3
MANIFEST := feed-manifest.json
OPML_ROOT := artifacts/opml
SOURCE_ROOT := artifacts/sources
NOTIFICATION_ROOT := artifacts/notifications
REPORT_ROOT := artifacts/validation
AIRDROP_ROOT := artifacts/AirDrop

help:
	@printf '%s\n' \
		'NetNewsWire Finance + Cyber bundle' \
		'  make package       Generate all profiles and refresh the AirDrop handoff' \
		'  make check         Run offline generation, lint, docs, hygiene and tests' \
		'  make hygiene       Scan tracked files for secrets, local paths and runtime state' \
		'  make validate-all  Run live validation for Master, iPhone Lite and Air' \
		'  make validate      Run live validation for the Master profile' \
		'  make validate-lite Run live validation for iPhone Lite' \
		'  make validate-air  Run live validation for iPhone Air' \
		'  make generate      Regenerate OPML and source-table artifacts only' \
		'  make check-frozen  Run non-mutating checks against the frozen artifacts' \
		'  make hourly-digest Collect manifest feeds and prepare the Apple Intelligence handoff'

RUNTIME_DIR ?= .runtime/hourly

generate:
	$(PYTHON) generate-bundle.py --manifest $(MANIFEST) --all \
		--notification-table $(NOTIFICATION_ROOT)/NetNewsWire-Notification-Profile.md \
		--notification-json $(NOTIFICATION_ROOT)/NetNewsWire-Notification-Profile.json

package: generate
	mkdir -p $(AIRDROP_ROOT)
	cp $(OPML_ROOT)/NetNewsWire-Finance-Cyber-iPhone-Air.opml $(AIRDROP_ROOT)/NetNewsWire-Finance-Cyber-iPhone-Air.opml

hourly-digest:
	$(PYTHON) run-hourly-rss-digest.py \
		--manifest $(MANIFEST) \
		--source-profile master \
		--digest-profile master \
		--fetch-state $(RUNTIME_DIR)/fetch-state.json \
		--digest-state $(RUNTIME_DIR)/digest-state.json \
		--output $(RUNTIME_DIR)/hourly-digest-input.json \
		--shortcut-output $(RUNTIME_DIR)/shortcut-digest.txt

test:
	PYTHONPATH=. $(PYTHON) -m unittest discover -s tests -v

compile:
	$(PYTHON) -m compileall -q .

syntax:
	zsh -n validate-rss-bundle.sh

lint:
	$(PYTHON) validate-manifest.py --manifest $(MANIFEST) --root .

docs-check:
	$(PYTHON) validate-docs.py --root .

hygiene:
	$(PYTHON) check-repository-hygiene.py --root .

validate:
	./validate-rss-bundle.sh

validate-lite:
	VALIDATION_PROFILE=iphone-lite \
	SOURCE_TABLE_FILE=$(SOURCE_ROOT)/NetNewsWire-Finance-Cyber-iPhone-Lite-Source-Table.md \
	REPORT_MARKDOWN_FILE=$(REPORT_ROOT)/NetNewsWire-Finance-Cyber-iPhone-Lite-VALIDATION-REPORT.md \
	REPORT_JSON_FILE=$(REPORT_ROOT)/NetNewsWire-Finance-Cyber-iPhone-Lite-VALIDATION-REPORT.json \
	./validate-rss-bundle.sh $(OPML_ROOT)/NetNewsWire-Finance-Cyber-iPhone-Lite.opml

validate-air:
	VALIDATION_PROFILE=iphone-air \
	SOURCE_TABLE_FILE=$(SOURCE_ROOT)/NetNewsWire-Finance-Cyber-iPhone-Air-Source-Table.md \
	REPORT_MARKDOWN_FILE=$(REPORT_ROOT)/NetNewsWire-Finance-Cyber-iPhone-Air-VALIDATION-REPORT.md \
	REPORT_JSON_FILE=$(REPORT_ROOT)/NetNewsWire-Finance-Cyber-iPhone-Air-VALIDATION-REPORT.json \
	./validate-rss-bundle.sh $(OPML_ROOT)/NetNewsWire-Finance-Cyber-iPhone-Air.opml

validate-all:
	$(MAKE) validate
	$(MAKE) validate-lite
	$(MAKE) validate-air

check: package lint docs-check hygiene compile test syntax

check-frozen:
	PYTHONDONTWRITEBYTECODE=1 $(MAKE) lint docs-check hygiene test syntax
	git diff --check
