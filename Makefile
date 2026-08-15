.PHONY: generate test validate validate-lite check

PYTHON ?= python3

generate:
	$(PYTHON) generate-bundle.py --manifest feed-manifest.json --profile master \
		--opml NetNewsWire-Finance-Cyber.opml \
		--source-table NetNewsWire-Finance-Cyber-Source-Table.md
	$(PYTHON) generate-bundle.py --manifest feed-manifest.json --profile iphone-lite \
		--opml NetNewsWire-Finance-Cyber-iPhone-Lite.opml \
		--source-table NetNewsWire-Finance-Cyber-iPhone-Lite-Source-Table.md
	$(PYTHON) generate-bundle.py --manifest feed-manifest.json --profile master \
		--notification-table NetNewsWire-Notification-Profile.md \
		--notification-json NetNewsWire-Notification-Profile.json

test:
	PYTHONPATH=. $(PYTHON) -m unittest discover -s tests -v

validate:
	./validate-rss-bundle.sh

validate-lite:
	VALIDATION_PROFILE=iphone-lite \
	SOURCE_TABLE_FILE=NetNewsWire-Finance-Cyber-iPhone-Lite-Source-Table.md \
	REPORT_MARKDOWN_FILE=NetNewsWire-Finance-Cyber-iPhone-Lite-VALIDATION-REPORT.md \
	REPORT_JSON_FILE=NetNewsWire-Finance-Cyber-iPhone-Lite-VALIDATION-REPORT.json \
	./validate-rss-bundle.sh NetNewsWire-Finance-Cyber-iPhone-Lite.opml

check: generate test
