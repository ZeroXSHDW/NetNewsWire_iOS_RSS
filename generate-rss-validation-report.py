#!/usr/bin/env python3
"""Generate machine-readable and Markdown reports for the RSS bundle validator."""

from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from rss_validation import (
    extract_feed,
    link_scheme,
    compare_feed_snapshots,
    feed_snapshot,
    manifest_entries,
    normalize_link,
    normalize_title,
    opml_entries,
    similar_titles,
    source_table_entries,
    url_is_web,
)


(
    bundle_path,
    table_path,
    fetch_manifest_path,
    markdown_path,
    json_path,
    max_age_raw,
    duplicate_rate_raw,
    min_items_raw,
    validator_path,
    *optional_args,
) = sys.argv[1:]

manifest_path = optional_args[0] if optional_args else str(Path(bundle_path).with_name("feed-manifest.json"))
manifest_profile = optional_args[1] if len(optional_args) > 1 else "master"
history_path = optional_args[2] if len(optional_args) > 2 else ""

MAX_AGE_DAYS = float(max_age_raw)
DUPLICATE_RATE_LIMIT = float(duplicate_rate_raw)
MIN_ITEMS_FOR_NOISE = int(min_items_raw)
MOBILE_REVIEW_BYTES = 256 * 1024
MOBILE_LARGE_BYTES = 1024 * 1024
MOBILE_SLOW_SECONDS = 2.0


def read_manifest(path: str) -> list[dict[str, str]]:
    records = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        fields = line.split("\t")
        if len(fields) < 16:
            continue
        records.append({
            "index": fields[0],
            "url": fields[1],
            "xml_path": fields[2],
            "http_code": fields[3],
            "effective_url": fields[4],
            "https": fields[5],
            "root": fields[6],
            "staleness_policy": fields[7],
            "item_link_status": fields[8],
            "recent": fields[9],
            "shell_age_days": fields[10],
            "shell_latest_date": fields[11],
            "passed": fields[12],
            "content_type": fields[13],
            "etag": fields[14],
            "last_modified": fields[15],
            "payload_bytes": fields[16] if len(fields) > 16 else "",
            "transfer_seconds": fields[17] if len(fields) > 17 else "",
            "wire_bytes": fields[18] if len(fields) > 18 else "",
            "content_encoding": fields[19] if len(fields) > 19 else "",
            "parse_seconds": fields[20] if len(fields) > 20 else "",
            "not_modified": fields[21] if len(fields) > 21 else "no",
        })
    return records


def count_where(details: list[dict[str, object]], predicate) -> int:
    return sum(1 for detail in details if predicate(detail))


records = read_manifest(fetch_manifest_path)
manifest_data = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
all_manifest_feed_list = manifest_entries(manifest_path)
manifest_feed_list = [
    feed
    for feed in all_manifest_feed_list
    if manifest_profile == "master" or feed.get("profiles", {}).get(manifest_profile, False)
]
manifest_by_url = {str(feed["url"]): feed for feed in manifest_feed_list}
opml_record_list = opml_entries(bundle_path)
opml_url_list = [str(entry["url"]) for entry in opml_record_list]
table_record_list = source_table_entries(table_path)
table_url_list = [entry["url"] for entry in table_record_list]
opml_url_set = set(opml_url_list)
table_url_set = set(table_url_list)
manifest_url_list = [str(feed["url"]) for feed in manifest_feed_list]
manifest_url_set = set(manifest_url_list)
duplicate_opml_urls = sorted(url for url, count in Counter(opml_url_list).items() if count > 1)
duplicate_table_urls = sorted(url for url, count in Counter(table_url_list).items() if count > 1)
duplicate_manifest_urls = sorted(url for url, count in Counter(manifest_url_list).items() if count > 1)

notification_display = {
    "on": "**On**",
    "optional": "Optional on",
    "optional-french": "Optional on; French",
    "off": "Off; summarize",
}
metadata_mismatches: list[dict[str, object]] = []
for index, feed in enumerate(manifest_feed_list):
    opml = opml_record_list[index] if index < len(opml_record_list) else None
    table = table_record_list[index] if index < len(table_record_list) else None
    expected_table = {
        "section": feed.get("section", ""),
        "folder": feed.get("folder", ""),
        "title": feed.get("title", ""),
        "url": feed.get("url", ""),
        "purpose": feed.get("purpose", ""),
        "signal_type": feed.get("signal_type", ""),
        "access": feed.get("access", ""),
        "cadence": feed.get("cadence", ""),
        "notification": notification_display.get(feed.get("notification", ""), ""),
        "validated": feed.get("validated", ""),
    }
    differences: dict[str, object] = {}
    if opml is None:
        differences["opml"] = "missing"
    else:
        for key in ("section", "folder", "title", "url", "html_url", "event_driven"):
            expected = feed.get("html_url" if key == "html_url" else key, False if key == "event_driven" else "")
            if opml.get(key) != expected:
                differences[f"opml.{key}"] = {"expected": expected, "actual": opml.get(key)}
    if table is None:
        differences["source_table"] = "missing"
    else:
        for key, expected in expected_table.items():
            if table.get(key) != expected:
                differences[f"source_table.{key}"] = {"expected": expected, "actual": table.get(key)}
    if differences:
        metadata_mismatches.append({"url": feed.get("url", ""), "differences": differences})

manifest_validation = manifest_data.get("validation", {})
MOBILE_REVIEW_BYTES = int(manifest_validation.get("mobile_review_bytes", 256 * 1024))
MOBILE_LARGE_BYTES = int(manifest_validation.get("mobile_large_bytes", 1024 * 1024))
MOBILE_SLOW_SECONDS = float(manifest_validation.get("mobile_slow_seconds", 2.0))
STALE_REVIEW_DEFAULT_DAYS = float(manifest_validation.get("stale_review_default_days", 365))

details: list[dict[str, object]] = []
cross_link_feeds: defaultdict[str, set[str]] = defaultdict(set)
story_records: list[dict[str, object]] = []

for record in records:
    detail: dict[str, object] = dict(record)
    feed_metadata = manifest_by_url.get(record["url"], {})
    detail["manifest_id"] = feed_metadata.get("id", "")
    detail["event_driven"] = bool(feed_metadata.get("event_driven", False))
    detail["freshness_reason"] = feed_metadata.get("freshness_reason", "")
    detail["stale_review_days"] = float(
        feed_metadata.get("stale_review_days", STALE_REVIEW_DEFAULT_DAYS)
    ) if detail["event_driven"] else None
    try:
        root = ET.parse(record["xml_path"]).getroot()
        detail["xml_valid"] = True
        feed_title, items = extract_feed(root)
    except (ET.ParseError, OSError):
        detail["xml_valid"] = False
        feed_title, items = "", []

    detail["feed_title"] = feed_title
    detail["item_count"] = len(items)
    detail["valid_item_title_count"] = sum(1 for item in items if str(item["title"]).strip())
    detail["all_item_titles_valid"] = bool(items) and detail["valid_item_title_count"] == detail["item_count"]
    detail["valid_item_date_count"] = sum(1 for item in items if item["date"] is not None)
    detail["all_item_dates_valid"] = bool(items) and detail["valid_item_date_count"] == detail["item_count"]
    detail["effective_https"] = url_is_web(str(detail["effective_url"])) and str(detail["effective_url"]).lower().startswith("https://")
    content_type = str(detail["content_type"]).lower()
    detail["content_type_unsafe"] = "application/json" in content_type or "text/json" in content_type
    detail["content_type_mislabelled"] = "text/html" in content_type
    detail["content_type_verified"] = bool(
        detail["xml_valid"]
        and detail["root"] in {"rss", "feed", "rdf:RDF", "RDF"}
        and not detail["content_type_unsafe"]
    )
    detail["content_type_mime_safe"] = not detail["content_type_unsafe"] and not detail["content_type_mislabelled"]
    try:
        detail["payload_bytes"] = int(float(str(record.get("payload_bytes", "") or "")))
    except (TypeError, ValueError):
        detail["payload_bytes"] = None
    try:
        detail["transfer_seconds"] = float(str(record.get("transfer_seconds", "") or ""))
    except (TypeError, ValueError):
        detail["transfer_seconds"] = None
    try:
        detail["wire_bytes"] = int(float(str(record.get("wire_bytes", "") or "")))
    except (TypeError, ValueError):
        detail["wire_bytes"] = None
    detail["content_encoding"] = str(record.get("content_encoding", "") or "")
    try:
        detail["parse_seconds"] = float(str(record.get("parse_seconds", "") or ""))
    except (TypeError, ValueError):
        detail["parse_seconds"] = None
    detail["not_modified"] = str(record.get("not_modified", "no") or "no") == "yes"
    payload_bytes = detail["payload_bytes"]
    transfer_seconds = detail["transfer_seconds"]
    if payload_bytes is None:
        detail["mobile_payload_class"] = "unknown"
    elif payload_bytes > MOBILE_LARGE_BYTES:
        detail["mobile_payload_class"] = "large"
    elif payload_bytes > MOBILE_REVIEW_BYTES:
        detail["mobile_payload_class"] = "review"
    else:
        detail["mobile_payload_class"] = "small"
    detail["mobile_refresh_review"] = bool(
        (payload_bytes is not None and payload_bytes > MOBILE_REVIEW_BYTES)
        or (transfer_seconds is not None and transfer_seconds > MOBILE_SLOW_SECONDS)
    )
    title_keys = [normalize_title(str(item["title"])) for item in items if normalize_title(str(item["title"]))]
    link_keys = [normalize_link(str(item["link"])) for item in items if normalize_link(str(item["link"]))]
    title_counts = Counter(title_keys)
    link_counts = Counter(link_keys)
    repeated_title_items = sum(count for count in title_counts.values() if count > 1)
    repeated_link_items = sum(count for count in link_counts.values() if count > 1)
    detail["unique_title_count"] = len(title_counts)
    detail["unique_link_count"] = len(link_counts)
    detail["duplicate_title_rate"] = round(repeated_title_items / len(title_keys), 3) if title_keys else 0.0
    detail["duplicate_link_rate"] = round(repeated_link_items / len(link_keys), 3) if link_keys else 0.0
    detail["valid_item_link_count"] = sum(1 for item in items if url_is_web(str(item["link"])))
    item_link_schemes = Counter(link_scheme(str(item["link"])) for item in items)
    detail["https_item_link_count"] = item_link_schemes.get("https", 0)
    detail["http_item_link_count"] = item_link_schemes.get("http", 0)
    detail["missing_item_link_count"] = item_link_schemes.get("(none)", 0)
    detail["all_item_links_https"] = bool(items) and detail["https_item_link_count"] == detail["item_count"]
    detail["all_item_links_valid"] = bool(
        detail["item_link_status"] == "structured-alert"
        or detail["valid_item_link_count"] == detail["item_count"]
    )
    dated_items = [item["date"] for item in items if item["date"] is not None]
    latest = max(dated_items, default=None)
    detail["latest_item_date"] = latest.isoformat() if latest else ""
    detail["latest_age_days"] = round((datetime.now(timezone.utc) - latest).total_seconds() / 86400, 1) if latest else None
    detail["stale_review_due"] = bool(
        detail["event_driven"]
        and detail["latest_age_days"] is not None
        and detail["stale_review_days"] is not None
        and detail["latest_age_days"] > detail["stale_review_days"]
    )
    detail["future_item_date_count"] = sum(
        1
        for item in items
        if item["date"] is not None
        and item["date"] > datetime.now(timezone.utc).replace(microsecond=0)
    )
    detail["noise_review"] = bool(
        len(items) >= MIN_ITEMS_FOR_NOISE
        and (detail["duplicate_title_rate"] > DUPLICATE_RATE_LIMIT or detail["duplicate_link_rate"] > DUPLICATE_RATE_LIMIT)
    )

    for key in set(link_keys):
        cross_link_feeds[key].add(record["url"])
    for item in items:
        title = str(item["title"]).strip()
        if title:
            story_records.append(
                {
                    "title": title,
                    "url": record["url"],
                    "feed": feed_title or record["url"],
                }
            )
    details.append(detail)

parent = list(range(len(story_records)))


def find_parent(index: int) -> int:
    while parent[index] != index:
        parent[index] = parent[parent[index]]
        index = parent[index]
    return index


def union(left: int, right: int) -> None:
    left_root = find_parent(left)
    right_root = find_parent(right)
    if left_root != right_root:
        parent[right_root] = left_root


# Use shared title tokens to limit fuzzy comparisons to plausible story pairs.
token_index: defaultdict[str, set[int]] = defaultdict(set)
for index, record in enumerate(story_records):
    for token in set(normalize_title(str(record["title"])).split()):
        if len(token) >= 5:
            token_index[token].add(index)
for index, record in enumerate(story_records):
    candidates: set[int] = set()
    for token in set(normalize_title(str(record["title"])).split()):
        if len(token) >= 5:
            candidates.update(token_index[token])
    for other_index in candidates:
        if other_index <= index:
            continue
        other = story_records[other_index]
        if record["url"] != other["url"] and similar_titles(str(record["title"]), str(other["title"])):
            union(index, other_index)

story_groups: defaultdict[int, list[dict[str, object]]] = defaultdict(list)
for index, record in enumerate(story_records):
    story_groups[find_parent(index)].append(record)

duplicate_story_clusters = []
for group in story_groups.values():
    feeds = sorted({str(record["feed"]) for record in group})
    if len(feeds) < 2:
        continue
    titles = sorted({normalize_title(str(record["title"])) for record in group})
    representative = max((str(record["title"]) for record in group), key=len)
    duplicate_story_clusters.append(
        {
            "title": representative,
            "feed_count": len(feeds),
            "feeds": feeds,
            "match_type": "exact" if len(titles) == 1 else "fuzzy",
            "title_variants": len(titles),
        }
    )
duplicate_story_clusters.sort(key=lambda cluster: (-int(cluster["feed_count"]), str(cluster["title"]).casefold()))

duplicate_link_clusters = [
    {"link": link, "feed_count": len(feeds), "feeds": sorted(feeds)}
    for link, feeds in sorted(cross_link_feeds.items(), key=lambda pair: (-len(pair[1]), pair[0]))
    if len(feeds) > 1
]
noisy_feeds = [
    {
        "feed": detail["feed_title"] or detail["url"],
        "url": detail["url"],
        "duplicate_title_rate": detail["duplicate_title_rate"],
        "duplicate_link_rate": detail["duplicate_link_rate"],
    }
    for detail in details
    if detail["noise_review"]
]
item_link_transport_warnings = [
    {
        "feed": detail["feed_title"] or detail["url"],
        "url": detail["url"],
        "http_item_link_count": detail["http_item_link_count"],
        "missing_item_link_count": detail["missing_item_link_count"],
    }
    for detail in details
    if detail["http_item_link_count"] or detail["missing_item_link_count"]
]
mobile_refresh_warnings = [
    {
        "feed": detail["feed_title"] or detail["url"],
        "url": detail["url"],
        "payload_bytes": detail["payload_bytes"],
        "wire_bytes": detail["wire_bytes"],
        "content_encoding": detail["content_encoding"],
        "not_modified": detail["not_modified"],
        "transfer_seconds": detail["transfer_seconds"],
        "payload_class": detail["mobile_payload_class"],
    }
    for detail in details
    if detail["mobile_refresh_review"]
]


def percentile(values: list[float], fraction: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    # Nearest-rank percentile: p95 of 51 values is the 49th value.
    index = min(len(ordered) - 1, max(0, int(len(ordered) * fraction + 0.999999) - 1))
    return ordered[index]

stale_review_failures = [detail for detail in details if detail["stale_review_due"]]
future_date_failures = [detail for detail in details if int(detail["future_item_date_count"]) > 0]

current_snapshots = {
    str(snapshot["url"]): snapshot
    for snapshot in (feed_snapshot(detail) for detail in details)
    if snapshot.get("url")
}
previous_snapshots: dict[str, dict[str, object]] = {}
if history_path:
    try:
        history_data = json.loads(Path(history_path).read_text(encoding="utf-8"))
        profile_history = history_data.get("profiles", {}).get(manifest_profile, {})
        stored_snapshots = profile_history.get("feed_snapshots", {})
        if isinstance(stored_snapshots, dict):
            previous_snapshots = {
                str(url): snapshot
                for url, snapshot in stored_snapshots.items()
                if isinstance(snapshot, dict)
            }
    except (OSError, json.JSONDecodeError, AttributeError):
        previous_snapshots = {}
regression_warnings = (
    compare_feed_snapshots(
        previous_snapshots,
        current_snapshots,
        duplicate_rate_limit=DUPLICATE_RATE_LIMIT,
    )
    if previous_snapshots
    else []
)

summary = {
    "feed_count": len(opml_url_list),
    "unique_url_count": len(opml_url_set),
    "duplicate_url_count": len(duplicate_opml_urls),
    "https_count": sum(url_is_web(url) and url.lower().startswith("https://") for url in opml_url_list),
    "http_200_count": count_where(details, lambda d: d["http_code"] == "200"),
    "not_modified_count": count_where(details, lambda d: d["not_modified"]),
    "successful_response_count": count_where(details, lambda d: d["passed"] == "yes"),
    "parseable_xml_count": count_where(details, lambda d: d["xml_valid"]),
    "recognized_root_count": count_where(details, lambda d: d["root"] in {"rss", "feed", "rdf:RDF", "RDF"}),
    "non_empty_title_count": count_where(details, lambda d: bool(d["feed_title"])),
    "valid_item_url_count": count_where(details, lambda d: d["item_link_status"] == "yes"),
    "structured_alert_exception_count": count_where(details, lambda d: d["item_link_status"] == "structured-alert"),
    "all_item_titles_valid_feed_count": count_where(details, lambda d: d["all_item_titles_valid"]),
    "invalid_item_title_feed_count": count_where(details, lambda d: not d["all_item_titles_valid"]),
    "item_title_total": sum(int(d["item_count"]) for d in details),
    "item_title_valid_total": sum(int(d["valid_item_title_count"]) for d in details),
    "all_item_dates_valid_feed_count": count_where(details, lambda d: d["all_item_dates_valid"]),
    "invalid_item_date_feed_count": count_where(details, lambda d: not d["all_item_dates_valid"]),
    "item_date_total": sum(int(d["item_count"]) for d in details),
    "item_date_valid_total": sum(int(d["valid_item_date_count"]) for d in details),
    "all_item_links_valid_feed_count": count_where(details, lambda d: d["all_item_links_valid"]),
    "invalid_item_link_feed_count": count_where(details, lambda d: not d["all_item_links_valid"]),
    "item_link_total": sum(int(d["item_count"]) for d in details),
    "item_link_valid_total": sum(int(d["valid_item_link_count"]) for d in details),
    "item_link_https_total": sum(int(d["https_item_link_count"]) for d in details),
    "item_link_http_total": sum(int(d["http_item_link_count"]) for d in details),
    "item_link_missing_total": sum(int(d["missing_item_link_count"]) for d in details),
    "all_item_links_https_feed_count": count_where(details, lambda d: d["all_item_links_https"]),
    "http_item_link_feed_count": count_where(details, lambda d: int(d["http_item_link_count"]) > 0),
    "missing_item_link_feed_count": count_where(details, lambda d: int(d["missing_item_link_count"]) > 0),
    "recent_content_count": count_where(details, lambda d: d["recent"] == "yes"),
    "event_driven_feed_count": count_where(details, lambda d: d["staleness_policy"] == "event-driven"),
    "event_driven_stale_count": count_where(details, lambda d: d["recent"] == "event-driven"),
    "recent_or_event_driven_count": count_where(details, lambda d: d["recent"] in {"yes", "event-driven"}),
    "oldest_latest_item_age_days": max((d["latest_age_days"] for d in details if d["latest_age_days"] is not None), default=None),
    "failed_feed_count": count_where(details, lambda d: d["passed"] != "yes"),
    "effective_https_count": count_where(details, lambda d: d["effective_https"]),
    "content_type_verified_count": count_where(details, lambda d: d["content_type_verified"]),
    "content_type_mime_safe_count": count_where(details, lambda d: d["content_type_mime_safe"]),
    "mislabelled_content_type_count": count_where(details, lambda d: d["content_type_mislabelled"]),
    "unsafe_content_type_count": count_where(details, lambda d: d["content_type_unsafe"]),
    "payload_measured_feed_count": count_where(details, lambda d: d["payload_bytes"] is not None),
    "payload_bytes_total": sum(int(d["payload_bytes"]) for d in details if d["payload_bytes"] is not None),
    "payload_bytes_median": percentile([float(d["payload_bytes"]) for d in details if d["payload_bytes"] is not None], 0.50),
    "payload_bytes_p95": percentile([float(d["payload_bytes"]) for d in details if d["payload_bytes"] is not None], 0.95),
    "payload_review_feed_count": count_where(details, lambda d: d["mobile_refresh_review"]),
    "payload_large_feed_count": count_where(details, lambda d: d["mobile_payload_class"] == "large"),
    "slow_refresh_feed_count": count_where(
        details,
        lambda d: d["transfer_seconds"] is not None and d["transfer_seconds"] > MOBILE_SLOW_SECONDS,
    ),
    "max_transfer_seconds": max(
        (float(d["transfer_seconds"]) for d in details if d["transfer_seconds"] is not None),
        default=None,
    ),
    "wire_bytes_total": sum(int(d["wire_bytes"]) for d in details if d["wire_bytes"] is not None),
    "wire_bytes_median": percentile([float(d["wire_bytes"]) for d in details if d["wire_bytes"] is not None], 0.50),
    "wire_bytes_p95": percentile([float(d["wire_bytes"]) for d in details if d["wire_bytes"] is not None], 0.95),
    "wire_bytes_measured_feed_count": count_where(details, lambda d: d["wire_bytes"] is not None),
    "parse_time_measured_feed_count": count_where(details, lambda d: d["parse_seconds"] is not None),
    "parse_seconds_total": sum(float(d["parse_seconds"]) for d in details if d["parse_seconds"] is not None),
    "max_parse_seconds": max(
        (float(d["parse_seconds"]) for d in details if d["parse_seconds"] is not None),
        default=None,
    ),
    "cross_feed_duplicate_title_clusters": len(duplicate_story_clusters),
    "cross_feed_duplicate_link_clusters": len(duplicate_link_clusters),
    "fuzzy_duplicate_story_clusters": sum(1 for cluster in duplicate_story_clusters if cluster["match_type"] == "fuzzy"),
    "noisy_feed_count": len(noisy_feeds),
    "max_age_days": MAX_AGE_DAYS,
    "duplicate_title_rate_limit": DUPLICATE_RATE_LIMIT,
    "min_items_for_noise": MIN_ITEMS_FOR_NOISE,
    "opml_table_url_sets_match": opml_url_set == table_url_set,
    "manifest_opml_url_order_match": manifest_url_list == opml_url_list,
    "manifest_table_url_order_match": manifest_url_list == table_url_list,
    "manifest_feed_count": len(manifest_feed_list),
    "manifest_duplicate_url_count": len(duplicate_manifest_urls),
    "table_url_count": len(table_url_list),
    "source_table_row_count": len(table_record_list),
    "source_table_metadata_complete_count": sum(1 for row in table_record_list if all(row.values())),
    "source_table_incomplete_row_count": sum(1 for row in table_record_list if not all(row.values())),
    "source_table_duplicate_url_count": len(duplicate_table_urls),
    "metadata_mismatch_count": len(metadata_mismatches),
    "stale_review_due_count": len(stale_review_failures),
    "future_item_date_feed_count": len(future_date_failures),
    "future_item_date_total": sum(int(d["future_item_date_count"]) for d in details),
    "drift_baseline_available": bool(previous_snapshots),
    "regression_warning_count": len(regression_warnings),
    "regression_critical_count": sum(1 for warning in regression_warnings if warning["severity"] == "critical"),
}

hard_failure = bool(
    summary["failed_feed_count"]
    or summary["duplicate_url_count"]
    or not summary["opml_table_url_sets_match"]
    or summary["invalid_item_title_feed_count"]
    or summary["invalid_item_date_feed_count"]
    or summary["invalid_item_link_feed_count"]
    or summary["effective_https_count"] != summary["feed_count"]
    or summary["unsafe_content_type_count"]
    or summary["source_table_row_count"] != summary["feed_count"]
    or summary["source_table_incomplete_row_count"]
    or summary["source_table_duplicate_url_count"]
    or summary["noisy_feed_count"]
    or not summary["manifest_opml_url_order_match"]
    or not summary["manifest_table_url_order_match"]
    or summary["manifest_duplicate_url_count"]
    or summary["metadata_mismatch_count"]
    or summary["stale_review_due_count"]
    or summary["future_item_date_feed_count"]
)

try:
    local_now = datetime.now(ZoneInfo("Europe/Dublin"))
except Exception:
    local_now = datetime.now().astimezone()
generated_at = local_now.isoformat(timespec="seconds")
display_date = local_now.strftime("%d %B %Y %H:%M %Z")

payload = {
    "generated_at": generated_at,
    "profile": manifest_profile,
    "bundle": str(Path(bundle_path).resolve()),
    "source_table": str(Path(table_path).resolve()),
    "manifest": str(Path(manifest_path).resolve()),
    "validator": str(Path(validator_path).resolve()),
    "summary": summary,
    "failed_feeds": [detail for detail in details if detail["passed"] != "yes" or detail["stale_review_due"] or detail["future_item_date_count"]],
    "metadata_mismatches": metadata_mismatches,
    "stale_review_failures": stale_review_failures,
    "future_date_failures": future_date_failures,
    "noisy_feeds": noisy_feeds,
    "item_link_transport_warnings": item_link_transport_warnings,
    "mobile_refresh_warnings": mobile_refresh_warnings,
    "regression_warnings": regression_warnings,
    "duplicate_story_clusters": duplicate_story_clusters[:100],
    "duplicate_link_clusters": duplicate_link_clusters[:100],
    "feeds": details,
}

json_destination = Path(json_path)
json_destination.parent.mkdir(parents=True, exist_ok=True)
json_destination.write_text(json.dumps(payload, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")


def md(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def human_bytes(value: object) -> str:
    if value is None:
        return "—"
    amount = float(value)
    if amount >= 1024 * 1024:
        return f"{amount / (1024 * 1024):.2f} MB"
    return f"{amount / 1024:.1f} KB"


lines = [
    f"# NetNewsWire Finance + Cyber Validation Report — {manifest_profile}",
    "",
    f"Validation date: {display_date} (Europe/Dublin)",
    "",
    "Command:",
    "",
    f"```text\n{validator_path}\n```",
    "",
    "## Results",
    "",
    "| Check | Result |",
    "|---|---:|",
    f"| Feed elements in OPML | {summary['feed_count']} |",
    f"| Unique feed URLs | {summary['unique_url_count']} |",
    f"| Duplicate URLs | {summary['duplicate_url_count']} |",
    f"| HTTPS feed URLs | {summary['https_count']}/{summary['feed_count']} |",
    f"| Effective URLs remain HTTPS | {summary['effective_https_count']}/{summary['feed_count']} |",
    f"| HTTP 200 responses | {summary['http_200_count']}/{summary['feed_count']} |",
    f"| Conditional 304 responses reused from cache | {summary['not_modified_count']} |",
    f"| Successful responses including cached 304s | {summary['successful_response_count']}/{summary['feed_count']} |",
    f"| Feed bodies verified as RSS/XML (not JSON) | {summary['content_type_verified_count']}/{summary['feed_count']} |",
    f"| MIME labels explicitly XML/RSS/Atom | {summary['content_type_mime_safe_count']}/{summary['feed_count']} |",
    f"| MIME-labelled HTML but verified XML body | {summary['mislabelled_content_type_count']} |",
    f"| Feed payload measured | {summary['payload_measured_feed_count']}/{summary['feed_count']} |",
    f"| Total feed payload in this audit | {human_bytes(summary['payload_bytes_total'])} |",
    f"| Median feed payload | {human_bytes(summary['payload_bytes_median'])} |",
    f"| 95th-percentile feed payload | {human_bytes(summary['payload_bytes_p95'])} |",
    f"| Compressed/wire bytes measured | {summary['wire_bytes_measured_feed_count']}/{summary['feed_count']} |",
    f"| Total measured wire bytes | {human_bytes(summary['wire_bytes_total'])} |",
    f"| 95th-percentile wire bytes | {human_bytes(summary['wire_bytes_p95'])} |",
    f"| Feed parse time measured | {summary['parse_time_measured_feed_count']}/{summary['feed_count']} |",
    f"| Total feed parse time | {summary['parse_seconds_total']:.3f} seconds |",
    f"| Slowest feed parse | {summary['max_parse_seconds']:.3f} seconds |" if summary['max_parse_seconds'] is not None else "| Slowest feed parse | — |",
    f"| Feeds over mobile review threshold ({MOBILE_REVIEW_BYTES // 1024} KB) | {summary['payload_review_feed_count']} |",
    f"| Feeds over 1 MB | {summary['payload_large_feed_count']} |",
    f"| Fetches over {MOBILE_SLOW_SECONDS:.0f} seconds | {summary['slow_refresh_feed_count']} |",
    f"| Slowest measured fetch | {summary['max_transfer_seconds']:.2f} seconds |" if summary['max_transfer_seconds'] is not None else "| Slowest measured fetch | — |",
    f"| Parseable XML documents | {summary['parseable_xml_count']}/{summary['feed_count']} |",
    f"| RSS/Atom/RSS 1.0 roots | {summary['recognized_root_count']}/{summary['feed_count']} |",
    f"| Non-empty feed titles | {summary['non_empty_title_count']}/{summary['feed_count']} |",
    f"| Valid item URLs | {summary['valid_item_url_count']}/{summary['feed_count']} |",
    f"| Structured alert identity | {summary['structured_alert_exception_count']}/{summary['feed_count']} |",
    f"| Item titles with text | {summary['item_title_valid_total']}/{summary['item_title_total']} |",
    f"| Feeds with all item titles valid | {summary['all_item_titles_valid_feed_count']}/{summary['feed_count']} |",
    f"| Item dates with valid timestamps | {summary['item_date_valid_total']}/{summary['item_date_total']} |",
    f"| Feeds with all item dates valid | {summary['all_item_dates_valid_feed_count']}/{summary['feed_count']} |",
    f"| Feeds with all item URLs valid (exception-aware) | {summary['all_item_links_valid_feed_count']}/{summary['feed_count']} |",
    f"| Item URLs with HTTP(S) links | {summary['item_link_valid_total']}/{summary['item_link_total']} |",
    f"| Item URLs using HTTPS | {summary['item_link_https_total']}/{summary['item_link_total']} |",
    f"| Item URLs using legacy HTTP | {summary['item_link_http_total']} |",
    f"| Items without a per-item URL | {summary['item_link_missing_total']} |",
    f"| Feeds with any legacy HTTP item links | {summary['http_item_link_feed_count']} |",
    f"| Feeds with any missing item links | {summary['missing_item_link_feed_count']} |",
    f"| Recent content, default max age {int(MAX_AGE_DAYS)} days | {summary['recent_content_count']}/{summary['feed_count']} |",
    f"| Feeds marked event-driven in OPML | {summary['event_driven_feed_count']}/{summary['feed_count']} |",
    f"| Stale feeds allowed by event-driven policy | {summary['event_driven_stale_count']} |",
    f"| Recent or allowed event-driven content | {summary['recent_or_event_driven_count']}/{summary['feed_count']} |",
    f"| Oldest detected current item | {summary['oldest_latest_item_age_days']} days |",
    f"| Cross-feed duplicate title clusters | {summary['cross_feed_duplicate_title_clusters']} |",
    f"| Cross-feed duplicate link clusters | {summary['cross_feed_duplicate_link_clusters']} |",
    f"| Fuzzy duplicate title clusters | {summary['fuzzy_duplicate_story_clusters']} |",
    f"| Feeds over noise review threshold | {summary['noisy_feed_count']} |",
    f"| OPML/source-table URL sets | {'Match' if summary['opml_table_url_sets_match'] else 'MISMATCH'} |",
    f"| Manifest feeds | {summary['manifest_feed_count']} |",
    f"| Manifest/OPML URL order | {'Match' if summary['manifest_opml_url_order_match'] else 'MISMATCH'} |",
    f"| Manifest/source-table URL order | {'Match' if summary['manifest_table_url_order_match'] else 'MISMATCH'} |",
    f"| Source-table rows | {summary['source_table_row_count']}/{summary['feed_count']} |",
    f"| Source-table rows with complete metadata | {summary['source_table_metadata_complete_count']}/{summary['feed_count']} |",
    f"| Metadata mismatches | {summary['metadata_mismatch_count']} |",
    f"| Source-table duplicate URLs | {summary['source_table_duplicate_url_count']} |",
    f"| Stale-review deadlines due | {summary['stale_review_due_count']} |",
    f"| Future-dated items | {summary['future_item_date_total']} |",
    f"| Failed feeds | {summary['failed_feed_count']} |",
    f"| Cross-run drift baseline available | {'Yes' if summary['drift_baseline_available'] else 'No — this run establishes it'} |",
    f"| Cross-run drift warnings | {summary['regression_warning_count']} ({summary['regression_critical_count']} critical) |",
    "",
    "Duplicate-story clusters are reported for Apple Intelligence deduplication. A feed crosses the noise gate when it has at least "
    f"{MIN_ITEMS_FOR_NOISE} items and more than {DUPLICATE_RATE_LIMIT:.0%} repeated item titles or links.",
    "",
    "Every retained item must have a non-empty title and a parseable publication/update date. Item-link transport is reported separately: direct feed endpoints must remain HTTPS, while legacy HTTP article links are warnings rather than hard failures when the feed itself is a verified HTTPS RSS/XML source. The Nasdaq Trade Halts feed is a deliberate structured-alert exception only for per-item URLs: its entries contain halt fields and titles but no per-item URLs.",
    f"Mobile refresh telemetry measures the full response body and compressed/wire transfer separately. Feed bodies over {MOBILE_REVIEW_BYTES // 1024} KB are flagged for review, bodies over 1 MB are marked large, and fetches over {MOBILE_SLOW_SECONDS:.0f} seconds are flagged as slow. The validator also reuses a local ETag/Last-Modified cache and reports conditional 304 responses; NetNewsWire refreshes can be smaller when servers honor validators.",
    "Normal feeds must have a detectable item date within the configured age window. Event-driven feeds require a documented freshness reason and have a manifest-level stale-review deadline; they still must pass every other structural and integrity check.",
    "The manifest is the source of truth for feed identity, folder, profile, freshness and notification policy. The validator compares it with both the OPML and the source table, including ordered metadata fields.",
    "",
    "## Feed health",
    "",
    "| Feed | HTTP | Cache | Root | Final HTTPS | Content type | Body | Wire | Encoding | Fetch s | Parse s | Freshness policy | Recent | Items | Missing titles | Missing dates | HTTPS item links | HTTP item links | Missing item links | Latest age | Duplicate titles | Duplicate links | Redirected | ETag / Last-Modified |",
    "|---|---:|---|---|---|---|---:|---:|---|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|",
]

for detail in details:
    redirected = "yes" if detail["effective_url"] and detail["effective_url"] != detail["url"] else "no"
    validators = f"{detail['etag'] or '—'} / {detail['last_modified'] or '—'}"
    lines.append(
        "| " + " | ".join([
            md(detail["feed_title"] or detail["url"]),
            md(detail["http_code"]),
            "yes" if detail["not_modified"] else "no",
            md(detail["root"] or "—"),
            "yes" if detail["effective_https"] else "no",
            md(detail["content_type"] or "—"),
            md(f"{human_bytes(detail['payload_bytes'])} ({detail['mobile_payload_class']})"),
            md(human_bytes(detail["wire_bytes"])),
            md(detail["content_encoding"] or "identity"),
            md(f"{detail['transfer_seconds']:.2f}" if detail["transfer_seconds"] is not None else "—"),
            md(f"{detail['parse_seconds']:.3f}" if detail["parse_seconds"] is not None else "—"),
            md(detail["staleness_policy"]),
            md(detail["recent"]),
            md(detail["item_count"]),
            md(detail["item_count"] - detail["valid_item_title_count"]),
            md(detail["item_count"] - detail["valid_item_date_count"]),
            md(detail["https_item_link_count"]),
            md(detail["http_item_link_count"]),
            md(detail["missing_item_link_count"]),
            md(detail["latest_age_days"] if detail["latest_age_days"] is not None else "—"),
            md(f"{detail['duplicate_title_rate']:.1%}"),
            md(f"{detail['duplicate_link_rate']:.1%}"),
            redirected,
            md(validators),
        ]) + " |"
    )

lines.extend(["", "## Cross-run drift review", ""])
if regression_warnings:
    lines.append("These advisory comparisons use the previous per-feed validation snapshot for this profile:")
    lines.extend(
        f"- **{md(item['feed'])}** — `{item['severity']}` `{item['kind']}`: {md(item['message'])}."
        for item in regression_warnings[:100]
    )
elif summary["drift_baseline_available"]:
    lines.append("No feed identity, freshness, payload, item-count, link-transport or noise-threshold drift was detected against the previous snapshot.")
else:
    lines.append("No prior per-feed snapshot was available; this run establishes the baseline for the next maintenance check.")

lines.extend(["", "## Duplicate-story clusters detected", ""])
if duplicate_story_clusters:
    lines.append("These are candidates for one Apple Intelligence summary with multiple corroborating sources:")
    lines.extend(
        f"- **{md(cluster['title'])}** — {cluster['feed_count']} feeds; {cluster['match_type']} match: {', '.join(md(name) for name in cluster['feeds'])}"
        for cluster in duplicate_story_clusters[:25]
    )
else:
    lines.append("No cross-feed story duplicates were detected in the current snapshots.")

if duplicate_link_clusters:
    lines.extend(["", "## Duplicate-link clusters detected", ""])
    lines.extend(
        f"- `{md(cluster['link'])}` — {cluster['feed_count']} feeds: {', '.join(md(name) for name in cluster['feeds'])}"
        for cluster in duplicate_link_clusters[:25]
    )

if noisy_feeds:
    lines.extend(["", "## Noise review required", ""])
    lines.extend(
        f"- **{md(item['feed'])}** — duplicate titles {item['duplicate_title_rate']:.1%}; duplicate links {item['duplicate_link_rate']:.1%}."
        for item in noisy_feeds
    )

if item_link_transport_warnings:
    lines.extend(["", "## Item-link transport warnings", ""])
    lines.append(
        "These warnings do not fail the bundle because the direct feed endpoints are HTTPS and the links are still valid HTTP(S) URLs; review them if a source changes its link policy."
    )
    lines.extend(
        f"- **{md(item['feed'])}** — legacy HTTP item links: {item['http_item_link_count']}; missing per-item URLs: {item['missing_item_link_count']}."
        for item in item_link_transport_warnings
    )

if mobile_refresh_warnings:
    lines.extend(["", "## Mobile refresh review", ""])
    lines.append(
        f"These feeds exceed the advisory mobile threshold of {MOBILE_REVIEW_BYTES // 1024} KB or took more than {MOBILE_SLOW_SECONDS:.0f} seconds in this full-response audit. They are not failures; review them if refresh cost becomes noticeable on iPhone."
    )
    lines.extend(
        f"- **{md(item['feed'])}** — body {human_bytes(item['payload_bytes'])}; wire {human_bytes(item['wire_bytes'])}; encoding `{item['content_encoding'] or 'identity'}`; fetch {item['transfer_seconds']:.2f}s; class `{item['payload_class']}`; cached 304 `{item['not_modified']}`."
        for item in mobile_refresh_warnings
    )

if payload["failed_feeds"]:
    lines.extend(["", "## Failed feeds", ""])
    lines.extend(
        f"- `{detail['url']}` — HTTP {detail['http_code']}, root `{detail['root'] or 'unavailable'}`, recent `{detail['recent']}`, stale review due `{detail['stale_review_due']}`, future dates `{detail['future_item_date_count']}`."
        for detail in payload["failed_feeds"]
    )

if metadata_mismatches:
    lines.extend(["", "## Metadata mismatches", ""])
    lines.extend(
        f"- `{item['url']}` — {', '.join(item['differences'])}"
        for item in metadata_mismatches
    )

lines.extend([
    "",
    "## Coverage audit",
    "",
    "- **Finance**: US, UK, Irish, euro-area and global market context; SEC, CFTC, Federal Reserve speeches and monetary policy, ECB press, market operations and statistical releases, Central Bank of Ireland, Bank of England, HM Treasury, FCA, Eurostat, ONS, BIS and European Commission sanctions guidance; Nasdaq trade halts and Equity Trader Alerts; EUR/USD and EUR/GBP reference data. BEA was tested but rejected for one malformed historical item link.",
    "- **Cyber**: Ireland NCSC, CISA, CISA ICS, CERT-EU, UK NCSC, CERT/CC, NIST, Microsoft, Mandiant, Cisco PSIRT, Cisco Talos, OpenSSF and CrowdStrike, plus independent incident reporting and technical research.",
    "- **Ireland/EU/UK/US scope**: present in official alerts, regulation, macro data and market coverage.",
    "- **Coverage-gap decisions**: see [Coverage-Gap-Assessment.md](Coverage-Gap-Assessment.md) for tested candidates, exact rejection reasons and next-addition triggers.",
    "",
    "## Notification recommendation",
    "",
    "**On:** Nasdaq Trade Halts, Ireland NCSC Alerts, CISA All Advisories and CERT-EU Security Advisories.",
    "",
    "**Optional:** Central Bank of Ireland News, Federal Reserve Monetary Policy, ECB Press, Bank of England News, UK NCSC All Updates, CISA ICS Advisories and Cisco PSIRT.",
    "",
    "**Off and summarize in batches:** commercial market news, RTÉ/BBC business news, CFTC regulatory releases, ECB market operations and statistical releases, Eurostat/ONS/BIS data, European Commission sanctions guidance, Federal Reserve speeches, Bank of England Publications, CERT/CC vulnerability notes, incident reporting, research feeds, exchange-rate data and broad regulatory context.",
    "",
    "## Strong candidates retained outside the OPML",
    "",
    "- **BIS Data Portal `https://data.bis.org/feed.xml`**: valid HTTPS RSS, but the current release-calendar feed contains many repeated dataset items and links; the lower-noise BIS Statistical Releases feed is retained instead.",
    "- **CSO Ireland release calendar**: valuable official web calendar, but no verified direct RSS/Atom endpoint was retained in this pass.",
    "- **Ireland Department of Finance / gov.ie**: valuable official fiscal and budget coverage, but tested RSS paths were blocked or unavailable; no direct validated RSS/Atom endpoint was retained.",
    "- **Euronext Dublin notices**: official notices are available through Euronext web/portal services, but no verified direct public RSS/Atom feed was retained.",
    "- **UK NCSC Reports feed**: valid, but it overlaps the retained UK NCSC All Updates feed; adding both would duplicate stories.",
    "- **CISA Known Exploited Vulnerabilities catalogue**: useful for a separate structured-data monitor, but not a direct RSS/Atom feed.",
    "- **U.S. Treasury press releases**: valuable official fiscal and macro context, but no verified direct HTTPS RSS/Atom endpoint was retained.",
    "- **Apple security releases**: valuable for iPhone security, but the official page is HTML rather than a direct RSS/Atom feed.",
    "- **Federal Reserve H.10 XML feed**: reachable and current, but rejected because its 92-entry stream had 40.2% repeated titles and 100% repeated item links; its HTML page was not used either.",
    "- **BLS Latest Numbers `https://www.bls.gov/feed/bls_latest.rss`**: authoritative US macro feed, but the current endpoint returned HTTP 403 and was not imported.",
    "- **ECB Yield Curve `https://www.ecb.europa.eu/rss/yc.html`**: valid RSS, but the newest actual data item is from 2017 and therefore fails the recent-content rule.",
    "- **ESMA `https://www.esma.europa.eu/rss.xml`**: direct HTTPS RSS and useful EU market-regulator coverage, but its current items contain no detectable publication date; it fails the date-integrity requirement and remains a web reference.",
    "- **BEA News Releases `https://apps.bea.gov/rss/rss.xml`**: useful official US macro coverage, but one historical item contains a schemeless `www.bea.gov/...` link; alternate BEA paths did not provide a clean RSS feed, so it was not imported.",
    "- **FINRA RSS feeds**: FINRA documents official feeds, but the published endpoints are HTTP-only and the HTTPS transport did not provide a reliable XML response; none were imported.",
    "- **NYSE trading halts**: NYSE provides a live web page and CSV/email or proprietary market-data services, not a verified direct public RSS/Atom feed; it remains a web reference.",
    "- **Euronext Dublin market notices**: Euronext’s public notices are available through web/portal services; the directly testable RSS endpoint found was for Euronext Athens, not Dublin, so it was not imported.",
    "- **Euronext Press Releases `https://www.euronext.com/en/press-releases/rss.xml`**: valid RSS transport, but the current ten-item response contains 2021–2022 releases and no detectable item dates; it is not a current Dublin market-notice stream.",
    "- **Nasdaq Current Headlines `https://www.nasdaqtrader.com/rss.aspx?feed=currentheadlines&categorylist=0`**: valid XML, but 679 mixed-category items and roughly 604 KB per full response made it too broad for a focused iPhone bundle; the narrower Equity Trader Alerts stream was retained.",
    "- **Nasdaq Equity Regulatory/Technical Updates**: valid but too sparse in the tested responses to add distinct value beyond the retained Equity Trader Alerts stream and Trade Halts feed.",
    "- **ENISA legacy RSS URLs**: the historical news and press-release RSS endpoints returned HTTP 404; current CERT-EU feeds cover the operational advisory and threat-intelligence gap instead.",
    "- **NVD RSS candidate `https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss.xml`**: HTTP 404; current official NVD feeds are structured JSON/XML rather than RSS/Atom.",
    "- **Google Project Zero `https://projectzero.google/feed.xml`**: parseable and high quality, but roughly 13 MB for 10 entries in the current response; excluded for mobile refresh cost.",
    "",
    "## Apple Intelligence guardrails",
    "",
    "Use the [Apple Intelligence RSS summary prompt](Apple-Intelligence-RSS-Summary-Prompt.md), [NetNewsWire setup plan](NetNewsWire-Setup-and-Notification-Plan.md) and [market-hours reference](Market-Hours-and-Holiday-Reference.md) for deduplication, confidence labels, Dublin-time conversion, exchange-session state and notification control.",
    "",
    "Finance summaries must identify the event, asset/ticker, catalyst, Dublin timing, confirmed facts, speculation, risks and sources, without a buy/sell recommendation.",
    "",
    "Cyber summaries must identify the affected product or organization, CVE/advisory, exploitation status, attack type, Ireland/EU relevance, mitigation, urgency and sources, without inventing technical details or claiming exploitation without evidence.",
    "",
    "RSS is not live market data: it does not provide live quotes, order books, broker execution, portfolio positions or trade IDs.",
    "",
    "## Machine-readable report",
    "",
    f"Full per-feed JSON: [{Path(json_path).name}]({Path(json_path).name})",
])

markdown_destination = Path(markdown_path)
markdown_destination.parent.mkdir(parents=True, exist_ok=True)
markdown_destination.write_text("\n".join(lines) + "\n", encoding="utf-8")

print(f"report markdown={markdown_destination}")
print(f"report json={json_destination}")
print(
    "integrity "
    f"table_url_sets_match={'yes' if summary['opml_table_url_sets_match'] else 'no'} "
    f"duplicate_urls={summary['duplicate_url_count']} noisy_feeds={summary['noisy_feed_count']}"
)
raise SystemExit(1 if hard_failure else 0)
