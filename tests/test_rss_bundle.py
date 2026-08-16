from __future__ import annotations

import json
import importlib.util
import copy
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from bundle_config import (
    ManifestValidationError,
    load_manifest,
    manifest_errors,
    profile_digest_budget,
    profile_device_budget,
    profile_inheritance,
    profile_includes_feed,
    profile_settings,
    validation_settings,
    validate_manifest,
)
from rss_validation import (
    compare_feed_snapshots,
    extract_feed,
    normalize_link,
    normalize_title,
    opml_entries,
    safe_xml_root,
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

    def test_rss_extraction_uses_direct_channel_items(self) -> None:
        root = ET.fromstring(
            """<rss version="2.0"><channel><title>Example</title>
              <item><title>Visible</title><link>https://example.test/visible</link><pubDate>Sat, 15 Aug 2026 10:00:00 GMT</pubDate></item>
              <extension><item><title>Nested should not count</title></item></extension>
            </channel></rss>"""
        )
        _, items = extract_feed(root)
        self.assertEqual([item["title"] for item in items], ["Visible"])

    def test_normalization_removes_tracking_and_punctuation(self) -> None:
        self.assertEqual(
            normalize_link("https://Example.test/story/?utm_source=rss&x=1#comments"),
            "https://example.test/story?x=1",
        )
        self.assertEqual(
            normalize_link("https://example.test/story?ref=share"),
            "https://example.test/story?ref=share",
        )
        self.assertEqual(normalize_title("Alert: Fortinet & VPN!"), "alert fortinet and vpn")
        self.assertTrue(
            similar_titles(
                "NCSC issues advice following global targeting of Fortinet firewalls",
                "NCSC: advice follows global targeting of Fortinet firewalls",
            )
        )

    def test_safe_xml_root_rejects_dtd_documents(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "unsafe.xml"
            path.write_text(
                '<!DOCTYPE feed [<!ENTITY xxe "blocked">]><feed><title>&xxe;</title></feed>',
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                safe_xml_root(path)

    def test_safe_xml_root_allows_html_doctype_inside_cdata(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "feed.xml"
            path.write_text(
                "<rss version='2.0'><channel><title>Example</title>"
                "<item><title>Story</title>"
                "<description><![CDATA[<!DOCTYPE html><html><body>Story</body></html>]]>"
                "</description></item></channel></rss>",
                encoding="utf-8",
            )
            self.assertEqual(safe_xml_root(path).tag, "rss")

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


class ManifestConfigurationTest(unittest.TestCase):
    def test_device_profile_inheritance_and_budget_are_explicit(self) -> None:
        manifest = load_manifest(ROOT / "feed-manifest.json")
        self.assertEqual(profile_inheritance(manifest, "iphone-air"), ("iphone-lite",))
        self.assertEqual(profile_device_budget(profile_settings(manifest)["iphone-air"])["max_feeds"], 50)
        self.assertEqual(profile_digest_budget(profile_settings(manifest)["iphone-air"])["max_items"], 30)
        invalid = copy.deepcopy(manifest)
        invalid["profiles"]["iphone-air"]["device_budget"]["max_single_payload_bytes"] = 5 * 1024 * 1024
        with self.assertRaises(ManifestValidationError):
            validate_manifest(invalid)

    def test_manifest_validation_rejects_boolean_and_non_finite_thresholds(self) -> None:
        manifest = load_manifest(ROOT / "feed-manifest.json")
        invalid = copy.deepcopy(manifest)
        invalid["validation"]["min_items_for_noise"] = True
        invalid["validation"]["max_age_days"] = float("nan")
        errors = manifest_errors(invalid)
        self.assertIn("validation.min_items_for_noise must be an integer", errors)
        self.assertIn("validation.max_age_days must be numeric", errors)

    def test_load_manifest_reports_all_structural_errors_without_traceback(self) -> None:
        manifest = load_manifest(ROOT / "feed-manifest.json")
        invalid = copy.deepcopy(manifest)
        invalid["manifest_version"] = True
        invalid["feeds"][0]["url"] = "http://example.test/feed.xml"
        invalid["feeds"][1]["url"] = invalid["feeds"][0]["url"]
        with self.assertRaises(ManifestValidationError) as context:
            from bundle_config import validate_manifest

            validate_manifest(invalid)
        message = str(context.exception)
        self.assertIn("manifest_version must be a positive integer", message)
        self.assertIn("feed URL must be HTTPS", message)
        self.assertIn("duplicate feed URL", message)


class GeneratedArtifactsTest(unittest.TestCase):
    def test_report_generator_rejects_missing_arguments_without_traceback(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "generate-rss-validation-report.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("usage:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_manifest_matches_every_profile_artifact(self) -> None:
        manifest = load_manifest(ROOT / "feed-manifest.json")
        profiles = profile_settings(manifest)
        artifacts: dict[str, tuple[list[dict], list[dict]]] = {}
        for profile, config in profiles.items():
            opml = opml_entries(ROOT / config["opml_file"])
            table = source_table_entries(ROOT / config["source_table_file"])
            expected_urls = [
                feed["url"]
                for feed in manifest["feeds"]
                if profile_includes_feed(manifest, profile, feed)
            ]
            self.assertEqual(len(opml), len(expected_urls))
            self.assertEqual(len(table), len(expected_urls))
            self.assertEqual([entry["url"] for entry in opml], expected_urls)
            self.assertEqual([entry["url"] for entry in table], expected_urls)
            artifacts[profile] = (opml, table)

        self.assertEqual(len(artifacts["master"][0]), len(manifest["feeds"]))
        self.assertEqual(len(artifacts["iphone-lite"][0]), 39)
        self.assertEqual(len(artifacts["iphone-air"][0]), 50)
        air_budget = profile_device_budget(profiles["iphone-air"])
        self.assertEqual(air_budget["max_feeds"], 50)
        self.assertTrue(
            any(
                feed["id"] == "cyber-security-04-optional-specialist-alerts-research-openssf-supply-chain-security"
                and profile_includes_feed(manifest, "iphone-air", feed)
                for feed in manifest["feeds"]
            )
        )
        trade_halts = next(
            entry for entry in artifacts["master"][0] if entry["title"] == "Nasdaq Trader — Trade Halts"
        )
        self.assertEqual(trade_halts["item_link_policy"], "structured-alert")

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
            manifest = load_manifest(ROOT / "feed-manifest.json")
            profiles = profile_settings(manifest)
            self.assertEqual(
                set(matrix["profiles"]),
                set(profiles),
            )
            for profile, config in profiles.items():
                expected = sum(
                    1 for feed in manifest["feeds"] if profile_includes_feed(manifest, profile, feed)
                )
                self.assertEqual(matrix["profiles"][profile]["feed_count"], expected)
            self.assertEqual(len(matrix["feeds"]), len(manifest["feeds"]))
            trade_halt_matrix = next(
                feed for feed in matrix["feeds"]
                if feed["id"] == "finance-01-core-market-trading-nasdaq-trader-trade-halts"
            )
            self.assertTrue(trade_halt_matrix["profiles"]["iphone-air"])
            self.assertEqual(matrix["profiles"]["iphone-air"]["device_budget"]["max_feeds"], 50)
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

    def test_documentation_and_airdrop_handoff_are_current(self) -> None:
        docs = subprocess.run(
            [sys.executable, str(ROOT / "validate-docs.py"), "--root", str(ROOT)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(docs.returncode, 0, docs.stderr or docs.stdout)
        manifest = load_manifest(ROOT / "feed-manifest.json")
        air_file = ROOT / profile_settings(manifest)["iphone-air"]["opml_file"]
        handoff_file = ROOT / "AirDrop" / air_file.name
        self.assertEqual(air_file.read_bytes(), handoff_file.read_bytes())

    def test_report_generator_is_import_safe_and_writes_portable_paths(self) -> None:
        module_path = ROOT / "generate-rss-validation-report.py"
        spec = importlib.util.spec_from_file_location("validation_report", module_path)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.portable_path(str(ROOT / "feed-manifest.json"), ROOT), "feed-manifest.json")

        manifest = load_manifest(ROOT / "feed-manifest.json")
        feed = manifest["feeds"][0]
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            xml_path = directory / "feed.xml"
            xml_path.write_text(
                "<rss version='2.0'><channel><title>Example</title>"
                "<item><title>Example story</title><link>https://example.test/story</link>"
                "<pubDate>Sat, 15 Aug 2026 10:00:00 GMT</pubDate></item>"
                "</channel></rss>",
                encoding="utf-8",
            )
            fetch_manifest = directory / "fetch.tsv"
            fetch_manifest.write_text(
                "\t".join(
                    [
                        "1",
                        feed["url"],
                        str(xml_path),
                        "200",
                        feed["url"],
                        "yes",
                        "rss",
                        "standard",
                        "yes",
                        "yes",
                        "0.0",
                        "2026-08-15T10:00:00+00:00",
                        "yes",
                        "application/rss+xml",
                        "",
                        "",
                        "100",
                        "0.1",
                        "100",
                        "identity",
                        "0.001",
                        "no",
                        "within-limit",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            markdown_path = directory / "report.md"
            json_path = directory / "report.json"
            result = subprocess.run(
                [
                    sys.executable,
                    str(module_path),
                    str(ROOT / "NetNewsWire-Finance-Cyber.opml"),
                    str(ROOT / "NetNewsWire-Finance-Cyber-Source-Table.md"),
                    str(fetch_manifest),
                    str(markdown_path),
                    str(json_path),
                    "180",
                    "0.5",
                    "10",
                    str(ROOT / "validate-rss-bundle.sh"),
                    str(ROOT / "feed-manifest.json"),
                    "master",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["bundle"], "NetNewsWire-Finance-Cyber.opml")
            self.assertEqual(payload["validator"], "validate-rss-bundle.sh")
            self.assertIn(f"[{json_path.name}]({json_path.name})", markdown_path.read_text(encoding="utf-8"))
            self.assertNotIn("/Users/", json_path.read_text(encoding="utf-8"))
            self.assertNotIn("/Users/", markdown_path.read_text(encoding="utf-8"))


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
            self.assertIn("iphone-air", enriched["profiles"])
            self.assertTrue(enriched["text_truncated"])
            self.assertEqual(first["manifest_enriched_count"], 1)
            self.assertEqual(first["unmatched_source_count"], 1)
            subprocess.run(command, check=True, cwd=ROOT)
            second = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(second["article_count"], 0)
            self.assertEqual(second["skipped_seen_count"], 2)

    def test_digest_profile_budget_filters_and_writes_shortcut_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            input_path = directory / "articles.json"
            output_path = directory / "digest.json"
            state_path = directory / "state.json"
            shortcut_path = directory / "shortcut.txt"
            input_path.write_text(
                json.dumps(
                    [
                        {
                            "title": "Nasdaq halt notice",
                            "link": "https://example.test/halt",
                            "feed": "Nasdaq Trader — Trade Halts",
                            "feed_url": "https://www.nasdaqtrader.com/rss.aspx?feed=tradehalts",
                            "published": "2026-08-15T10:00:00Z",
                            "summary": "An official market alert.",
                        },
                        {
                            "title": "Mandiant research update",
                            "link": "https://example.test/mandiant",
                            "feed": "Google Threat Intelligence — Mandiant",
                            "feed_url": "https://feeds.feedburner.com/threatintelligence/pvexyqv7v0v",
                            "published": "2026-08-15T09:00:00Z",
                            "summary": "A master-only research item.",
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
                    "--state",
                    str(state_path),
                    "--shortcut-output",
                    str(shortcut_path),
                    "--profile",
                    "iphone-air",
                    "--dry-run",
                ],
                check=True,
                cwd=ROOT,
            )
            package = json.loads(output_path.read_text(encoding="utf-8"))
            shortcut = shortcut_path.read_text(encoding="utf-8")
            self.assertEqual(package["profile"], "iphone-air")
            self.assertEqual(package["budget_source"], "profile")
            self.assertEqual(package["max_items"], 30)
            self.assertEqual(package["max_item_chars"], 6000)
            self.assertEqual(package["max_total_chars"], 90000)
            self.assertEqual(package["article_count"], 1)
            self.assertEqual(package["skipped_profile_count"], 1)
            self.assertIn("iphone-air", package["articles"][0]["profiles"])
            self.assertIn("Profile: iphone-air", shortcut)
            self.assertIn("Nasdaq halt notice", shortcut)
            self.assertIn("Link: https://example.test/halt", shortcut)
            self.assertNotIn("Mandiant research update", shortcut)

    def test_digest_marks_conservative_duplicate_story_groups(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            input_path = directory / "articles.json"
            output_path = directory / "digest.json"
            state_path = directory / "state.json"
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
                    "--state",
                    str(state_path),
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

    def test_digest_partial_export_does_not_advance_an_implicit_time_cursor(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            input_path = directory / "articles.json"
            output_path = directory / "digest.json"
            state_path = directory / "state.json"
            input_path.write_text(
                json.dumps(
                    [
                        {"title": "Newest", "link": "https://example.test/new", "published": "2026-08-15T10:00:00Z"},
                        {"title": "Older", "link": "https://example.test/old", "published": "2026-08-15T09:00:00Z"},
                        {"title": "Oldest", "link": "https://example.test/oldest", "published": "2026-08-15T08:00:00Z"},
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
                "--max-items",
                "1",
            ]
            subprocess.run(command, check=True, cwd=ROOT)
            first = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(first["article_count"], 1)

            command[-1] = "3"
            subprocess.run(command, check=True, cwd=ROOT)
            second = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(second["article_count"], 2)
            self.assertEqual(second["skipped_old_count"], 0)

    def test_digest_duplicate_groups_respect_publication_window(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            input_path = directory / "articles.json"
            output_path = directory / "digest.json"
            state_path = directory / "state.json"
            input_path.write_text(
                json.dumps(
                    [
                        {"title": "Repeated alert", "link": "https://example.test/one", "published": "2026-08-15T10:00:00Z"},
                        {"title": "Repeated alert", "link": "https://example.test/two", "published": "2026-08-25T10:00:00Z"},
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
                    "--state",
                    str(state_path),
                    "--dry-run",
                ],
                check=True,
                cwd=ROOT,
            )
            package = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(package["duplicate_cluster_count"], 0)

    def test_digest_rejects_invalid_budget_and_since_arguments_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            input_path = directory / "articles.json"
            state_path = directory / "state.json"
            input_path.write_text("[]\n", encoding="utf-8")
            for extra_args, expected_text in ((["--max-items", "0"], "--max-items"), (["--since", "not-a-date"], "--since")):
                result = subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / "prepare-rss-digest-input.py"),
                        "--input",
                        str(input_path),
                        "--state",
                        str(state_path),
                        "--dry-run",
                        *extra_args,
                    ],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected_text, result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_digest_rejects_corrupt_state_without_writing_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            input_path = directory / "articles.json"
            state_path = directory / "state.json"
            output_path = directory / "digest.json"
            input_path.write_text("[]\n", encoding="utf-8")
            state_path.write_text('{"version": true, "seen": {}}\n', encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "prepare-rss-digest-input.py"),
                    "--input",
                    str(input_path),
                    "--state",
                    str(state_path),
                    "--output",
                    str(output_path),
                    "--dry-run",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("digest state version", result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            self.assertFalse(output_path.exists())


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

    def test_history_rejects_stale_current_report(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            report_path = directory / "report.json"
            history_path = directory / "history.json"
            report_path.write_text(
                json.dumps(
                    {
                        "schema_version": 2,
                        "generated_at": "2020-01-01T00:00:00+00:00",
                        "profile": "master",
                        "feeds": [{"url": "https://example.test/feed.xml"}],
                        "summary": {},
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "record-validation-result.py"),
                    "--report",
                    str(report_path),
                    "--history",
                    str(history_path),
                    "--profile",
                    "master",
                    "--current-run",
                    "--healthy",
                    "yes",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(history_path.exists())


if __name__ == "__main__":
    unittest.main()
