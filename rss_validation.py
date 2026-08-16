"""Shared parsing, normalization and metadata helpers for RSS validation."""

from __future__ import annotations

import html
import hashlib
import json
import time
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timezone
from difflib import SequenceMatcher
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


TRACKING_QUERY_KEYS = {
    "fbclid",
    "gclid",
    "mc_cid",
    "mc_eid",
}

MAX_SAFE_XML_BYTES = 32 * 1024 * 1024


def safe_xml_root(path: str | Path) -> ET.Element:
    """Parse a local feed while rejecting oversized or DTD-bearing XML.

    HTML article bodies are commonly embedded in RSS CDATA and may contain
    their own ``<!DOCTYPE>`` text.  Strip CDATA sections only for the
    pre-parse declaration scan so those literals are not confused with an
    XML document-level DTD; real declarations outside CDATA remain blocked.
    """

    raw = Path(path).read_bytes()
    if len(raw) > MAX_SAFE_XML_BYTES:
        raise ValueError(f"XML document exceeds safe parser limit: {path}")
    declaration_scan = re.sub(rb"<!\[CDATA\[.*?\]\]>", b"", raw, flags=re.DOTALL)
    lowered = declaration_scan.lower()
    if b"<!doctype" in lowered or b"<!entity" in lowered:
        raise ValueError(f"DTD/entity declarations are not allowed: {path}")
    return ET.fromstring(raw)


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].split(":")[-1]


def text_content(element: ET.Element | None) -> str:
    return " ".join("".join(element.itertext()).split()) if element is not None else ""


def child_text(element: ET.Element, names: set[str]) -> str:
    for child in list(element):
        if local_name(child.tag) in names:
            value = text_content(child)
            if value:
                return value
    return ""


def child_link(element: ET.Element) -> str:
    """Return the preferred article link from an RSS item or Atom entry."""

    candidates: list[tuple[int, str]] = []
    for child in list(element):
        if local_name(child.tag) != "link":
            continue
        href = (child.attrib.get("href") or "").strip()
        value = href or text_content(child)
        if not value:
            continue
        rel = (child.attrib.get("rel") or "").lower()
        priority = 0 if rel in {"", "alternate"} else 1
        if url_is_web(value) and value.startswith("https://"):
            priority -= 1
        candidates.append((priority, value))
    if candidates:
        return min(candidates, key=lambda item: item[0])[1]
    return ""


def item_date_raw(element: ET.Element) -> str:
    """Prefer publication time, falling back to update time and legacy date fields."""

    for preferred_names in (
        {"published"},
        {"pubDate"},
        {"updated"},
        {"date"},
    ):
        value = child_text(element, preferred_names)
        if value:
            return value
    return ""


def parse_date(raw: str) -> datetime | None:
    raw = (raw or "").strip()
    if not raw:
        return None
    try:
        parsed = parsedate_to_datetime(raw)
    except (TypeError, ValueError, OverflowError):
        parsed = None
    if parsed is None:
        try:
            parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except ValueError:
            parsed = None
    if parsed is None:
        for fmt in (
            "%Y-%m-%d",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%S.%f%z",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S",
            "%A, %B %d, %Y - %H:%M",
        ):
            try:
                parsed = datetime.strptime(raw, fmt)
                break
            except ValueError:
                pass
    if parsed is None:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def url_is_web(value: str, schemes: tuple[str, ...] = ("http", "https")) -> bool:
    parsed = urlsplit((value or "").strip())
    return parsed.scheme.lower() in schemes and bool(parsed.netloc)


def normalize_title(value: str) -> str:
    """Normalize a title for exact duplicate detection without losing identifiers."""

    value = unicodedata.normalize("NFKC", html.unescape(value or ""))
    value = re.sub(r"<[^>]+>", " ", value)
    value = value.casefold().replace("&", " and ")
    value = re.sub(r"[^\w\d]+", " ", value, flags=re.UNICODE)
    return re.sub(r"\s+", " ", value).strip()


def title_tokens(value: str) -> set[str]:
    return {token for token in normalize_title(value).split() if len(token) > 1}


def similar_titles(left: str, right: str) -> bool:
    """Conservatively detect minor cross-publisher headline variations."""

    left_norm = normalize_title(left)
    right_norm = normalize_title(right)
    if left_norm == right_norm:
        return True
    if min(len(left_norm), len(right_norm)) < 24:
        return False
    left_tokens = title_tokens(left_norm)
    right_tokens = title_tokens(right_norm)
    if len(left_tokens) < 5 or len(right_tokens) < 5:
        return False
    jaccard = len(left_tokens & right_tokens) / len(left_tokens | right_tokens)
    ratio = SequenceMatcher(None, left_norm, right_norm).ratio()
    return jaccard >= 0.65 and ratio >= 0.88


def normalize_link(value: str) -> str:
    """Canonicalize links for duplicate detection, removing common tracking fields."""

    value = (value or "").strip()
    if not value:
        return ""
    parsed = urlsplit(value)
    if not parsed.scheme or not parsed.netloc:
        return ""
    query_pairs = [
        (key, val)
        for key, val in parse_qsl(parsed.query, keep_blank_values=True)
        if key.lower() not in TRACKING_QUERY_KEYS and not key.lower().startswith("utm_")
    ]
    query = urlencode(sorted(query_pairs))
    path = parsed.path.rstrip("/") or "/"
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path, query, ""))


def link_scheme(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return "(none)"
    parsed = urlsplit(value)
    return parsed.scheme.lower() if parsed.scheme else "(none)"


def extract_feed(root: ET.Element) -> tuple[str, list[dict[str, object]]]:
    """Extract feed-level title and item records from RSS, Atom or RDF."""

    root_name = local_name(root.tag)
    feed_title = ""
    if root_name == "rss":
        channel = next((child for child in list(root) if local_name(child.tag) == "channel"), None)
        feed_title = child_text(channel, {"title"}) if channel is not None else ""
    elif root_name == "RDF":
        channel = next((child for child in list(root) if local_name(child.tag) == "channel"), None)
        feed_title = child_text(channel, {"title"}) if channel is not None else ""
    elif root_name == "feed":
        feed_title = child_text(root, {"title"})
    if not feed_title:
        feed_title = child_text(root, {"title"})

    if root_name == "rss":
        channel = next((child for child in list(root) if local_name(child.tag) == "channel"), None)
        item_elements = [child for child in list(channel) if local_name(child.tag) == "item"] if channel is not None else []
    elif root_name == "RDF":
        item_elements = [child for child in list(root) if local_name(child.tag) == "item"]
    elif root_name == "feed":
        item_elements = [child for child in list(root) if local_name(child.tag) == "entry"]
    else:
        item_elements = [element for element in root.iter() if local_name(element.tag) in {"item", "entry"}]

    items: list[dict[str, object]] = []
    for element in item_elements:
        title = child_text(element, {"title"})
        link = child_link(element)
        date = parse_date(item_date_raw(element))
        items.append({"title": title, "link": link, "date": date})
    return feed_title, items


def split_markdown_row(line: str) -> list[str]:
    """Split a Markdown table row while respecting escaped pipe characters."""

    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    columns: list[str] = []
    current: list[str] = []
    escaped = False
    for char in body:
        if escaped:
            current.append(char)
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == "|":
            columns.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    if escaped:
        current.append("\\")
    columns.append("".join(current).strip())
    return columns


def source_table_entries(path: str | Path) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    section = ""
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        if not line.startswith("|"):
            continue
        columns = split_markdown_row(line)
        if len(columns) != 9 or not url_is_web(columns[2]):
            continue
        entries.append(
            {
                "section": section,
                "folder": columns[0],
                "title": columns[1],
                "url": columns[2],
                "purpose": columns[3],
                "signal_type": columns[4],
                "access": columns[5],
                "cadence": columns[6],
                "notification": columns[7],
                "validated": columns[8],
            }
        )
    return entries


def opml_entries(path: str | Path) -> list[dict[str, str | bool]]:
    root = safe_xml_root(path)
    body = next((child for child in list(root) if local_name(child.tag) == "body"), None)
    if body is None:
        return []
    entries: list[dict[str, str | bool]] = []
    for section_outline in list(body):
        section = section_outline.attrib.get("text", section_outline.attrib.get("title", "")).strip()
        for folder_outline in list(section_outline):
            folder = folder_outline.attrib.get("text", folder_outline.attrib.get("title", "")).strip()
            for outline in list(folder_outline):
                url = (outline.attrib.get("xmlUrl") or "").strip()
                if not url:
                    continue
                entries.append(
                    {
                        "section": section,
                        "folder": folder,
                        "title": outline.attrib.get("text", outline.attrib.get("title", "")).strip(),
                        "url": url,
                        "html_url": (outline.attrib.get("htmlUrl") or "").strip(),
                        "event_driven": outline.attrib.get("eventDriven", "").lower() == "true",
                        "item_link_policy": (outline.attrib.get("itemLinkPolicy") or "default").strip().lower(),
                    }
                )
    return entries


def manifest_entries(path: str | Path) -> list[dict]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return list(data.get("feeds", []))


def _snapshot_int(value: object) -> int | None:
    try:
        return int(float(str(value))) if value not in (None, "") else None
    except (TypeError, ValueError):
        return None


def _snapshot_float(value: object) -> float | None:
    try:
        return float(value) if value not in (None, "") else None
    except (TypeError, ValueError):
        return None


def feed_snapshot(detail: dict[str, object]) -> dict[str, object]:
    """Keep the stable, comparable subset of one live feed validation result."""

    return {
        "url": str(detail.get("url", "")),
        "title": str(detail.get("feed_title", "") or ""),
        "root": str(detail.get("root", "") or ""),
        "http_code": str(detail.get("http_code", "") or ""),
        "effective_url": str(detail.get("effective_url", "") or ""),
        "passed": str(detail.get("passed", "") or ""),
        "recent": str(detail.get("recent", "") or ""),
        "staleness_policy": str(detail.get("staleness_policy", "") or ""),
        "item_count": _snapshot_int(detail.get("item_count")),
        "latest_age_days": _snapshot_float(detail.get("latest_age_days")),
        "payload_bytes": _snapshot_int(detail.get("payload_bytes")),
        "wire_bytes": _snapshot_int(detail.get("wire_bytes")),
        "duplicate_title_rate": _snapshot_float(detail.get("duplicate_title_rate")) or 0.0,
        "duplicate_link_rate": _snapshot_float(detail.get("duplicate_link_rate")) or 0.0,
        "http_item_link_count": _snapshot_int(detail.get("http_item_link_count")) or 0,
        "missing_item_link_count": _snapshot_int(detail.get("missing_item_link_count")) or 0,
        "item_link_status": str(detail.get("item_link_status", "") or ""),
        "content_type": str(detail.get("content_type", "") or ""),
    }


def compare_feed_snapshots(
    previous: dict[str, dict[str, object]],
    current: dict[str, dict[str, object]],
    duplicate_rate_limit: float = 0.50,
) -> list[dict[str, object]]:
    """Report meaningful feed drift between two validation runs.

    These are maintenance warnings, not a replacement for the current-run
    hard validation gates. A transient failed fetch is still useful context,
    while the current validator remains responsible for deciding pass/fail.
    """

    warnings: list[dict[str, object]] = []

    def add(
        url: str,
        feed: str,
        kind: str,
        severity: str,
        message: str,
        old_value: object = None,
        new_value: object = None,
    ) -> None:
        warning: dict[str, object] = {
            "url": url,
            "feed": feed or url,
            "kind": kind,
            "severity": severity,
            "message": message,
        }
        if old_value is not None:
            warning["previous"] = old_value
        if new_value is not None:
            warning["current"] = new_value
        warnings.append(warning)

    for url in sorted(set(previous) | set(current)):
        old = previous.get(url)
        new = current.get(url)
        if old is None and new is not None:
            add(url, str(new.get("title", "")), "feed-added", "warning", "feed appeared in the current profile")
            continue
        if new is None and old is not None:
            add(url, str(old.get("title", "")), "feed-removed", "critical", "feed disappeared from the current profile")
            continue
        assert old is not None and new is not None
        feed = str(new.get("title", "") or old.get("title", "") or url)

        if old.get("passed") == "yes" and new.get("passed") != "yes":
            add(
                url,
                feed,
                "validation-regression",
                "critical",
                "feed no longer passes the current validation gates",
                old.get("passed"),
                new.get("passed"),
            )

        old_title = str(old.get("title", ""))
        new_title = str(new.get("title", ""))
        if old_title and new_title and normalize_title(old_title) != normalize_title(new_title):
            add(url, feed, "feed-title-changed", "warning", f"feed title changed from {old_title!r} to {new_title!r}", old_title, new_title)

        old_root = str(old.get("root", ""))
        new_root = str(new.get("root", ""))
        if old_root and new_root and old_root != new_root:
            add(url, feed, "root-changed", "warning", f"document root changed from {old_root!r} to {new_root!r}", old_root, new_root)

        old_effective = str(old.get("effective_url", ""))
        new_effective = str(new.get("effective_url", ""))
        if old_effective and new_effective and old_effective != new_effective:
            add(url, feed, "redirect-target-changed", "warning", "redirect target changed", old_effective, new_effective)

        old_items = _snapshot_int(old.get("item_count"))
        new_items = _snapshot_int(new.get("item_count"))
        if old_items is not None and new_items is not None and old_items > 0:
            if new_items == 0:
                add(url, feed, "item-count-collapse", "critical", "feed item count collapsed to zero", old_items, new_items)
            elif old_items >= 10 and new_items < old_items * 0.50:
                add(url, feed, "item-count-collapse", "warning", "feed item count fell by more than half", old_items, new_items)
            elif old_items >= 10 and new_items > old_items * 2:
                add(url, feed, "item-count-spike", "warning", "feed item count more than doubled", old_items, new_items)

        old_recent = str(old.get("recent", ""))
        new_recent = str(new.get("recent", ""))
        if old_recent in {"yes", "event-driven"} and new_recent == "no":
            add(url, feed, "freshness-regression", "warning", "feed moved from recent/allowed content to stale content", old_recent, new_recent)

        old_payload = _snapshot_int(old.get("payload_bytes"))
        new_payload = _snapshot_int(new.get("payload_bytes"))
        if old_payload and new_payload and old_payload >= 64 * 1024 and new_payload > old_payload * 2:
            add(url, feed, "payload-growth", "warning", "full feed body more than doubled", old_payload, new_payload)

        old_transport = int(old.get("http_item_link_count") or 0) + int(old.get("missing_item_link_count") or 0)
        new_transport = int(new.get("http_item_link_count") or 0) + int(new.get("missing_item_link_count") or 0)
        if new_transport > old_transport:
            add(url, feed, "item-link-transport-regression", "warning", "legacy or missing item links increased", old_transport, new_transport)

        old_title_rate = float(old.get("duplicate_title_rate") or 0.0)
        new_title_rate = float(new.get("duplicate_title_rate") or 0.0)
        old_link_rate = float(old.get("duplicate_link_rate") or 0.0)
        new_link_rate = float(new.get("duplicate_link_rate") or 0.0)
        if old_title_rate <= duplicate_rate_limit < new_title_rate:
            add(url, feed, "duplicate-title-threshold", "warning", "duplicate-title rate crossed the noise threshold", old_title_rate, new_title_rate)
        if old_link_rate <= duplicate_rate_limit < new_link_rate:
            add(url, feed, "duplicate-link-threshold", "warning", "duplicate-link rate crossed the noise threshold", old_link_rate, new_link_rate)

        if str(old.get("content_type", "")).lower() != str(new.get("content_type", "")).lower():
            if old.get("content_type") and new.get("content_type"):
                add(url, feed, "content-type-changed", "warning", "server content-type label changed", old.get("content_type"), new.get("content_type"))

    severity_order = {"critical": 0, "warning": 1}
    warnings.sort(key=lambda item: (severity_order.get(str(item["severity"]), 9), str(item["url"]), str(item["kind"])))
    return warnings


def counter_rates(values: list[str]) -> tuple[int, int, float]:
    counts = Counter(value for value in values if value)
    repeated = sum(count for count in counts.values() if count > 1)
    return len(counts), repeated, (repeated / len(values) if values else 0.0)


def _cli() -> int:
    if len(sys.argv) < 3:
        print("usage: rss_validation.py latest-date FEED_XML | inspect FEED_XML | age-days ISO_DATE | cache-key URL", file=sys.stderr)
        return 2
    operation, value = sys.argv[1:3]
    if operation == "latest-date":
        root = safe_xml_root(value)
        dates = [
            item["date"]
            for element in root.iter()
            if local_name(element.tag) in {"item", "entry"}
            for item in [{"date": parse_date(item_date_raw(element))}]
            if item["date"] is not None
        ]
        if dates:
            print(max(dates).isoformat())
            return 0
        return 1
    if operation == "inspect":
        started = time.perf_counter()
        root = safe_xml_root(value)
        _, items = extract_feed(root)
        dates = [item["date"] for item in items if item["date"] is not None]
        latest = max(dates).isoformat() if dates else ""
        print(f"{latest}\t{time.perf_counter() - started:.6f}\t{len(items)}")
        return 0 if dates else 1
    if operation == "age-days":
        parsed = parse_date(value)
        if parsed is None:
            return 1
        age = (datetime.now(timezone.utc) - parsed).total_seconds() / 86400
        print(f"{age:.1f}")
        return 0
    if operation == "cache-key":
        print(hashlib.sha256(value.encode("utf-8")).hexdigest())
        return 0
    print(f"unknown operation: {operation}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(_cli())
