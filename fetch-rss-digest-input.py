#!/usr/bin/env python3
"""Fetch manifest RSS/Atom feeds into a bounded Apple Intelligence input export.

This collector deliberately reads the same HTTPS endpoints that are imported
into NetNewsWire. It is an unattended manifest mirror, not an export of
NetNewsWire's private unread database. Use the NetNewsWire Share Sheet path
when the digest must contain only items selected in the reader.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import gzip
import json
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin
from zoneinfo import ZoneInfo

from bundle_config import load_manifest, profile_includes_feed, profile_settings
from rss_validation import (
    child_link,
    child_text,
    item_date_raw,
    local_name,
    parse_date,
    url_is_web,
)
from state_utils import atomic_write_text, file_lock, lock_path


DEFAULT_USER_AGENT = "NetNewsWire-Finance-Cyber/2.0 local-rss-digest"
MAX_SAFE_XML_BYTES = 32 * 1024 * 1024

# The public European Parliament RSS endpoint returns an AWS WAF challenge to
# the collector's descriptive user-agent.  The same endpoint is valid RSS
# when requested with the neutral curl identity used by the live validator.
ENDPOINT_USER_AGENTS = {
    "https://www.europarl.europa.eu/rss/doc/press-releases-committees/en.xml": "curl/8.0",
    "https://www.dnb.nl/en/rss/16451/6882": "curl/8.0",
    "https://www.dnb.nl/en/rss/16453/6892": "curl/8.0",
    "https://www.dnb.nl/en/rss/16452/6893": "curl/8.0",
    "https://www.dnb.nl/en/rss/13039/4612": "curl/8.0",
    "https://www.dnb.nl/en/rss/16455/4614": "curl/8.0",
    "https://www.consumerfinance.gov/about-us/newsroom/feed/": "curl/8.0",
    "https://www.stlouisfed.org/rss/page%20resources/publications/blog-entries": "curl/8.0",
    "https://www.stlouisfed.org/rss/page-resources/publications/review": "curl/8.0",
}


def now_dublin() -> str:
    return datetime.now(ZoneInfo("Europe/Dublin")).isoformat(timespec="seconds")


def load_state(path: Path) -> dict:
    if not path.exists():
        return {"version": 1, "feeds": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("RSS fetch state must be a JSON object")
    feeds = data.get("feeds", {})
    if not isinstance(feeds, dict):
        raise ValueError("RSS fetch state feeds field must be an object")
    data["version"] = 1
    data["feeds"] = feeds
    return data


def _feed_items(root: ET.Element) -> tuple[str, list[ET.Element]]:
    root_name = local_name(root.tag).lower()
    if root_name == "rss":
        container = next(
            (child for child in list(root) if local_name(child.tag).lower() == "channel"),
            None,
        )
        if container is None:
            return "", []
        return child_text(container, {"title"}), [
            child for child in list(container) if local_name(child.tag).lower() == "item"
        ]
    if root_name == "rdf":
        channel = next(
            (child for child in list(root) if local_name(child.tag).lower() == "channel"),
            None,
        )
        feed_title = child_text(channel, {"title"}) if channel is not None else child_text(root, {"title"})
        return feed_title, [
            child for child in list(root) if local_name(child.tag).lower() == "item"
        ]
    if root_name == "feed":
        return child_text(root, {"title"}), [
            child for child in list(root) if local_name(child.tag).lower() == "entry"
        ]
    return "", []


def parse_feed_bytes(
    body: bytes,
    feed: dict,
    *,
    max_items: int,
) -> tuple[list[dict], int, str]:
    """Parse a safe RSS/Atom/RDF body into the article contract."""

    if len(body) > MAX_SAFE_XML_BYTES:
        raise ValueError("XML body exceeds the safe parser limit")
    declaration_scan = re.sub(rb"<!\[CDATA\[.*?\]\]>", b"", body, flags=re.DOTALL)
    lowered = declaration_scan.lower()
    if b"<!doctype" in lowered or b"<!entity" in lowered:
        raise ValueError("DTD/entity declarations are not allowed")
    root = ET.fromstring(body)
    root_name = local_name(root.tag).lower()
    if root_name not in {"rss", "rdf", "feed"}:
        raise ValueError("XML root is not a recognized RSS, Atom or RDF feed")
    feed_title, elements = _feed_items(root)
    # Some valid Atom endpoints, including several central-bank feeds, leave
    # the top-level <title> empty while still providing dated entries. Keep
    # the manifest title as the stable source label instead of rejecting the
    # feed solely because its channel title is blank.
    feed_title = feed_title.strip() or str(feed.get("title", "")).strip()

    articles: list[dict] = []
    skipped = 0
    for element in elements[:max_items]:
        title = " ".join(child_text(element, {"title"}).split())
        link = child_link(element).strip()
        if link and not url_is_web(link):
            resolved_link = urljoin(str(feed.get("url", "")), link)
            if url_is_web(resolved_link):
                link = resolved_link
        raw_date = item_date_raw(element).strip()
        parsed_date = parse_date(raw_date) if raw_date else None
        if not title or not url_is_web(link) or parsed_date is None:
            skipped += 1
            continue
        summary = child_text(element, {"description", "summary", "content", "encoded"})
        articles.append(
            {
                "title": title,
                "link": link,
                "feed": str(feed.get("title", "")),
                "feed_url": str(feed.get("url", "")),
                "published": parsed_date.isoformat(),
                "summary": summary[:24000],
                "source_class": str(feed.get("signal_type", "")),
                "language": "",
            }
        )
    return articles, skipped, feed_title


def _state_after(
    previous: dict,
    *,
    checked_at: str,
    status: int | str,
    effective_url: str,
    error: str = "",
    etag: str = "",
    last_modified: str = "",
) -> dict:
    state = dict(previous)
    state.update(
        {
            "checked_at": checked_at,
            "last_status": status,
            "effective_url": effective_url,
            "last_error": error,
        }
    )
    if etag:
        state["etag"] = etag
    if last_modified:
        state["last_modified"] = last_modified
    if not error:
        state["last_success"] = checked_at
    return state


def _result_base(feed: dict) -> dict:
    return {
        "title": str(feed.get("title", "")),
        "url": str(feed.get("url", "")),
        "status": "",
        "effective_url": str(feed.get("url", "")),
        "content_type": "",
        "not_modified": False,
        "article_count": 0,
        "skipped_item_count": 0,
        "feed_title": "",
        "elapsed_seconds": 0.0,
        "error": "",
        "articles": [],
        "state": {},
    }


def fetch_feed(
    feed: dict,
    previous_state: dict,
    *,
    timeout: float,
    max_response_bytes: int,
    max_items: int,
    user_agent: str,
) -> dict:
    """Fetch one feed and return articles plus the next cache state."""

    result = _result_base(feed)
    started = time.perf_counter()
    checked_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    headers = {
        "Accept": "application/rss+xml, application/atom+xml, application/rdf+xml, application/xml, text/xml;q=0.9, */*;q=0.1",
        "Accept-Encoding": "gzip",
        "User-Agent": ENDPOINT_USER_AGENTS.get(str(feed["url"]), user_agent),
    }
    if previous_state.get("etag"):
        headers["If-None-Match"] = str(previous_state["etag"])
    if previous_state.get("last_modified"):
        headers["If-Modified-Since"] = str(previous_state["last_modified"])
    request = urllib.request.Request(str(feed["url"]), headers=headers)

    try:
        try:
            response_context = urllib.request.urlopen(request, timeout=timeout)
        except urllib.error.HTTPError as exc:
            if exc.code == 304:
                result.update(
                    {
                        "status": 304,
                        "not_modified": True,
                        "elapsed_seconds": round(time.perf_counter() - started, 3),
                        "state": _state_after(
                            previous_state,
                            checked_at=checked_at,
                            status=304,
                            effective_url=str(feed["url"]),
                        ),
                    }
                )
                return result
            raise

        with response_context as response:
            status = int(getattr(response, "status", response.getcode()))
            effective_url = str(response.geturl() or feed["url"])
            content_type = str(response.headers.get("Content-Type", ""))
            result.update(
                {
                    "status": status,
                    "effective_url": effective_url,
                    "content_type": content_type,
                }
            )
            if status != 200:
                raise ValueError(f"HTTP status {status}")
            if not url_is_web(effective_url, schemes=("https",)):
                raise ValueError(f"redirected to non-HTTPS URL: {effective_url}")
            body = response.read(max_response_bytes + 1)
            if len(body) > max_response_bytes:
                raise ValueError(f"response exceeds {max_response_bytes} bytes")
            if "gzip" in content_type.lower() or str(response.headers.get("Content-Encoding", "")).lower() == "gzip":
                body = gzip.decompress(body)
            articles, skipped, feed_title = parse_feed_bytes(body, feed, max_items=max_items)
            etag = str(response.headers.get("ETag", "")).strip()
            last_modified = str(response.headers.get("Last-Modified", "")).strip()
            result.update(
                {
                    "feed_title": feed_title,
                    "article_count": len(articles),
                    "skipped_item_count": skipped,
                    "articles": articles,
                    "elapsed_seconds": round(time.perf_counter() - started, 3),
                    "state": _state_after(
                        previous_state,
                        checked_at=checked_at,
                        status=status,
                        effective_url=effective_url,
                        etag=etag,
                        last_modified=last_modified,
                    ),
                }
            )
            return result
    except (OSError, ValueError, ET.ParseError, gzip.BadGzipFile, urllib.error.URLError) as exc:
        result.update(
            {
                "error": str(exc),
                "elapsed_seconds": round(time.perf_counter() - started, 3),
                "state": _state_after(
                    previous_state,
                    checked_at=checked_at,
                    status=result["status"] or "error",
                    effective_url=result["effective_url"],
                    error=str(exc),
                ),
            }
        )
        return result


def collect_feeds(
    feeds: list[dict],
    state: dict,
    *,
    timeout: float,
    max_response_bytes: int,
    max_items: int,
    workers: int,
    user_agent: str,
) -> tuple[list[dict], dict]:
    results: list[dict | None] = [None] * len(feeds)

    def worker(index: int, feed: dict) -> tuple[int, dict]:
        previous = state["feeds"].get(str(feed["url"]), {})
        if not isinstance(previous, dict):
            previous = {}
        try:
            result = fetch_feed(
                feed,
                previous,
                timeout=timeout,
                max_response_bytes=max_response_bytes,
                max_items=max_items,
                user_agent=user_agent,
            )
        except Exception as exc:  # Keep one bad endpoint from aborting the batch.
            result = _result_base(feed)
            result["error"] = str(exc)
            result["state"] = _state_after(
                previous,
                checked_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
                status="error",
                effective_url=str(feed["url"]),
                error=str(exc),
            )
        return index, result

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(worker, index, feed) for index, feed in enumerate(feeds)]
        for future in concurrent.futures.as_completed(futures):
            index, result = future.result()
            results[index] = result

    complete_results = [result for result in results if result is not None]
    articles = [article for result in complete_results for article in result["articles"]]
    articles.sort(key=lambda article: parse_date(str(article.get("published", ""))) or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    state["last_run"] = now_dublin()
    for result in complete_results:
        state["feeds"][result["url"]] = result["state"]
    summary = {
        "feeds_considered": len(feeds),
        "feeds_succeeded": sum(
            1
            for result in complete_results
            if result["status"] in {200, 304} and not result["error"]
        ),
        "feeds_not_modified": sum(1 for result in complete_results if result["not_modified"]),
        "feeds_failed": sum(1 for result in complete_results if result["error"]),
        "article_candidates": len(articles),
        "generated_at": state["last_run"],
    }
    return articles, {"summary": summary, "results": complete_results, "state": state}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path("feed-manifest.json"))
    parser.add_argument("--profile", default="master", help="manifest profile to collect, default: master")
    parser.add_argument("--output", type=Path, help="write a JSON article export here; stdout when omitted")
    parser.add_argument("--state", type=Path, default=Path(".rss-fetch-state.json"))
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--max-items-per-feed", type=int, default=20)
    parser.add_argument("--max-response-bytes", type=int, help="override manifest response limit")
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT)
    parser.add_argument("--dry-run", action="store_true", help="do not update fetch state")
    args = parser.parse_args()

    try:
        if args.timeout <= 0:
            raise ValueError("--timeout must be positive")
        if not 1 <= args.workers <= 32:
            raise ValueError("--workers must be between 1 and 32")
        if args.max_items_per_feed < 1:
            raise ValueError("--max-items-per-feed must be at least 1")
        if args.max_response_bytes is not None and args.max_response_bytes < 1:
            raise ValueError("--max-response-bytes must be positive")
        manifest = load_manifest(args.manifest)
        if args.profile not in profile_settings(manifest):
            raise ValueError(f"unknown profile: {args.profile}")
        feeds = [
            feed for feed in manifest["feeds"] if profile_includes_feed(manifest, args.profile, feed)
        ]
        validation = manifest.get("validation", {})
        max_response_bytes = args.max_response_bytes or int(validation.get("max_response_bytes", 16 * 1024 * 1024))

        lock = file_lock(lock_path(args.state))
        lock_acquired = False
        try:
            lock.__enter__()
            lock_acquired = True
            state = load_state(args.state)
            articles, report = collect_feeds(
                feeds,
                state,
                timeout=args.timeout,
                max_response_bytes=max_response_bytes,
                max_items=args.max_items_per_feed,
                workers=args.workers,
                user_agent=args.user_agent,
            )
            summary = report["summary"]
            payload = {
                "schema_version": 1,
                "generated_at": summary["generated_at"],
                "profile": args.profile,
                "summary": summary,
                "failed_feeds": [
                    {
                        "title": result["title"],
                        "url": result["url"],
                        "error": result["error"],
                    }
                    for result in report["results"]
                    if result["error"]
                ],
                "feed_results": [
                    {
                        key: result[key]
                        for key in (
                            "title",
                            "url",
                            "status",
                            "effective_url",
                            "content_type",
                            "not_modified",
                            "article_count",
                            "skipped_item_count",
                            "feed_title",
                            "elapsed_seconds",
                            "error",
                        )
                    }
                    for result in report["results"]
                ],
                "articles": articles,
            }
            if summary["feeds_failed"] == summary["feeds_considered"] and summary["feeds_considered"]:
                raise RuntimeError("all selected feeds failed; keeping the last good output")
            serialized = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
            if args.output:
                atomic_write_text(args.output, serialized)
            else:
                print(serialized, end="")
            if not args.dry_run:
                atomic_write_text(args.state, json.dumps(state, indent=2, ensure_ascii=False) + "\n")
        finally:
            if lock_acquired:
                lock.__exit__(None, None, None)
    except (OSError, ValueError, json.JSONDecodeError, RuntimeError) as exc:
        print(f"fetch-rss-digest-input: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
