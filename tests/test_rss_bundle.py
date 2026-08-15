from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from rss_validation import (
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
                            "feed": "Example",
                            "published": "2026-08-15T10:00:00Z",
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
            ]
            subprocess.run(command, check=True, cwd=ROOT)
            first = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(first["article_count"], 2)
            subprocess.run(command, check=True, cwd=ROOT)
            second = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(second["article_count"], 0)
            self.assertEqual(second["skipped_seen_count"], 2)


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
