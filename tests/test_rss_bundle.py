from __future__ import annotations

import json
import importlib.util
import copy
import os
import plistlib
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest import mock
from zoneinfo import ZoneInfo

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
    normalize_content_type,
    normalize_link,
    normalize_title,
    opml_entries,
    parse_date,
    safe_xml_root,
    similar_titles,
    source_table_entries,
)
from runtime_health import write_health
import state_utils
from state_utils import atomic_write_bytes, atomic_write_text, directory_lock


ROOT = Path(__file__).resolve().parents[1]
_PROJECT_STATUS_SPEC = importlib.util.spec_from_file_location(
    "project_status_cli",
    ROOT / "project-status.py",
)
if _PROJECT_STATUS_SPEC is None or _PROJECT_STATUS_SPEC.loader is None:
    raise RuntimeError("cannot load project-status.py")
_PROJECT_STATUS_MODULE = importlib.util.module_from_spec(_PROJECT_STATUS_SPEC)
_PROJECT_STATUS_SPEC.loader.exec_module(_PROJECT_STATUS_MODULE)
build_status = _PROJECT_STATUS_MODULE.build_status
_HOURLY_RUNNER_SPEC = importlib.util.spec_from_file_location(
    "hourly_digest_runner",
    ROOT / "run-hourly-rss-digest.py",
)
if _HOURLY_RUNNER_SPEC is None or _HOURLY_RUNNER_SPEC.loader is None:
    raise RuntimeError("cannot load run-hourly-rss-digest.py")
_HOURLY_RUNNER_MODULE = importlib.util.module_from_spec(_HOURLY_RUNNER_SPEC)
_HOURLY_RUNNER_SPEC.loader.exec_module(_HOURLY_RUNNER_MODULE)


class ProjectStatusTest(unittest.TestCase):
    def test_status_matches_manifest_and_committed_snapshots(self) -> None:
        status = build_status(ROOT)
        manifest = load_manifest(ROOT / "feed-manifest.json")

        self.assertIn(status["status"], {"ready", "attention"})
        self.assertEqual(status["manifest"]["feed_count"], len(manifest["feeds"]))
        self.assertEqual(
            sum(status["manifest"]["section_counts"].values()),
            len(manifest["feeds"]),
        )
        self.assertEqual(status["profiles"]["master"]["feed_count"], len(manifest["feeds"]))
        self.assertEqual(
            status["artifacts"]["present_count"],
            status["artifacts"]["expected_count"],
        )
        self.assertEqual(
            status["validation"]["master"]["feed_count"],
            status["profiles"]["master"]["feed_count"],
        )

    def test_status_contains_machine_readable_validation_details(self) -> None:
        status = build_status(ROOT)
        self.assertIn("findings", status)
        self.assertIn("validation", status)
        self.assertIn("generated_at_local", status["validation"]["master"])

    def test_status_does_not_call_attention_entries_failed(self) -> None:
        report = {
            "summary": {"failed_feed_count": 1},
            "feeds": [],
            "failed_feeds": [
                {"feed_title": "Broken feed", "passed": "no"},
                {"feed_title": "Tolerated future feed", "passed": "yes"},
            ],
        }
        details = _PROJECT_STATUS_MODULE._report_summary(
            report,
            expected_count=2,
            path=ROOT / "report.json",
            root=ROOT,
        )
        self.assertEqual(details["failed_count"], 1)
        self.assertEqual(details["failure_names"], ["Broken feed"])
        self.assertEqual(details["attention_count"], 2)


class RuntimeReliabilityTest(unittest.TestCase):
    def test_atomic_write_preserves_previous_value_when_replace_is_interrupted(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "state.json"
            destination.write_text("old\n", encoding="utf-8")
            with mock.patch.object(state_utils.os, "replace", side_effect=OSError("interrupted")):
                with self.assertRaises(OSError):
                    atomic_write_text(destination, "new\n")
            self.assertEqual(destination.read_text(encoding="utf-8"), "old\n")
            self.assertEqual(list(destination.parent.glob(f".{destination.name}.*.tmp")), [])

    def test_health_preserves_last_success_after_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            health_path = directory / "health.json"
            package_path = directory / "package.json"
            package_path.write_text(
                json.dumps(
                    {
                        "article_count": 3,
                        "collection": {
                            "status": "partial",
                            "source_profile": "master",
                            "feeds_considered": 10,
                            "feeds_succeeded": 9,
                            "feeds_failed": 1,
                            "article_candidates": 12,
                        },
                        "articles": [
                            {
                                "title": "PRIVATE ARTICLE BODY",
                                "summary": "should never enter health.json",
                                "link": "https://example.test/private",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            write_health(
                health_path,
                status="running",
                run_id="run-1",
                started_at="2026-08-24T08:00:00+00:00",
            )
            write_health(
                health_path,
                status="succeeded",
                run_id="run-1",
                started_at="2026-08-24T08:00:00+00:00",
                finished_at="2026-08-24T08:01:00+00:00",
                package_path=package_path,
            )
            write_health(
                health_path,
                status="failed",
                run_id="run-2",
                started_at="2026-08-24T08:30:00+00:00",
                finished_at="2026-08-24T08:30:05+00:00",
                exit_code=124,
                message="timeout",
            )
            payload = json.loads(health_path.read_text(encoding="utf-8"))
            health_text = health_path.read_text(encoding="utf-8")

        self.assertEqual(payload["status"], "failed")
        self.assertEqual(payload["last_success_run_id"], "run-1")
        self.assertEqual(payload["article_count"], None)
        self.assertNotIn("PRIVATE ARTICLE BODY", health_text)
        self.assertNotIn("should never enter health.json", health_text)

    def test_interrupted_state_transaction_restores_previous_state(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            state_path = directory / "fetch-state.json"
            transaction = directory / ".hourly-commit.crashed"
            transaction.mkdir()
            state_path.write_text("new\n", encoding="utf-8")
            (transaction / "fetch-state.backup").write_text("old\n", encoding="utf-8")
            (transaction / "journal.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "status": "prepared",
                        "states": [
                            {
                                "destination": str(state_path),
                                "present": True,
                                "backup": "fetch-state.backup",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            _HOURLY_RUNNER_MODULE._recover_state_transactions(directory)
            self.assertEqual(state_path.read_text(encoding="utf-8"), "old\n")
            self.assertFalse(transaction.exists())

    def test_pipeline_lock_rejects_a_second_owner(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            lock_directory = Path(temporary) / ".hourly-run.lock"
            with directory_lock(lock_directory):
                with self.assertRaises(TimeoutError):
                    with directory_lock(lock_directory, timeout_seconds=0):
                        pass

    def test_pipeline_lock_does_not_steal_an_ownerless_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            lock_directory = Path(temporary) / ".hourly-run.lock"
            lock_directory.mkdir()
            with self.assertRaises(TimeoutError):
                with directory_lock(lock_directory, timeout_seconds=0):
                    pass

    def test_shortcut_runner_returns_timeout_without_accepting_stale_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            fake_bin = directory / "bin"
            fake_bin.mkdir()
            shortcut_command = fake_bin / "shortcuts"
            shortcut_command.write_text("#!/bin/sh\nsleep 1\n", encoding="utf-8")
            shortcut_command.chmod(0o755)
            input_path = directory / "input.txt"
            output_path = directory / "output.txt"
            input_path.write_text("input\n", encoding="utf-8")
            output_path.write_text("stale\n", encoding="utf-8")
            environment = os.environ.copy()
            environment["PATH"] = f"{fake_bin}:{environment.get('PATH', '')}"
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "automation/run-shortcut.py"),
                    "Digest",
                    str(input_path),
                    str(output_path),
                    "--timeout",
                    "0.05",
                ],
                cwd=ROOT,
                env=environment,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 124)
            self.assertFalse(output_path.exists())

    def test_hourly_wrapper_trims_active_log_after_a_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            environment = os.environ.copy()
            environment.update(
                {
                    "NETNEWSWIRE_DIGEST_DIR": str(directory),
                    "NETNEWSWIRE_LOG_PATH": str(directory / "hourly.log"),
                    "NETNEWSWIRE_LOG_MAX_BYTES": "10",
                    "NETNEWSWIRE_SOURCE_PROFILE": "does-not-exist",
                    "PYTHON_BIN": sys.executable,
                }
            )
            result = subprocess.run(
                ["/bin/sh", str(ROOT / "automation/run-hourly-digest.sh")],
                cwd=ROOT,
                env=environment,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertLessEqual((directory / "hourly.log").stat().st_size, 10)
            health = json.loads((directory / "health.json").read_text(encoding="utf-8"))
            self.assertEqual(health["status"], "failed")
            self.assertFalse((directory / ".hourly-run.lock").exists())

    def test_launch_agent_template_contains_timeout_and_bounded_log_settings(self) -> None:
        template = (
            ROOT / "automation/com.netnewswire.finance-cyber.hourly-digest.plist.template"
        ).read_text(encoding="utf-8")
        for marker, value in {
            "__STAGED_ROOT__": "/tmp/hourly-app",
            "__RUNTIME_DIR__": "/tmp/hourly-runtime",
            "__PYTHON_BIN__": "/usr/bin/python3",
            "__INTERVAL__": "1800",
            "__JOB_TIMEOUT__": "3600",
            "__SHORTCUT_NAME__": "Digest",
            "__SHORTCUT_TIMEOUT__": "900",
            "__LOG_MAX_BYTES__": "1048576",
        }.items():
            template = template.replace(marker, value)
        payload = plistlib.loads(template.encode("utf-8"))
        self.assertEqual(payload["TimeOut"], 3600)
        self.assertEqual(payload["ThrottleInterval"], 60)
        self.assertEqual(
            payload["EnvironmentVariables"]["NETNEWSWIRE_SHORTCUT_TIMEOUT_SECONDS"],
            "900",
        )
        self.assertTrue(payload["StandardOutPath"].endswith("/hourly.log"))



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

    def test_rss_uses_https_guid_as_permalink_when_link_is_missing(self) -> None:
        root = ET.fromstring(
            """<rss version="2.0"><channel><title>Example</title>
              <item><title>Official episode</title>
              <guid>https://example.test/audio/episode.mp3/view</guid>
              <pubDate>Sat, 15 Aug 2026 10:00:00 GMT</pubDate></item>
              <item><title>Opaque identifier</title>
              <guid isPermaLink="false">opaque-123</guid>
              <pubDate>Sat, 15 Aug 2026 09:00:00 GMT</pubDate></item>
            </channel></rss>"""
        )
        _, items = extract_feed(root)
        self.assertEqual(items[0]["link"], "https://example.test/audio/episode.mp3/view")
        self.assertEqual(items[1]["link"], "")

    def test_rss_can_interpret_timezone_less_dates_in_source_timezone(self) -> None:
        root = ET.fromstring(
            """<rss version="2.0"><channel><title>Example</title>
              <item><title>India-local release</title>
              <link>https://example.test/release</link>
              <pubDate>Tue, 18 Aug 2026 09:00:00</pubDate></item>
            </channel></rss>"""
        )
        _, items = extract_feed(root, naive_timezone=ZoneInfo("Asia/Kolkata"))
        self.assertEqual(items[0]["date"].isoformat(), "2026-08-18T03:30:00+00:00")

    def test_rss_accepts_indian_publisher_date_format(self) -> None:
        parsed = parse_date("18 Aug, 2026 +0530")
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed.isoformat(), "2026-08-17T18:30:00+00:00")

    def test_rss_accepts_month_first_publisher_date_format(self) -> None:
        parsed = parse_date("August 14, 2026")
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed.isoformat(), "2026-08-14T00:00:00+00:00")

    def test_rss_resolves_relative_item_links_against_feed_url(self) -> None:
        root = ET.fromstring(
            """<rss version="2.0"><channel><title>Example</title>
              <item><title>Archived release</title>
              <link>/news/archived-release</link>
              <pubDate>Tue, 18 Aug 2026 09:00:00 GMT</pubDate></item>
            </channel></rss>"""
        )
        _, items = extract_feed(root, base_url="https://example.test/rss/feed.xml")
        self.assertEqual(items[0]["link"], "https://example.test/news/archived-release")

    def test_rss_prefers_relative_title_anchor_over_malformed_link(self) -> None:
        root = ET.fromstring(
            """<rss version="2.0"><channel><title>Example</title>
              <item><title><a href="/news/official-release">Official release</a></title>
              <link>https://example.test/%3Ca%20href%3D%22/news/official-release%22%3EOfficial%20release%3C/a%3E</link>
              <pubDate>Fri, 08/14/2026 - 16:01</pubDate></item>
            </channel></rss>"""
        )
        _, items = extract_feed(root, base_url="https://example.test/rss.xml")
        self.assertEqual(items[0]["link"], "https://example.test/news/official-release")
        self.assertEqual(items[0]["date"].isoformat(), "2026-08-14T16:01:00+00:00")

    def test_rss_extraction_uses_direct_channel_items(self) -> None:
        root = ET.fromstring(
            """<rss version="2.0"><channel><title>Example</title>
              <item><title>Visible</title><link>https://example.test/visible</link><pubDate>Sat, 15 Aug 2026 10:00:00 GMT</pubDate></item>
              <extension><item><title>Nested should not count</title></item></extension>
            </channel></rss>"""
        )
        _, items = extract_feed(root)
        self.assertEqual([item["title"] for item in items], ["Visible"])

    def test_rss_extraction_accepts_explicit_time_in_escaped_description(self) -> None:
        root = ET.fromstring(
            """<rss version="2.0"><channel><title>Example</title>
              <item><title>Visible</title><link>https://example.test/visible</link>
              <description>&lt;span&gt;&lt;time datetime="2026-08-14T10:54:44+02:00"&gt;14 August 2026&lt;/time&gt;&lt;/span&gt;</description>
              </item></channel></rss>"""
        )
        _, items = extract_feed(root)
        self.assertEqual(items[0]["date"].isoformat(), "2026-08-14T08:54:44+00:00")

    def test_rss_extraction_accepts_explicit_time_in_escaped_date_field(self) -> None:
        root = ET.fromstring(
            """<rss version="2.0"><channel><title>Example</title>
              <item><title>Visible</title><link>https://example.test/visible</link>
              <pubDate>Thu, 30 Jul 26 &lt;time datetime="2026-07-30T07:20:00+02:00"&gt;07:20:00 +0200&lt;/time&gt;</pubDate>
              </item></channel></rss>"""
        )
        _, items = extract_feed(root)
        self.assertEqual(items[0]["date"].isoformat(), "2026-07-30T05:20:00+00:00")

    def test_cbsl_rss_uses_only_explicit_report_dates_when_item_dates_are_omitted(self) -> None:
        root = ET.fromstring(
            """<rss version="2.0"><channel><title>Central Bank of Sri Lanka</title>
              <item><title>Weekly Economic Indicators -21 August 2026</title>
              <link>https://www.cbsl.gov.lk/sites/default/files/WEI_20260821_e.pdf</link></item>
              <item><title>Monthly Economic Indicators - June 2026</title>
              <link>https://www.cbsl.gov.lk/sites/default/files/MEI_202606_e.pdf</link></item>
              <item><title>Monetary Policy Review - No. 4 of 2026</title>
              <link>https://www.cbsl.gov.lk/sites/default/files/press_20260722_Monetary_Policy_Review.pdf</link></item>
            </channel></rss>"""
        )
        _, items = extract_feed(root, base_url="https://www.cbsl.gov.lk/en/statistics/economic-indicators/weirss")
        self.assertEqual(
            [item["date"].isoformat() for item in items],
            [
                "2026-08-21T00:00:00+00:00",
                "2026-06-01T00:00:00+00:00",
                "2026-07-22T00:00:00+00:00",
            ],
        )

    def test_embedded_date_fallback_is_not_used_for_other_hosts(self) -> None:
        root = ET.fromstring(
            """<rss version="2.0"><channel><title>Other</title>
              <item><title>Weekly Economic Indicators -21 August 2026</title>
              <link>https://example.test/WEI_20260821_e.pdf</link></item>
            </channel></rss>"""
        )
        _, items = extract_feed(root, base_url="https://example.test/feed.xml")
        self.assertIsNone(items[0]["date"])

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

    def test_safe_xml_root_allows_comment_preamble_before_declaration(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "feed.xml"
            path.write_text(
                "<!-- generated by the official feed renderer -->\n"
                "<?xml version='1.0' encoding='utf-8'?>"
                "<rss version='2.0'><channel><title>Example</title></channel></rss>",
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

    def test_structured_alert_duplicate_rate_is_not_treated_as_editorial_noise(self) -> None:
        url = "https://example.test/structured-alerts.xml"
        previous = {
            url: {
                "url": url,
                "title": "Structured Alerts",
                "passed": "yes",
                "duplicate_title_rate": 0.0,
                "duplicate_link_rate": 0.0,
                "item_link_status": "structured-alert",
                "http_item_link_count": 0,
                "missing_item_link_count": 1,
            }
        }
        current = {
            url: {
                **previous[url],
                "duplicate_title_rate": 0.8,
                "duplicate_link_rate": 0.8,
                "missing_item_link_count": 4,
            }
        }
        warnings = compare_feed_snapshots(previous, current)
        self.assertNotIn(
            "duplicate-title-threshold",
            {warning["kind"] for warning in warnings},
        )
        self.assertNotIn(
            "item-link-transport-regression",
            {warning["kind"] for warning in warnings},
        )

    def test_catalogue_update_duplicate_rate_is_not_treated_as_editorial_noise(self) -> None:
        url = "https://example.test/catalogue-updates.xml"
        previous = {
            url: {
                "url": url,
                "title": "Catalogue Updates",
                "passed": "yes",
                "duplicate_title_rate": 0.0,
                "duplicate_link_rate": 0.0,
                "item_link_policy": "catalogue-update",
            }
        }
        current = {
            url: {
                **previous[url],
                "duplicate_title_rate": 0.8,
                "duplicate_link_rate": 0.8,
            }
        }
        warnings = compare_feed_snapshots(previous, current)
        self.assertNotIn(
            "duplicate-title-threshold",
            {warning["kind"] for warning in warnings},
        )
        self.assertNotIn(
            "duplicate-link-threshold",
            {warning["kind"] for warning in warnings},
        )

    def test_scheduled_calendar_duplicate_rate_is_not_treated_as_editorial_noise(self) -> None:
        url = "https://example.test/scheduled-calendar.xml"
        previous = {
            url: {
                "url": url,
                "title": "Scheduled Calendar",
                "passed": "yes",
                "duplicate_title_rate": 0.0,
                "duplicate_link_rate": 0.0,
                "item_link_policy": "scheduled-calendar",
            }
        }
        current = {
            url: {
                **previous[url],
                "duplicate_title_rate": 0.8,
                "duplicate_link_rate": 0.8,
            }
        }
        warnings = compare_feed_snapshots(previous, current)
        self.assertNotIn(
            "duplicate-title-threshold",
            {warning["kind"] for warning in warnings},
        )
        self.assertNotIn(
            "duplicate-link-threshold",
            {warning["kind"] for warning in warnings},
        )

    def test_feed_drift_ignores_content_type_whitespace_only(self) -> None:
        url = "https://example.test/content-type.xml"
        previous = {
            url: {
                "url": url,
                "title": "Example Feed",
                "passed": "yes",
                "content_type": "application/rss+xml                              ",
            }
        }
        current = {
            url: {
                **previous[url],
                "content_type": "  application/rss+xml\t\n",
            }
        }
        self.assertEqual(
            normalize_content_type(previous[url]["content_type"]),
            "application/rss+xml",
        )
        warnings = compare_feed_snapshots(previous, current)
        self.assertNotIn("content-type-changed", {warning["kind"] for warning in warnings})


class ManifestConfigurationTest(unittest.TestCase):
    def test_device_profile_inheritance_and_budget_are_explicit(self) -> None:
        manifest = load_manifest(ROOT / "feed-manifest.json")
        self.assertEqual(profile_inheritance(manifest, "iphone-air"), ("iphone-lite",))
        self.assertEqual(profile_device_budget(profile_settings(manifest)["iphone-air"])["max_feeds"], 127)
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

    def test_manifest_future_date_override_requires_a_reason(self) -> None:
        manifest = load_manifest(ROOT / "feed-manifest.json")
        invalid = copy.deepcopy(manifest)
        feed = next(
            item
            for item in invalid["feeds"]
            if item["id"] == "finance-01-core-market-trading-nasdaq-trader-equity-trader-alerts"
        )
        feed.pop("future_date_reason")
        errors = manifest_errors(invalid)
        self.assertIn(
            "finance-01-core-market-trading-nasdaq-trader-equity-trader-alerts: feed-specific future-date tolerance needs future_date_reason",
            errors,
        )

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
    def test_atomic_artifact_writes_replace_symlinks_without_following_them(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            sentinel = directory / "sentinel.txt"
            destination = directory / "artifact.txt"
            sentinel.write_text("original\n", encoding="utf-8")
            destination.symlink_to(sentinel.name)

            atomic_write_text(destination, "replacement\n")

            self.assertFalse(destination.is_symlink())
            self.assertEqual(destination.read_text(encoding="utf-8"), "replacement\n")
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "original\n")

            binary_destination = directory / "artifact.bin"
            binary_sentinel = directory / "sentinel.bin"
            binary_sentinel.write_bytes(b"original")
            binary_destination.symlink_to(binary_sentinel.name)
            atomic_write_bytes(binary_destination, b"replacement")

            self.assertFalse(binary_destination.is_symlink())
            self.assertEqual(binary_destination.read_bytes(), b"replacement")
            self.assertEqual(binary_sentinel.read_bytes(), b"original")

    def test_bundle_generators_use_atomic_artifact_writers(self) -> None:
        source = (ROOT / "generate-bundle.py").read_text(encoding="utf-8")
        self.assertIn("atomic_write_bytes(destination", source)
        self.assertIn("atomic_write_text(destination", source)

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
            grouped: dict[tuple[str, str], list[dict]] = {}
            for feed in manifest["feeds"]:
                if profile_includes_feed(manifest, profile, feed):
                    grouped.setdefault((feed["section"], feed["folder"]), []).append(feed)
            expected_urls = [
                feed["url"]
                for feeds in grouped.values()
                for feed in feeds
            ]
            self.assertEqual(len(opml), len(expected_urls))
            self.assertEqual(len(table), len(expected_urls))
            self.assertEqual([entry["url"] for entry in opml], expected_urls)
            self.assertEqual([entry["url"] for entry in table], expected_urls)
            artifacts[profile] = (opml, table)

        self.assertEqual(len(artifacts["master"][0]), len(manifest["feeds"]))
        self.assertEqual(len(artifacts["iphone-lite"][0]), 120)
        self.assertEqual(len(artifacts["iphone-air"][0]), 125)
        air_budget = profile_device_budget(profiles["iphone-air"])
        self.assertEqual(air_budget["max_feeds"], 127)
        promoted_ids = {
            "finance-02-core-official-macro-federal-reserve-other-announcements",
            "finance-02-core-official-macro-federal-reserve-banking-applications",
            "finance-03-optional-data-ireland-eu-uk-ecb-statistical-releases",
            "finance-04-optional-global-data-research-reserve-bank-australia-bulletin",
            "finance-04-optional-global-data-research-reserve-bank-australia-research-discussion-papers",
            "finance-02-core-official-macro-danmarks-nationalbank-press-releases",
            "finance-04-optional-global-data-research-deutsche-bundesbank-speeches-interviews-contributions",
            "finance-04-optional-global-data-research-ecb-banking-supervision-publications",
            "finance-02-core-official-macro-danmarks-nationalbank-market-announcements",
            "finance-02-core-official-macro-banca-ditalia-news-english",
            "finance-02-core-official-macro-norges-bank-press-releases",
            "finance-01-core-market-trading-euronext-market-status",
            "finance-04-optional-global-data-research-cvm-legislation",
            "finance-04-optional-global-data-research-cvm-collegiate-bulletins",
            "finance-04-optional-global-data-research-singapore-food-agency-food-alerts-recalls",
        }
        for feed in manifest["feeds"]:
            if feed["id"] in promoted_ids:
                self.assertTrue(profile_includes_feed(manifest, "iphone-lite", feed))
                self.assertTrue(profile_includes_feed(manifest, "iphone-air", feed))
        euronext_athens = next(
            feed for feed in manifest["feeds"]
            if feed["id"] == "finance-01-core-market-trading-euronext-athens-market-notices"
        )
        self.assertFalse(profile_includes_feed(manifest, "iphone-lite", euronext_athens))
        self.assertFalse(profile_includes_feed(manifest, "iphone-air", euronext_athens))
        openssf = next(
            feed for feed in manifest["feeds"]
            if feed["id"] == "cyber-security-04-optional-specialist-alerts-research-openssf-supply-chain-security"
        )
        self.assertFalse(profile_includes_feed(manifest, "iphone-air", openssf))
        fbi_podcast = next(
            feed for feed in manifest["feeds"]
            if feed["id"] == "cyber-security-03-core-technical-research-fbi-ahead-of-the-threat-cyber-podcast"
        )
        self.assertFalse(profile_includes_feed(manifest, "iphone-lite", fbi_podcast))
        self.assertFalse(profile_includes_feed(manifest, "iphone-air", fbi_podcast))
        bbc_business = next(
            feed for feed in manifest["feeds"]
            if feed["id"] == "finance-01-core-market-trading-bbc-business"
        )
        self.assertFalse(profile_includes_feed(manifest, "iphone-lite", bbc_business))
        self.assertFalse(profile_includes_feed(manifest, "iphone-air", bbc_business))
        cyberscoop = next(
            feed for feed in manifest["feeds"]
            if feed["id"] == "cyber-security-02-core-news-incident-reporting-cyberscoop"
        )
        self.assertFalse(profile_includes_feed(manifest, "iphone-lite", cyberscoop))
        self.assertFalse(profile_includes_feed(manifest, "iphone-air", cyberscoop))
        un_news = next(
            feed for feed in manifest["feeds"]
            if feed["id"] == "finance-04-optional-global-data-research-un-news-economic-development"
        )
        self.assertTrue(profile_includes_feed(manifest, "iphone-lite", un_news))
        self.assertTrue(profile_includes_feed(manifest, "iphone-air", un_news))
        un_human_rights = next(
            feed for feed in manifest["feeds"]
            if feed["id"] == "finance-04-optional-global-data-research-un-news-human-rights"
        )
        self.assertTrue(profile_includes_feed(manifest, "iphone-lite", un_human_rights))
        self.assertTrue(profile_includes_feed(manifest, "iphone-air", un_human_rights))
        un_peace_security = next(
            feed for feed in manifest["feeds"]
            if feed["id"] == "finance-04-optional-global-data-research-un-news-peace-and-security"
        )
        self.assertTrue(profile_includes_feed(manifest, "iphone-lite", un_peace_security))
        self.assertTrue(profile_includes_feed(manifest, "iphone-air", un_peace_security))
        un_health = next(
            feed for feed in manifest["feeds"]
            if feed["id"] == "finance-04-optional-global-data-research-un-news-health"
        )
        self.assertTrue(profile_includes_feed(manifest, "iphone-lite", un_health))
        self.assertTrue(profile_includes_feed(manifest, "iphone-air", un_health))
        council = next(
            feed for feed in manifest["feeds"]
            if feed["id"] == "finance-04-optional-global-data-research-council-of-the-eu-press-releases"
        )
        self.assertTrue(profile_includes_feed(manifest, "iphone-lite", council))
        self.assertTrue(profile_includes_feed(manifest, "iphone-air", council))
        european_parliament = next(
            feed for feed in manifest["feeds"]
            if feed["id"] == "finance-04-optional-global-data-research-european-parliament-committee-press-releases"
        )
        self.assertTrue(profile_includes_feed(manifest, "iphone-lite", european_parliament))
        self.assertTrue(profile_includes_feed(manifest, "iphone-air", european_parliament))
        curia = next(
            feed for feed in manifest["feeds"]
            if feed["id"] == "finance-04-optional-global-data-research-court-of-justice-of-the-european-union-press-releases"
        )
        self.assertTrue(profile_includes_feed(manifest, "iphone-lite", curia))
        self.assertTrue(profile_includes_feed(manifest, "iphone-air", curia))
        ema = next(
            feed for feed in manifest["feeds"]
            if feed["id"] == "finance-04-optional-global-data-research-european-medicines-agency-news-and-press-releases"
        )
        self.assertTrue(profile_includes_feed(manifest, "iphone-lite", ema))
        self.assertTrue(profile_includes_feed(manifest, "iphone-air", ema))
        financial_times = next(
            feed for feed in manifest["feeds"]
            if feed["id"] == "finance-01-core-market-trading-financial-times-markets"
        )
        self.assertFalse(profile_includes_feed(manifest, "iphone-lite", financial_times))
        self.assertFalse(profile_includes_feed(manifest, "iphone-air", financial_times))
        bis_statistics = next(
            feed for feed in manifest["feeds"]
            if feed["id"] == "finance-04-optional-global-data-research-bis-statistical-releases"
        )
        self.assertFalse(profile_includes_feed(manifest, "iphone-air", bis_statistics))
        trade_halts = next(
            entry for entry in artifacts["master"][0] if entry["title"] == "Nasdaq Trader — Trade Halts"
        )
        self.assertEqual(trade_halts["item_link_policy"], "structured-alert")
        eurostat_catalogue = next(
            entry for entry in artifacts["master"][0]
            if entry["title"] == "Eurostat — Data and Data Structure Updates"
        )
        self.assertEqual(eurostat_catalogue["item_link_policy"], "catalogue-update")
        european_council = next(
            entry for entry in artifacts["master"][0]
            if entry["title"] == "European Council — Meetings"
        )
        self.assertEqual(european_council["item_link_policy"], "scheduled-calendar")

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
            self.assertEqual(matrix["profiles"]["iphone-air"]["device_budget"]["max_feeds"], 127)
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
        handoff_file = ROOT / "artifacts" / "AirDrop" / air_file.name
        self.assertEqual(air_file.read_bytes(), handoff_file.read_bytes())
        handoff_readme = ROOT / "artifacts" / "AirDrop" / "README.txt"
        self.assertIn("125 feeds", handoff_readme.read_text(encoding="utf-8"))
        self.assertNotIn("50 feeds", handoff_readme.read_text(encoding="utf-8"))

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
        master_config = profile_settings(manifest)["master"]
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
                    str(ROOT / master_config["opml_file"]),
                    str(ROOT / master_config["source_table_file"]),
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
                env={**os.environ, "REPORT_LINK_DIRECTORY": str(ROOT / "artifacts" / "validation")},
            )
            self.assertNotEqual(result.returncode, 0)
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["bundle"], master_config["opml_file"])
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

    def test_digest_profile_routes_hmrc_and_apra_for_apple_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            input_path = directory / "articles.json"
            air_output_path = directory / "air-digest.json"
            air_state_path = directory / "air-state.json"
            air_shortcut_path = directory / "air-shortcut.txt"
            master_output_path = directory / "master-digest.json"
            master_state_path = directory / "master-state.json"
            input_path.write_text(
                json.dumps(
                    [
                        {
                            "title": "HMRC tax-customs test item",
                            "link": "https://www.gov.uk/government/news/example-hmrc",
                            "feed": "HM Revenue & Customs — Activity on GOV.UK",
                            "feed_url": "https://www.gov.uk/government/organisations/hm-revenue-customs.atom",
                            "published": "2026-08-17T23:15:02Z",
                            "summary": "A synthetic HMRC handoff item.",
                        },
                        {
                            "title": "APRA prudential test item",
                            "link": "https://www.apra.gov.au/news/example-apra",
                            "feed": "APRA — News",
                            "feed_url": "https://www.apra.gov.au/rss.xml",
                            "published": "2026-07-31T00:00:00Z",
                            "summary": "A synthetic APRA handoff item.",
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
                    str(air_output_path),
                    "--state",
                    str(air_state_path),
                    "--shortcut-output",
                    str(air_shortcut_path),
                    "--profile",
                    "iphone-air",
                    "--dry-run",
                ],
                check=True,
                cwd=ROOT,
            )
            air_package = json.loads(air_output_path.read_text(encoding="utf-8"))
            air_shortcut = air_shortcut_path.read_text(encoding="utf-8")
            self.assertEqual(air_package["profile"], "iphone-air")
            self.assertEqual(air_package["article_count"], 1)
            self.assertEqual(air_package["skipped_profile_count"], 1)
            self.assertEqual(air_package["manifest_enriched_count"], 1)
            self.assertEqual(air_package["unmatched_source_count"], 0)
            self.assertEqual(
                air_package["articles"][0]["manifest_id"],
                "finance-02-core-official-macro-hm-revenue-customs-activity-gov-uk",
            )
            self.assertIn("HMRC tax-customs test item", air_shortcut)
            self.assertIn("Link: https://www.gov.uk/government/news/example-hmrc", air_shortcut)
            self.assertNotIn("APRA prudential test item", air_shortcut)

            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "prepare-rss-digest-input.py"),
                    "--input",
                    str(input_path),
                    "--output",
                    str(master_output_path),
                    "--state",
                    str(master_state_path),
                    "--profile",
                    "master",
                    "--dry-run",
                ],
                check=True,
                cwd=ROOT,
            )
            master_package = json.loads(master_output_path.read_text(encoding="utf-8"))
            self.assertEqual(master_package["profile"], "master")
            self.assertEqual(master_package["article_count"], 2)
            self.assertEqual(master_package["skipped_profile_count"], 0)
            self.assertEqual(master_package["manifest_enriched_count"], 2)
            self.assertEqual(master_package["unmatched_source_count"], 0)
            self.assertEqual(
                {article["manifest_id"] for article in master_package["articles"]},
                {
                    "finance-02-core-official-macro-hm-revenue-customs-activity-gov-uk",
                    "finance-02-core-official-macro-apra-news",
                },
            )

    def test_digest_profile_routes_financial_crime_and_project_zero_sources(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            input_path = directory / "articles.json"
            air_output_path = directory / "air-digest.json"
            air_state_path = directory / "air-state.json"
            air_shortcut_path = directory / "air-shortcut.txt"
            master_output_path = directory / "master-digest.json"
            master_state_path = directory / "master-state.json"
            input_path.write_text(
                json.dumps(
                    [
                        {
                            "title": "SFO financial-crime test item",
                            "link": "https://www.gov.uk/government/news/example-sfo",
                            "feed": "Serious Fraud Office — Activity on GOV.UK",
                            "feed_url": "https://www.gov.uk/government/organisations/serious-fraud-office.atom",
                            "published": "2026-08-10T12:03:55Z",
                            "summary": "A synthetic SFO handoff item.",
                        },
                        {
                            "title": "Insolvency director-enforcement test item",
                            "link": "https://www.gov.uk/government/news/example-insolvency",
                            "feed": "Insolvency Service — Activity on GOV.UK",
                            "feed_url": "https://www.gov.uk/government/organisations/insolvency-service.atom",
                            "published": "2026-08-14T13:50:00Z",
                            "summary": "A synthetic Insolvency Service handoff item.",
                        },
                        {
                            "title": "EDPB AI-governance test item",
                            "link": "https://www.edpb.europa.eu/news/example-ai-governance_en",
                            "feed": "European Data Protection Board — News",
                            "feed_url": "https://www.edpb.europa.eu/rss.xml_en",
                            "published": "2026-07-08T11:34:38Z",
                            "summary": "A synthetic EDPB handoff item.",
                        },
                        {
                            "title": "European Commission competition-policy test item",
                            "link": "https://competition-policy.ec.europa.eu/news/example-competition_en",
                            "feed": "European Commission — Competition Policy News",
                            "feed_url": "https://competition-policy.ec.europa.eu/node/38/rss_en",
                            "published": "2026-08-07T09:48:22Z",
                            "summary": "A synthetic Commission competition handoff item.",
                        },
                        {
                            "title": "European Commission tax-customs test item",
                            "link": "https://taxation-customs.ec.europa.eu/news/example-tax-customs_en",
                            "feed": "European Commission — Taxation & Customs News",
                            "feed_url": "https://taxation-customs.ec.europa.eu/node/2/rss_en",
                            "published": "2026-08-14T08:12:13Z",
                            "summary": "A synthetic Commission tax and customs handoff item.",
                        },
                        {
                            "title": "European Commission financial-services test item",
                            "link": "https://finance.ec.europa.eu/news/example-financial-services_en",
                            "feed": "European Commission — Financial Services News (FISMA)",
                            "feed_url": "https://finance.ec.europa.eu/node/1408/rss_en",
                            "published": "2026-08-03T10:27:07Z",
                            "summary": "A synthetic Commission financial-services handoff item.",
                        },
                        {
                            "title": "EPPO financial-crime test item",
                            "link": "https://www.eppo.europa.eu/media/news/example-financial-crime-2026-08-13_en",
                            "feed": "European Public Prosecutor’s Office — News",
                            "feed_url": "https://www.eppo.europa.eu/node/2/rss_en",
                            "published": "2026-08-13T07:48:28Z",
                            "summary": "A synthetic EPPO handoff item.",
                        },
                        {
                            "title": "OLAF anti-fraud test item",
                            "link": "https://anti-fraud.ec.europa.eu/media-corner/news/example-anti-fraud-2026-08-07_en",
                            "feed": "European Anti-Fraud Office (OLAF) — News",
                            "feed_url": "https://anti-fraud.ec.europa.eu/node/2/rss_en",
                            "published": "2026-08-07T13:24:30Z",
                            "summary": "A synthetic OLAF handoff item.",
                        },
                        {
                            "title": "Eurojust organised-crime test item",
                            "link": "https://www.eurojust.europa.eu/news/example-organised-crime",
                            "feed": "Eurojust — Press Releases & News",
                            "feed_url": "https://www.eurojust.europa.eu/rss/press-releases.xml",
                            "published": "2026-08-11T12:00:00Z",
                            "summary": "A synthetic Eurojust handoff item.",
                        },
                        {
                            "title": "Project Zero vulnerability-research test item",
                            "link": "https://projectzero.google/example-research",
                            "feed": "Google Project Zero — Research",
                            "feed_url": "https://projectzero.google/feed.xml",
                            "published": "2026-05-13T07:00:00Z",
                            "summary": "A synthetic Project Zero handoff item.",
                        },
                        {
                            "title": "FBI cyber-resilience podcast test item",
                            "link": "https://www.fbi.gov/audio-repository/ahead-of-the-threat-podcast-example.mp3/view",
                            "feed": "FBI — Ahead of the Threat Cyber Podcast",
                            "feed_url": "https://www.fbi.gov/feeds/ahead-of-the-threat-itunes/rss.xml",
                            "published": "2026-07-23T11:31:00Z",
                            "summary": "A synthetic FBI Cyber Division handoff item.",
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
                    str(air_output_path),
                    "--state",
                    str(air_state_path),
                    "--shortcut-output",
                    str(air_shortcut_path),
                    "--profile",
                    "iphone-air",
                    "--dry-run",
                ],
                check=True,
                cwd=ROOT,
            )
            air_package = json.loads(air_output_path.read_text(encoding="utf-8"))
            air_shortcut = air_shortcut_path.read_text(encoding="utf-8")
            self.assertEqual(air_package["article_count"], 7)
            self.assertEqual(air_package["skipped_profile_count"], 4)
            self.assertEqual(air_package["manifest_enriched_count"], 7)
            self.assertEqual(air_package["unmatched_source_count"], 0)
            self.assertEqual(
                {article["manifest_id"] for article in air_package["articles"]},
                {
                    "finance-02-core-official-macro-serious-fraud-office-activity-gov-uk",
                    "finance-02-core-official-macro-insolvency-service-activity-gov-uk",
                    "cyber-security-01-core-ireland-eu-official-alerts-european-data-protection-board-news",
                    "finance-02-core-official-macro-european-commission-competition-policy-news",
                    "finance-02-core-official-macro-european-commission-taxation-customs-news",
                    "finance-02-core-official-macro-european-commission-financial-services-news-fisma",
                    "finance-02-core-official-macro-european-public-prosecutors-office-news",
                },
            )
            self.assertIn("SFO financial-crime test item", air_shortcut)
            self.assertIn("Insolvency director-enforcement test item", air_shortcut)
            self.assertIn("EDPB AI-governance test item", air_shortcut)
            self.assertIn("European Commission competition-policy test item", air_shortcut)
            self.assertIn("European Commission tax-customs test item", air_shortcut)
            self.assertIn("European Commission financial-services test item", air_shortcut)
            self.assertIn("EPPO financial-crime test item", air_shortcut)
            self.assertNotIn("FBI cyber-resilience podcast test item", air_shortcut)
            self.assertNotIn("OLAF anti-fraud test item", air_shortcut)
            self.assertNotIn("Eurojust organised-crime test item", air_shortcut)
            self.assertNotIn("Project Zero vulnerability-research test item", air_shortcut)

            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "prepare-rss-digest-input.py"),
                    "--input",
                    str(input_path),
                    "--output",
                    str(master_output_path),
                    "--state",
                    str(master_state_path),
                    "--profile",
                    "master",
                    "--dry-run",
                ],
                check=True,
                cwd=ROOT,
            )
            master_package = json.loads(master_output_path.read_text(encoding="utf-8"))
            self.assertEqual(master_package["article_count"], 11)
            self.assertEqual(master_package["skipped_profile_count"], 0)
            self.assertEqual(master_package["manifest_enriched_count"], 11)
            self.assertEqual(master_package["unmatched_source_count"], 0)
            self.assertEqual(
                {article["manifest_id"] for article in master_package["articles"]},
                {
                    "finance-02-core-official-macro-serious-fraud-office-activity-gov-uk",
                    "finance-02-core-official-macro-insolvency-service-activity-gov-uk",
                    "cyber-security-01-core-ireland-eu-official-alerts-european-data-protection-board-news",
                    "finance-02-core-official-macro-european-commission-competition-policy-news",
                    "finance-02-core-official-macro-european-commission-taxation-customs-news",
                    "finance-02-core-official-macro-european-commission-financial-services-news-fisma",
                    "finance-02-core-official-macro-european-public-prosecutors-office-news",
                    "finance-02-core-official-macro-european-anti-fraud-office-olaf-news",
                    "finance-02-core-official-macro-eurojust-press-releases-news",
                    "cyber-security-03-core-technical-research-google-project-zero-research",
                    "cyber-security-03-core-technical-research-fbi-ahead-of-the-threat-cyber-podcast",
                },
            )

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

    def test_digest_rejects_future_state_version_without_resetting_it(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            input_path = directory / "articles.json"
            state_path = directory / "state.json"
            input_path.write_text("[]\n", encoding="utf-8")
            original = '{"version": 99, "last_run": "", "seen": {}}\n'
            state_path.write_text(original, encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "prepare-rss-digest-input.py"),
                    "--input",
                    str(input_path),
                    "--state",
                    str(state_path),
                    "--output",
                    str(directory / "digest.json"),
                    "--dry-run",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("version must be 1 or 2", result.stderr)
            self.assertEqual(state_path.read_text(encoding="utf-8"), original)


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

    def test_history_rejects_future_schema_version_without_resetting_it(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            report_path = directory / "report.json"
            history_path = directory / "history.json"
            report_path.write_text(
                json.dumps({"summary": {"failed_feed_count": 0}}),
                encoding="utf-8",
            )
            original = '{"version": 99, "profiles": {}}\n'
            history_path.write_text(original, encoding="utf-8")
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
                    "--healthy",
                    "yes",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("version must be 1 or 2", result.stdout)
            self.assertEqual(history_path.read_text(encoding="utf-8"), original)

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


class WorkflowContractTest(unittest.TestCase):
    def test_workflow_lint_job_is_hash_pinned_and_read_only(self) -> None:
        workflow = (ROOT / ".github/workflows/rss-validation.yml").read_text(encoding="utf-8")
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        self.assertIn("workflow-lint:", workflow)
        self.assertIn("persist-credentials: false", workflow)
        self.assertIn("ACTIONLINT_VERSION: 1.7.12", workflow)
        self.assertIn(
            "ACTIONLINT_SHA256: 8aca8db96f1b94770f1b0d72b6dddcb1ebb8123cb3712530b08cc387b349a3d8",
            workflow,
        )
        self.assertIn("sha256sum --check --status", workflow)
        self.assertIn('"${RUNNER_TEMP}/actionlint"', workflow)
        self.assertEqual(
            workflow.count("git diff --check"),
            workflow.count("uses: actions/checkout@"),
        )
        self.assertIn("patch-hygiene:", makefile)
        self.assertIn("check: patch-hygiene", makefile)
        self.assertIn("check: patch-hygiene generate", makefile)
        self.assertNotIn("check: patch-hygiene package", makefile)
        self.assertIn("AirDrop/NetNewsWire-Finance-Cyber-iPhone-Air.opml", workflow)


class RepositoryHygieneTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        module_path = ROOT / "check-repository-hygiene.py"
        spec = importlib.util.spec_from_file_location("repository_hygiene", module_path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot load hygiene checker: {module_path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        cls.hygiene = module

    def test_hygiene_gate_passes_the_repository(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "check-repository-hygiene.py"), "--root", str(ROOT)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        self.assertIn("hygiene-check passed", result.stdout)

    def test_hygiene_patterns_detect_secret_and_machine_path(self) -> None:
        fake_token = b"gh" + b"p_" + b"A" * 24
        findings = self.hygiene.content_findings(
            b"token=" + fake_token + b"\npath=/Users/" + b"alice/project\n"
        )
        labels = {label for label, _line in findings}
        self.assertIn("GitHub token", labels)
        self.assertIn("macOS absolute user path", labels)
        self.assertIn("tracked runtime state", self.hygiene.path_findings(Path(".digest-state.json")))


if __name__ == "__main__":
    unittest.main()
