#!/usr/bin/env python3
"""Prepare a deduplicated, stateful input package for the daily RSS digest."""

from __future__ import annotations

import argparse
import html
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from zoneinfo import ZoneInfo

from bundle_config import (
    load_manifest,
    profile_digest_budget,
    profile_includes_feed,
    profile_settings,
)
from rss_validation import normalize_link, normalize_title, parse_date, similar_titles, url_is_web
from state_utils import atomic_write_text, file_lock, lock_path


def load_articles(path: Path) -> list[dict]:
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return []
    try:
        decoded = json.loads(raw)
        if isinstance(decoded, dict):
            decoded = decoded.get("articles", [])
        if not isinstance(decoded, list):
            raise ValueError("JSON input must be an array or an object with an articles array")
        return [article for article in decoded if isinstance(article, dict)]
    except json.JSONDecodeError:
        articles = []
        for line_number, line in enumerate(raw.splitlines(), start=1):
            try:
                article = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSON on line {line_number}: {exc}") from exc
            if isinstance(article, dict):
                articles.append(article)
        return articles


def article_id(article: dict) -> str:
    link = normalize_link(str(article.get("link", "")))
    title = normalize_title(str(article.get("title", "")))
    published = str(article.get("published", "")).strip()
    source = normalize_link(str(article.get("feed_url") or article.get("feedUrl") or ""))
    if not source:
        source = normalize_title(str(article.get("feed", "")))
    identity = link or "|".join((title, published, source))
    if not identity:
        raise ValueError("article needs a link or title/published identity")
    return hashlib.sha256(identity.encode("utf-8")).hexdigest()[:20]


def load_manifest_index(path: Path) -> tuple[dict[str, dict], dict[str, list[dict]], dict[str, set[str]]]:
    data = load_manifest(path)
    feeds = data.get("feeds")
    by_url: dict[str, dict] = {}
    by_title: dict[str, list[dict]] = {}
    profile_modes = {
        name: {
            str(feed.get("id"))
            for feed in feeds
            if isinstance(feed, dict) and profile_includes_feed(data, name, feed)
        }
        for name in profile_settings(data)
    }
    for feed in feeds:
        if not isinstance(feed, dict):
            continue
        url = str(feed.get("url", "")).strip()
        title = str(feed.get("title", "")).strip()
        if url:
            by_url[url] = feed
            normalized_url = normalize_link(url)
            if normalized_url:
                by_url[normalized_url] = feed
        if title:
            by_title.setdefault(normalize_title(title), []).append(feed)
    return by_url, by_title, profile_modes


def clean_text(value: object) -> str:
    raw = str(value or "")
    if "<" in raw and ">" in raw:
        raw = re.sub(r"<script\b[^>]*>.*?</script\s*>", " ", raw, flags=re.IGNORECASE | re.DOTALL)
        raw = re.sub(r"<style\b[^>]*>.*?</style\s*>", " ", raw, flags=re.IGNORECASE | re.DOTALL)

        class TextExtractor(HTMLParser):
            def __init__(self) -> None:
                super().__init__(convert_charrefs=True)
                self.parts: list[str] = []

            def handle_data(self, data: str) -> None:
                self.parts.append(data)

        parser = TextExtractor()
        try:
            parser.feed(raw)
            parser.close()
            raw = " ".join(parser.parts)
        except (AssertionError, ValueError):
            pass
    return " ".join(html.unescape(raw).split())


def resolve_manifest_feed(
    article: dict,
    by_url: dict[str, dict],
    by_title: dict[str, list[dict]],
) -> tuple[dict | None, str]:
    explicit_feed_url = clean_text(article.get("feed_url") or article.get("feedUrl") or "")
    if explicit_feed_url:
        metadata = by_url.get(explicit_feed_url) or by_url.get(normalize_link(explicit_feed_url))
        if metadata:
            return metadata, "manifest-url"
    raw_feed_title = clean_text(article.get("feed", ""))
    feed_title = normalize_title(raw_feed_title)
    matches = by_title.get(feed_title, []) if feed_title else []
    if len(matches) == 1:
        return matches[0], "manifest-title"
    if len(matches) > 1:
        return None, "ambiguous-feed-title"
    if explicit_feed_url:
        return None, "unmatched-feed-url"
    return None, "unmatched-feed-title" if raw_feed_title else "unmatched"


def truncate_text(value: str, limit: int) -> tuple[str, bool]:
    if len(value) <= limit:
        return value, False
    if limit <= 1:
        return ("…" if limit else ""), True
    shortened = value[: limit - 1].rstrip()
    return shortened + "…", True


def bounded_text_fields(article: dict, max_item_chars: int) -> tuple[str, str, bool]:
    summary = clean_text(article.get("summary", ""))
    content = clean_text(article.get("content", ""))
    if summary and content:
        summary_limit = min(len(summary), max_item_chars // 3)
        content_limit = max(0, max_item_chars - summary_limit)
    elif summary:
        summary_limit = max_item_chars
        content_limit = 0
    else:
        summary_limit = 0
        content_limit = max_item_chars
    summary, summary_truncated = truncate_text(summary, summary_limit)
    content, content_truncated = truncate_text(content, content_limit)
    return summary, content, summary_truncated or content_truncated


def article_record(
    article: dict,
    by_url: dict[str, dict],
    by_title: dict[str, list[dict]],
    profile_modes: dict[str, set[str]],
    max_item_chars: int,
) -> dict:
    title = " ".join(str(article.get("title", "")).split())
    link = str(article.get("link", "")).strip()
    if not title:
        raise ValueError("article title is empty")
    if not url_is_web(link):
        raise ValueError(f"article link is not an HTTP(S) URL: {link!r}")
    published = str(article.get("published", "")).strip()
    parsed = parse_date(published) if published else None
    metadata, source_match = resolve_manifest_feed(article, by_url, by_title)
    summary, content, text_truncated = bounded_text_fields(article, max_item_chars)
    input_feed_url = clean_text(article.get("feed_url") or article.get("feedUrl") or "")
    date_quality = "valid" if parsed else ("missing" if not published else "invalid")
    record = {
        "id": article_id(article),
        "title": title,
        "link": link,
        "feed": str(metadata.get("title", "")) if metadata else clean_text(article.get("feed", "")),
        "published": parsed.isoformat() if parsed else published,
        "date_quality": date_quality,
        "summary": summary,
        "content": content,
        "source_class": str(article.get("source_class", "")).strip() or (str(metadata.get("signal_type", "")) if metadata else ""),
        "language": clean_text(article.get("language", "")),
        "source_match": source_match,
        "text_characters": len(summary) + len(content),
        "text_truncated": text_truncated,
    }
    if metadata:
        record.update(
            {
                "feed_url": metadata.get("url", ""),
                "manifest_id": metadata.get("id", ""),
                "section": metadata.get("section", ""),
                "folder": metadata.get("folder", ""),
                "signal_type": metadata.get("signal_type", ""),
                "notification_policy": metadata.get("notification", ""),
                "profiles": [
                    profile
                    for profile, selected_ids in profile_modes.items()
                    if str(metadata.get("id", "")) in selected_ids
                ],
            }
        )
    elif url_is_web(input_feed_url):
        record["feed_url"] = input_feed_url
    return record


def assign_duplicate_groups(records: list[dict], window_days: float = 3.0) -> list[dict]:
    """Assign conservative fuzzy headline groups before the prompt sees the package."""

    parent = list(range(len(records)))

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left: int, right: int) -> None:
        left_root = find(left)
        right_root = find(right)
        if left_root != right_root:
            parent[right_root] = left_root

    def dates_are_far_apart(left: dict, right: dict) -> bool:
        left_date = parse_date(str(left.get("published", "")))
        right_date = parse_date(str(right.get("published", "")))
        return bool(
            left_date is not None
            and right_date is not None
            and abs((left_date - right_date).total_seconds()) > window_days * 86400
        )

    exact_title_index: dict[str, int] = {}
    for index, record in enumerate(records):
        normalized = normalize_title(record["title"])
        if normalized in exact_title_index:
            other_index = exact_title_index[normalized]
            if not dates_are_far_apart(record, records[other_index]):
                union(index, other_index)
        else:
            exact_title_index[normalized] = index

    token_index: dict[str, set[int]] = {}
    for index, record in enumerate(records):
        for token in set(normalize_title(record["title"]).split()):
            if len(token) >= 5:
                token_index.setdefault(token, set()).add(index)
    for index, record in enumerate(records):
        candidates: set[int] = set()
        for token in set(normalize_title(record["title"]).split()):
            if len(token) >= 5:
                candidates.update(token_index.get(token, set()))
        for other_index in candidates:
            if other_index <= index:
                continue
            if not dates_are_far_apart(record, records[other_index]) and similar_titles(
                record["title"], records[other_index]["title"]
            ):
                union(index, other_index)

    groups: dict[int, list[int]] = {}
    for index in range(len(records)):
        groups.setdefault(find(index), []).append(index)

    clusters: list[dict] = []
    for indexes in groups.values():
        if len(indexes) < 2:
            continue
        titles = sorted({normalize_title(records[index]["title"]) for index in indexes})
        representative = max((records[index]["title"] for index in indexes), key=len)
        group_id = "story-" + hashlib.sha256(normalize_title(representative).encode("utf-8")).hexdigest()[:10]
        match_type = "exact" if len(titles) == 1 else "fuzzy"
        feeds = sorted({records[index].get("feed", "") or "Unknown source" for index in indexes})
        cluster = {
            "id": group_id,
            "title": representative,
            "article_count": len(indexes),
            "feed_count": len(feeds),
            "feeds": feeds,
            "match_type": match_type,
            "title_variants": len(titles),
        }
        clusters.append(cluster)
        for index in indexes:
            records[index]["duplicate_group_id"] = group_id
            records[index]["duplicate_match_type"] = match_type

    clusters.sort(key=lambda cluster: (-cluster["article_count"], cluster["title"].casefold()))
    return clusters


def load_state(path: Path) -> dict:
    if not path.exists():
        return {"version": 2, "last_run": "", "seen": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("digest state must be a JSON object")
    version = data.get("version", 1)
    if isinstance(version, bool) or not isinstance(version, int):
        raise ValueError("digest state version must be an integer")
    data["version"] = max(2, version)
    data.setdefault("last_run", "")
    data.setdefault("seen", {})
    if not isinstance(data["seen"], dict):
        raise ValueError("digest state seen field must be an object")
    return data


def prune_seen(state: dict, max_entries: int) -> int:
    """Keep state bounded while retaining the most recently processed IDs."""

    seen = state["seen"]
    if len(seen) <= max_entries:
        return 0
    ordered = sorted(
        seen.items(),
        key=lambda pair: str(pair[1].get("processed_at", "")) if isinstance(pair[1], dict) else "",
        reverse=True,
    )
    state["seen"] = dict(ordered[:max_entries])
    return len(seen) - max_entries


def write_json(path: Path, data: dict) -> None:
    atomic_write_text(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def shortcut_text(package: dict) -> str:
    """Render a compact, link-preserving handoff for an iPhone Shortcut."""

    coverage = package.get("coverage_window", {})
    profile = package.get("profile") or "unfiltered"
    lines = [
        "Finance + Cyber Digest Input",
        f"Profile: {profile}",
        f"Articles: {package.get('article_count', 0)}",
        f"Coverage since: {coverage.get('since') or 'not specified'}",
        f"Coverage until: {coverage.get('until') or 'not specified'}",
        "",
    ]
    collection = package.get("collection")
    if isinstance(collection, dict):
        lines.insert(
            5,
            "Feed collection: "
            f"{collection.get('feeds_succeeded', 0)}/{collection.get('feeds_considered', 0)} succeeded; "
            f"{collection.get('feeds_failed', 0)} failed",
        )
        if collection.get("status") == "partial":
            lines.insert(6, "Warning: this batch is partial; check failed feed details before relying on completeness.")
    articles = package.get("articles", [])
    if not articles:
        lines.append("No material new articles were selected.")
        return "\n".join(lines) + "\n"

    for index, article in enumerate(articles, start=1):
        lines.extend(
            [
                f"{index}. {article.get('title', 'Untitled')}",
                f"Source: {article.get('feed') or 'Unknown source'}",
            ]
        )
        section = article.get("section") or article.get("folder")
        if section:
            lines.append(f"Section: {section}")
        signal = article.get("signal_type") or article.get("source_class")
        if signal:
            lines.append(f"Signal: {signal}")
        if article.get("published"):
            lines.append(f"Published: {article['published']}")
        if article.get("duplicate_group_id"):
            lines.append(f"Duplicate group: {article['duplicate_group_id']}")
        if article.get("summary"):
            lines.append(f"Summary: {article['summary']}")
        if article.get("content"):
            lines.append(f"Content: {article['content']}")
        lines.extend(
            [
                f"Link: {article.get('link', '')}",
                "",
            ]
        )
    lines.append(
        "Guardrail: keep source links beside material claims; separate confirmed facts from claims and speculation."
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="JSON array or JSON-lines export of selected NetNewsWire articles")
    parser.add_argument("--output", type=Path, help="write the prepared package here; stdout when omitted")
    parser.add_argument("--manifest", type=Path, default=Path("feed-manifest.json"))
    parser.add_argument("--state", type=Path, default=Path(".digest-state.json"))
    parser.add_argument("--since", help="optional explicit ISO-8601 lower bound; state never advances this filter implicitly")
    parser.add_argument("--profile", help="filter to a manifest profile, such as iphone-air")
    parser.add_argument("--max-items", type=int, help="override the selected profile's item budget")
    parser.add_argument("--max-item-chars", type=int, help="override the selected profile's per-item text budget")
    parser.add_argument("--max-total-chars", type=int, help="override the selected profile's total text budget")
    parser.add_argument("--max-seen-items", type=int, help="override the selected profile's seen-state budget")
    parser.add_argument("--duplicate-window-days", type=float, help="override the selected profile's duplicate window")
    parser.add_argument("--dry-run", action="store_true", help="do not update digest state")
    parser.add_argument("--prompt-file", default="docs/Apple-Intelligence-RSS-Summary-Prompt.md")
    parser.add_argument("--shortcut-output", type=Path, help="also write a compact plain-text package for an iPhone Shortcut")
    args = parser.parse_args()

    lock = file_lock(lock_path(args.state))
    lock_acquired = False
    try:
        lock.__enter__()
        lock_acquired = True
        raw_articles = load_articles(args.input)
        manifest = load_manifest(args.manifest)
        profiles = profile_settings(manifest)
        if args.profile and args.profile not in profiles:
            raise ValueError(f"unknown profile: {args.profile}")
        profile_budget = profile_digest_budget(profiles[args.profile]) if args.profile else {}
        max_items = args.max_items if args.max_items is not None else int(profile_budget.get("max_items", 100))
        max_item_chars = args.max_item_chars if args.max_item_chars is not None else int(profile_budget.get("max_item_chars", 6000))
        max_total_chars = args.max_total_chars if args.max_total_chars is not None else int(profile_budget.get("max_total_chars", 180000))
        max_seen_items = args.max_seen_items if args.max_seen_items is not None else int(profile_budget.get("max_seen_items", 10000))
        duplicate_window_days = (
            args.duplicate_window_days
            if args.duplicate_window_days is not None
            else float(profile_budget.get("duplicate_window_days", 3.0))
        )
        has_budget_override = any(
            value is not None
            for value in (
                args.max_items,
                args.max_item_chars,
                args.max_total_chars,
                args.max_seen_items,
                args.duplicate_window_days,
            )
        )
        if max_items < 1:
            raise ValueError("--max-items must be at least 1")
        if max_item_chars < 1:
            raise ValueError("--max-item-chars must be at least 1")
        if max_total_chars < 1:
            raise ValueError("--max-total-chars must be at least 1")
        if max_seen_items < 1:
            raise ValueError("--max-seen-items must be at least 1")
        if duplicate_window_days < 0:
            raise ValueError("--duplicate-window-days must not be negative")
        by_url, by_title, profile_modes = load_manifest_index(args.manifest)
        state = load_state(args.state)
        # A run can be deliberately partial because of max-items or prompt
        # budgets. Only an explicit --since is safe as a publication cursor;
        # seen IDs provide the repeat protection for normal exports.
        lower_bound = args.since or ""
        lower_date = parse_date(lower_bound) if lower_bound else None
        if lower_bound and lower_date is None:
            raise ValueError("--since must be a valid ISO-8601 date/time")
        records: dict[str, dict] = {}
        skipped_seen = 0
        skipped_old = 0
        skipped_profile = 0
        for raw_article in raw_articles:
            record = article_record(raw_article, by_url, by_title, profile_modes, max_item_chars)
            if args.profile and args.profile not in record.get("profiles", []):
                skipped_profile += 1
                continue
            if record["id"] in state["seen"]:
                skipped_seen += 1
                continue
            published_date = parse_date(record["published"]) if record["published"] else None
            if lower_date and published_date and published_date <= lower_date:
                skipped_old += 1
                continue
            records.setdefault(record["id"], record)
        selected = list(records.values())
        selected.sort(
            key=lambda record: parse_date(record["published"]) or datetime.min.replace(tzinfo=timezone.utc),
            reverse=True,
        )
        selected = selected[:max_items]
        bounded_selected: list[dict] = []
        input_characters = 0
        skipped_budget = 0
        for record in selected:
            record_characters = int(record["text_characters"])
            if input_characters + record_characters > max_total_chars:
                skipped_budget += 1
                continue
            bounded_selected.append(record)
            input_characters += record_characters
        selected = bounded_selected
        duplicate_clusters = assign_duplicate_groups(selected, duplicate_window_days)
        manifest_enriched_count = sum(
            1 for record in selected if str(record.get("source_match", "")).startswith("manifest-")
        )
        unmatched_source_count = sum(
            1
            for record in selected
            if str(record.get("source_match", "")) in {"unmatched", "unmatched-feed-url", "unmatched-feed-title"}
        )
        ambiguous_source_count = sum(
            1 for record in selected if record.get("source_match") == "ambiguous-feed-title"
        )
        now = datetime.now(ZoneInfo("Europe/Dublin"))
        package = {
            "schema_version": 2,
            "generated_at": now.isoformat(timespec="seconds"),
            "prompt_file": args.prompt_file,
            "profile": args.profile,
            "budget_source": (
                "profile+overrides"
                if profile_budget and has_budget_override
                else "profile"
                if profile_budget
                else "defaults/overrides"
            ),
            "coverage_window": {"since": lower_bound or None, "until": now.isoformat(timespec="seconds")},
            "article_count": len(selected),
            "input_characters": input_characters,
            "max_items": max_items,
            "max_item_chars": max_item_chars,
            "max_total_chars": max_total_chars,
            "max_seen_items": max_seen_items,
            "duplicate_window_days": duplicate_window_days,
            "truncated_item_count": sum(1 for record in selected if record["text_truncated"]),
            "manifest_enriched_count": manifest_enriched_count,
            "unmatched_source_count": unmatched_source_count,
            "ambiguous_source_count": ambiguous_source_count,
            "undated_count": sum(1 for record in selected if record["date_quality"] != "valid"),
            "invalid_date_count": sum(1 for record in selected if record["date_quality"] == "invalid"),
            "duplicate_cluster_count": len(duplicate_clusters),
            "duplicate_article_count": sum(cluster["article_count"] for cluster in duplicate_clusters),
            "skipped_seen_count": skipped_seen,
            "skipped_old_count": skipped_old,
            "skipped_profile_count": skipped_profile,
            "skipped_budget_count": skipped_budget,
            "pruned_seen_count": 0,
            "articles": selected,
            "duplicate_clusters": duplicate_clusters,
            "instructions": "Pass this package to the Apple Intelligence prompt. Cluster duplicate events, separate confirmed facts from claims, and end with No action recommendation.",
        }
        if not args.dry_run:
            for record in selected:
                state["seen"][record["id"]] = {
                    "title": record["title"],
                    "link": record["link"],
                    "published": record["published"],
                    "processed_at": now.isoformat(timespec="seconds"),
                }
            state["last_run"] = now.isoformat(timespec="seconds")
            package["pruned_seen_count"] = prune_seen(state, max_seen_items)
        serialized = json.dumps(package, indent=2, ensure_ascii=False) + "\n"
        if args.output:
            atomic_write_text(args.output, serialized)
        else:
            print(serialized, end="")
        if args.shortcut_output:
            atomic_write_text(args.shortcut_output, shortcut_text(package))
        if not args.dry_run:
            write_json(args.state, state)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"prepare-rss-digest-input: {exc}", file=sys.stderr)
        return 2
    finally:
        if lock_acquired:
            lock.__exit__(None, None, None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
