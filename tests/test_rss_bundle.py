from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from rss_validation import (
    compare_feed_snapshots,
    extract_feed,
    normalize_link,
    normalize_title,
    opml_entries,
    similar_titles,
    source_table_entries,
)


ROOT = Path(__file__).resolve().parents[1]


class ValidationHelpersTest(unittest.TestCase):
    def test_atom_prefers_published_and_alternate_link(self) -> None:
        root = ET.fromstring(
            """<feed xmlns="http://www.w3.org/2005/Atom">
              <title>Example</title>
              <entry>
                <title>Example story</title>
                <link rel="self" href="https://example.test/feed/1" />
                <link rel="alternate" href="https://example.test/story/1" />
                <published>2026-08-15T10:00:00Z</published>
                <updated>2026-08-16T10:00:00Z</updated>
              </entry>
            </feed>"""
        )
        title, items = extract_feed(root)
        self.assertEqual(title, "Example")
        self.assertEqual(items[0]["link"], "https://example.test/story/1")
        self.assertEqual(items[0]["date"].isoformat(), "2026-08-15T10:00:00+00:00")

    def test_normalization_removes_tracking_and_punctuation(self) -> None:
        self.assertEqual(
            normalize_link("https://Example.test/story/?utm_source=rss&x=1#comments"),
            "https://example.test/story?x=1",
        )
        self.assertEqual(normalize_title("Alert: Fortinet & VPN!"), "alert fortinet and vpn")
        self.assertTrue(
            similar_titles(
                "NCSC issues advice following global targeting of Fortinet firewalls",
                "NCSC: advice follows global targeting of Fortinet firewalls",
            )
        )

    def test_feed_drift_comparison_flags_operational_regressions(self) -> None:
        url = "https://example.test/feed.xml"
        previous = {
            url: {
                "url": url,
                "title": "Example Feed",
                "root": "rss",
                "http_code": "200",
                "effective_url": url,
                "passed": "yes",
                "recent": "yes",
                "item_count": 20,
                "payload_bytes": 100000,
                "duplicate_title_rate": 0.1,
                "duplicate_link_rate": 0.1,
                "http_item_link_count": 0,
                "missing_item_link_count": 0,
                "content_type": "application/rss+xml",
            }
        }
        current = {
            url: {
                **previous[url],
                "title": "Example Feed Renamed",
                "passed": "no",
                "recent": "no",
                "item_count": 4,
                "payload_bytes": 250000,
                "duplicate_title_rate": 0.7,
                "http_item_link_count": 2,
            }
        }
        warnings = compare_feed_snapshots(previous, current)
        kinds = {warning["kind"] for warning in warnings}
        self.assertTrue({"validation-regression", "item-count-collapse", "freshness-regression"} <= kinds)
        self.assertIn("payload-growth", kinds)
        self.assertIn("duplicate-title-threshold", kinds)
        self.assertIn("item-link-transport-regression", kinds)


class GeneratedArtifactsTest(unittest.TestCase):
    def test_manifest_matches_master_and_lite_artifacts(self) -> None:
        manifest = json.loads((ROOT / "feed-manifest.json").read_text(encoding="utf-8"))
        opml = opml_entries(ROOT / "NetNewsWire-Finance-Cyber.opml")
        table = source_table_entries(ROOT / "NetNewsWire-Finance-Cyber-Source-Table.md")
        self.assertEqual(len(manifest["feeds"]), 51)
        self.assertEqual(len(opml), 51)
        self.assertEqual(len(table), 51)
        self.assertEqual([feed["url"] for feed in manifest["feeds"]], [entry["url"] for entry in opml])
        self.assertEqual([feed["url"] for feed in manifest["feeds"]], [entry["url"] for entry in table])
        self.assertEqual(
            sum(feed["profiles"].get("iphone-lite", False) for feed in manifest["feeds"]),
            30,
        )

    def test_notification_matrix_is_generated_from_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            table_path = directory / "notifications.md"
            json_path = directory / "notifications.json"
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "generate-bundle.py"),
                    "--manifest",
                    str(ROOT / "feed-manifest.json"),
                    "--notification-table",
                    str(table_path),
                    "--notification-json",
                    str(json_path),
                ],
                check=True,
                cwd=ROOT,
            )
            matrix = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(matrix["profiles"]["master"]["feed_count"], 51)
            self.assertEqual(matrix["profiles"]["iphone-lite"]["feed_count"], 30)
            self.assertEqual(len(matrix["feeds"]), 51)
            self.assertIn("## Import checklist", table_path.read_text(encoding="utf-8"))

    def test_manifest_lint_accepts_committed_artifacts(self) -> None:
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "validate-manifest.py"),
                "--manifest",
                str(ROOT / "feed-manifest.json"),
                "--root",
                str(ROOT),
            ],
            check=True,
            cwd=ROOT,
        )


class DigestPreparationTest(unittest.TestCase):
    def test_digest_state_prevents_repeat_items(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            input_path = directory / "articles.json"
            output_path = directory / "digest.json"
            state_path = directory / "state.json"
            input_path.write_text(
                json.dumps(
                    [
                        {
                            "title": "Story one",
                            "link": "https://example.test/one?utm_source=rss",
                            "feed": "Nasdaq Trader — Trade Halts",
                            "feed_url": "https://www.nasdaqtrader.com/rss.aspx?feed=tradehalts",
                            "published": "2026-08-15T10:00:00Z",
                            "content": "A very long body that should be bounded before it reaches the digest prompt.",
                        },
                        {
                            "title": "Story two",
                            "link": "https://example.test/two",
                            "feed": "Example",
                            "published": "2026-08-15T09:00:00Z",
                        },
                    ]
                ),
                encoding="utf-8",
            )
            command = [
                sys.executable,
                str(ROOT / "prepare-rss-digest-input.py"),
                "--input",
                str(input_path),
                "--output",
                str(output_path),
                "--state",
                str(state_path),
                "--max-item-chars",
                "24",
            ]
            subprocess.run(command, check=True, cwd=ROOT)
            first = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(first["article_count"], 2)
            enriched = next(article for article in first["articles"] if article["title"] == "Story one")
            self.assertEqual(enriched["manifest_id"], "finance-01-core-market-trading-nasdaq-trader-trade-halts")
            self.assertEqual(enriched["notification_policy"], "on")
            self.assertTrue(enriched["text_truncated"])
            self.assertEqual(first["manifest_enriched_count"], 1)
            self.assertEqual(first["unmatched_source_count"], 1)
            subprocess.run(command, check=True, cwd=ROOT)
            second = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(second["article_count"], 0)
            self.assertEqual(second["skipped_seen_count"], 2)

    def test_digest_marks_conservative_duplicate_story_groups(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            input_path = directory / "articles.json"
            output_path = directory / "digest.json"
            input_path.write_text(
                json.dumps(
                    [
                        {
                            "title": "NCSC issues advice following global targeting of Fortinet firewalls",
                            "link": "https://example.test/ncsc-fortinet",
                            "feed": "Ireland NCSC — Alerts & Advisories",
                            "published": "2026-08-15T10:00:00Z",
                        },
                        {
                            "title": "NCSC: advice follows global targeting of Fortinet firewalls",
                            "link": "https://example.test/cisa-fortinet",
                            "feed": "CISA — All Advisories",
                            "published": "2026-08-15T09:00:00Z",
                        },
                    ]
                ),
                encoding="utf-8",
            )
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "prepare-rss-digest-input.py"),
                    "--input",
                    str(input_path),
                    "--output",
                    str(output_path),
                    "--dry-run",
                ],
                check=True,
                cwd=ROOT,
            )
            package = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(package["duplicate_cluster_count"], 1)
            self.assertEqual(package["duplicate_article_count"], 2)
            group_ids = {article["duplicate_group_id"] for article in package["articles"]}
            self.assertEqual(len(group_ids), 1)
            self.assertEqual(package["manifest_enriched_count"], 2)


class ValidationHistoryTest(unittest.TestCase):
    def test_history_counts_consecutive_failures_and_resets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            report_path = directory / "report.json"
            history_path = directory / "history.json"
            report_path.write_text(
                json.dumps({"summary": {"failed_feed_count": 1, "metadata_mismatch_count": 0, "noisy_feed_count": 0}}),
                encoding="utf-8",
            )
            command = [
                sys.executable,
                str(ROOT / "record-validation-result.py"),
                "--report",
                str(report_path),
                "--history",
                str(history_path),
                "--profile",
                "master",
                "--healthy",
                "no",
            ]
            for expected in (1, 2, 3):
                subprocess.run(command, check=True, cwd=ROOT)
                history = json.loads(history_path.read_text(encoding="utf-8"))
                self.assertEqual(history["profiles"]["master"]["consecutive_failures"], expected)
            command[-1] = "yes"
            subprocess.run(command, check=True, cwd=ROOT)
            history = json.loads(history_path.read_text(encoding="utf-8"))
            self.assertEqual(history["profiles"]["master"]["consecutive_failures"], 0)


if __name__ == "__main__":
    unittest.main()
