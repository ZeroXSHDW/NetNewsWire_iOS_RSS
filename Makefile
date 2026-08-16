.PHONY: generate package lint test compile syntax validate validate-lite validate-air check

PYTHON ?= python3

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

check: package lint compile test syntax
