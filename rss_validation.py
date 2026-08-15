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
    "ref",
    "ref_",
}


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

    items: list[dict[str, object]] = []
    for element in root.iter():
        if local_name(element.tag) not in {"item", "entry"}:
            continue
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
    root = ET.parse(path).getroot()
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
                    }
                )
    return entries


def manifest_entries(path: str | Path) -> list[dict]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return list(data.get("feeds", []))


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
        root = ET.parse(value).getroot()
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
        root = ET.parse(value).getroot()
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
