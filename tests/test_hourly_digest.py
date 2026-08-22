from __future__ import annotations

import importlib.util
import urllib.error
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]


def load_collector():
    path = ROOT / "fetch-rss-digest-input.py"
    spec = importlib.util.spec_from_file_location("fetch_rss_digest_input", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeResponse:
    def __init__(self, body: bytes, *, status: int = 200, headers: dict[str, str] | None = None) -> None:
        self.body = body
        self.status = status
        self.headers = headers or {"Content-Type": "application/rss+xml"}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        return None

    def getcode(self) -> int:
        return self.status

    def geturl(self) -> str:
        return "https://example.test/feed.xml"

    def read(self, limit: int = -1) -> bytes:
        return self.body if limit < 0 else self.body[:limit]


class HourlyCollectorTest(unittest.TestCase):
    def test_parse_feed_preserves_dated_summary_and_manifest_source(self) -> None:
        collector = load_collector()
        body = b"""<?xml version='1.0'?>
        <rss version='2.0'><channel><title>Fixture Feed</title>
          <item><title>Important update</title>
            <link>https://example.test/story</link>
            <pubDate>Tue, 18 Aug 2026 09:00:00 GMT</pubDate>
            <description><![CDATA[<p>Short evidence summary.</p>]]></description>
          </item>
        </channel></rss>"""
        feed = {
            "title": "Manifest Feed",
            "url": "https://example.test/feed.xml",
            "signal_type": "official/alert",
        }

        articles, skipped, title = collector.parse_feed_bytes(body, feed, max_items=20)

        self.assertEqual(title, "Fixture Feed")
        self.assertEqual(skipped, 0)
        self.assertEqual(articles[0]["feed"], "Manifest Feed")
        self.assertEqual(articles[0]["published"], "2026-08-18T09:00:00+00:00")
        self.assertIn("Short evidence summary", articles[0]["summary"])

    def test_fetch_uses_conditional_request_and_handles_not_modified(self) -> None:
        collector = load_collector()
        feed = {"title": "Fixture", "url": "https://example.test/feed.xml"}
        prior = {"etag": '"abc"', "last_modified": "Tue, 18 Aug 2026 08:00:00 GMT"}
        error = urllib.error.HTTPError(
            feed["url"],
            304,
            "Not Modified",
            {},
            None,
        )

        with mock.patch.object(collector.urllib.request, "urlopen", side_effect=error) as urlopen:
            result = collector.fetch_feed(
                feed,
                prior,
                timeout=2,
                max_response_bytes=1024,
                max_items=10,
                user_agent="test-agent",
            )

        request = urlopen.call_args.args[0]
        request_headers = dict(request.header_items())
        self.assertEqual(request_headers["If-none-match"], '"abc"')
        self.assertEqual(request_headers["If-modified-since"], "Tue, 18 Aug 2026 08:00:00 GMT")
        self.assertTrue(result["not_modified"])
        self.assertEqual(result["status"], 304)
        self.assertEqual(result["state"]["last_status"], 304)

    def test_fetch_uses_endpoint_identity_for_european_parliament_rss(self) -> None:
        collector = load_collector()
        feed = {
            "title": "European Parliament",
            "url": "https://www.europarl.europa.eu/rss/doc/press-releases-committees/en.xml",
        }
        response = FakeResponse(b"<rss><channel><title>Parliament</title></channel></rss>")

        with mock.patch.object(collector.urllib.request, "urlopen", return_value=response) as urlopen:
            result = collector.fetch_feed(
                feed,
                {},
                timeout=2,
                max_response_bytes=1024,
                max_items=10,
                user_agent="test-agent",
            )

        request = urlopen.call_args.args[0]
        self.assertEqual(dict(request.header_items())["User-agent"], "curl/8.0")
        self.assertEqual(result["status"], 200)

    def test_fetch_uses_endpoint_identity_for_dnb_rss(self) -> None:
        collector = load_collector()
        feed = {
            "title": "DNB — Supervision News",
            "url": "https://www.dnb.nl/en/rss/16453/6892",
        }
        response = FakeResponse(b"<rss><channel><title>DNB</title></channel></rss>")

        with mock.patch.object(collector.urllib.request, "urlopen", return_value=response) as urlopen:
            result = collector.fetch_feed(
                feed,
                {},
                timeout=2,
                max_response_bytes=1024,
                max_items=10,
                user_agent="test-agent",
            )

        request = urlopen.call_args.args[0]
        self.assertEqual(dict(request.header_items())["User-agent"], "curl/8.0")
        self.assertEqual(result["status"], 200)

    def test_fetch_uses_endpoint_identity_for_cfpb_rss(self) -> None:
        collector = load_collector()
        feed = {
            "title": "CFPB — Newsroom",
            "url": "https://www.consumerfinance.gov/about-us/newsroom/feed/",
        }
        response = FakeResponse(b"<rss><channel><title>CFPB</title></channel></rss>")

        with mock.patch.object(collector.urllib.request, "urlopen", return_value=response) as urlopen:
            result = collector.fetch_feed(
                feed,
                {},
                timeout=2,
                max_response_bytes=1024,
                max_items=10,
                user_agent="test-agent",
            )

        request = urlopen.call_args.args[0]
        self.assertEqual(dict(request.header_items())["User-agent"], "curl/8.0")
        self.assertEqual(result["status"], 200)

    def test_fetch_uses_endpoint_identity_for_st_louis_fed_rss(self) -> None:
        collector = load_collector()
        feed = {
            "title": "Federal Reserve Bank of St. Louis — On the Economy",
            "url": "https://www.stlouisfed.org/rss/page%20resources/publications/blog-entries",
        }
        response = FakeResponse(b"<rss><channel><title>St. Louis Fed</title></channel></rss>")

        with mock.patch.object(collector.urllib.request, "urlopen", return_value=response) as urlopen:
            result = collector.fetch_feed(
                feed,
                {},
                timeout=2,
                max_response_bytes=1024,
                max_items=10,
                user_agent="test-agent",
            )

        request = urlopen.call_args.args[0]
        self.assertEqual(dict(request.header_items())["User-agent"], "curl/8.0")
        self.assertEqual(result["status"], 200)

    def test_parse_feed_resolves_relative_item_link(self) -> None:
        collector = load_collector()
        body = b"""<rss version='2.0'><channel><title>Fixture Feed</title>
          <item><title>Archived update</title>
            <link>/news/archived-update</link>
            <pubDate>Tue, 18 Aug 2026 09:00:00 GMT</pubDate>
          </item>
        </channel></rss>"""
        feed = {"title": "Manifest Feed", "url": "https://example.test/rss/feed.xml"}

        articles, skipped, _ = collector.parse_feed_bytes(body, feed, max_items=20)

        self.assertEqual(skipped, 0)
        self.assertEqual(articles[0]["link"], "https://example.test/news/archived-update")

    def test_parse_feed_accepts_atom_with_empty_channel_title(self) -> None:
        collector = load_collector()
        body = b"""<feed xmlns='http://www.w3.org/2005/Atom'>
          <title></title>
          <entry><title>Policy update</title>
            <link rel='alternate' href='/news/policy-update'/>
            <published>2026-08-18T09:00:00Z</published>
          </entry>
        </feed>"""
        feed = {
            "title": "Manifest Central Bank Feed",
            "url": "https://example.test/rss/feed.xml",
        }

        articles, skipped, title = collector.parse_feed_bytes(body, feed, max_items=20)

        self.assertEqual(title, "Manifest Central Bank Feed")
        self.assertEqual(skipped, 0)
        self.assertEqual(articles[0]["title"], "Policy update")
        self.assertEqual(articles[0]["link"], "https://example.test/news/policy-update")

    def test_parse_failures_are_not_counted_as_successful_feeds(self) -> None:
        collector = load_collector()
        feed = {"title": "Invalid fixture", "url": "https://example.test/feed.xml"}
        response = FakeResponse(b"<html><title>not a feed</title></html>")

        with mock.patch.object(collector.urllib.request, "urlopen", return_value=response):
            _, report = collector.collect_feeds(
                [feed],
                {"version": 1, "feeds": {}},
                timeout=2,
                max_response_bytes=1024,
                max_items=10,
                workers=1,
                user_agent="test-agent",
            )

        self.assertEqual(report["summary"]["feeds_considered"], 1)
        self.assertEqual(report["summary"]["feeds_succeeded"], 0)
        self.assertEqual(report["summary"]["feeds_failed"], 1)
