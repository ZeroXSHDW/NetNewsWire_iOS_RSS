#!/usr/bin/env python3
"""Prepare a deduplicated, stateful input package for the daily RSS digest."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from rss_validation import normalize_link, normalize_title, parse_date, url_is_web


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
    identity = link or "|".join((title, published))
    if not identity:
        raise ValueError("article needs a link or title/published identity")
    return hashlib.sha256(identity.encode("utf-8")).hexdigest()[:20]


def load_manifest_index(path: Path) -> tuple[dict[str, dict], dict[str, list[dict]]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    feeds = data.get("feeds")
    if not isinstance(feeds, list):
        raise ValueError("feed manifest must contain a feeds array")
    by_url: dict[str, dict] = {}
    by_title: dict[str, list[dict]] = {}
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
    return by_url, by_title


def resolve_manifest_feed(article: dict, by_url: dict[str, dict], by_title: dict[str, list[dict]]) -> dict | None:
    explicit_feed_url = str(article.get("feed_url", article.get("feedUrl", ""))).strip()
    if explicit_feed_url:
        metadata = by_url.get(explicit_feed_url) or by_url.get(normalize_link(explicit_feed_url))
        if metadata:
            return metadata
    feed_title = normalize_title(str(article.get("feed", "")))
    matches = by_title.get(feed_title, []) if feed_title else []
    return matches[0] if len(matches) == 1 else None


def clean_text(value: object) -> str:
    return " ".join(str(value or "").split())


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
    metadata = resolve_manifest_feed(article, by_url, by_title)
    summary, content, text_truncated = bounded_text_fields(article, max_item_chars)
    record = {
        "id": article_id(article),
        "title": title,
        "link": link,
        "feed": str(metadata.get("title", "")) if metadata else clean_text(article.get("feed", "")),
        "published": parsed.isoformat() if parsed else published,
        "summary": summary,
        "content": content,
        "source_class": str(article.get("source_class", "")).strip() or (str(metadata.get("signal_type", "")) if metadata else ""),
        "language": clean_text(article.get("language", "")),
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
                    for profile in ("master", "iphone-lite")
                    if profile == "master" or metadata.get("profiles", {}).get(profile, False)
                ],
            }
        )
    return record


def load_state(path: Path) -> dict:
    if not path.exists():
        return {"version": 1, "last_run": "", "seen": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("digest state must be a JSON object")
    data.setdefault("version", 1)
    data.setdefault("last_run", "")
    data.setdefault("seen", {})
    if not isinstance(data["seen"], dict):
        raise ValueError("digest state seen field must be an object")
    return data


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="JSON array or JSON-lines export of selected NetNewsWire articles")
    parser.add_argument("--output", type=Path, help="write the prepared package here; stdout when omitted")
    parser.add_argument("--manifest", type=Path, default=Path("feed-manifest.json"))
    parser.add_argument("--state", type=Path, default=Path(".digest-state.json"))
    parser.add_argument("--since", help="optional ISO-8601 lower bound; otherwise use the last state timestamp")
    parser.add_argument("--max-items", type=int, default=100)
    parser.add_argument("--max-item-chars", type=int, default=6000)
    parser.add_argument("--max-total-chars", type=int, default=180000)
    parser.add_argument("--dry-run", action="store_true", help="do not update digest state")
    parser.add_argument("--prompt-file", default="Apple-Intelligence-RSS-Summary-Prompt.md")
    args = parser.parse_args()

    try:
        raw_articles = load_articles(args.input)
        if args.max_item_chars < 1:
            raise ValueError("--max-item-chars must be at least 1")
        if args.max_total_chars < 0:
            raise ValueError("--max-total-chars must not be negative")
        by_url, by_title = load_manifest_index(args.manifest)
        state = load_state(args.state)
        lower_bound = args.since or state.get("last_run", "")
        lower_date = parse_date(lower_bound) if lower_bound else None
        records: dict[str, dict] = {}
        skipped_seen = 0
        skipped_old = 0
        for raw_article in raw_articles:
            record = article_record(raw_article, by_url, by_title, args.max_item_chars)
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
        selected = selected[: max(0, args.max_items)]
        bounded_selected: list[dict] = []
        input_characters = 0
        skipped_budget = 0
        for record in selected:
            record_characters = int(record["text_characters"])
            if input_characters + record_characters > args.max_total_chars:
                skipped_budget += 1
                continue
            bounded_selected.append(record)
            input_characters += record_characters
        selected = bounded_selected
        now = datetime.now(ZoneInfo("Europe/Dublin"))
        package = {
            "generated_at": now.isoformat(timespec="seconds"),
            "prompt_file": args.prompt_file,
            "coverage_window": {"since": lower_bound or None, "until": now.isoformat(timespec="seconds")},
            "article_count": len(selected),
            "input_characters": input_characters,
            "max_item_chars": args.max_item_chars,
            "max_total_chars": args.max_total_chars,
            "truncated_item_count": sum(1 for record in selected if record["text_truncated"]),
            "skipped_seen_count": skipped_seen,
            "skipped_old_count": skipped_old,
            "skipped_budget_count": skipped_budget,
            "articles": selected,
            "instructions": "Pass this package to the Apple Intelligence prompt. Cluster duplicate events, separate confirmed facts from claims, and end with No action recommendation.",
        }
        serialized = json.dumps(package, indent=2, ensure_ascii=False) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            temporary = args.output.with_name(f".{args.output.name}.tmp")
            temporary.write_text(serialized, encoding="utf-8")
            temporary.replace(args.output)
        else:
            print(serialized, end="")
        if not args.dry_run:
            for record in selected:
                state["seen"][record["id"]] = {
                    "title": record["title"],
                    "link": record["link"],
                    "published": record["published"],
                    "processed_at": now.isoformat(timespec="seconds"),
                }
            state["last_run"] = now.isoformat(timespec="seconds")
            write_json(args.state, state)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"prepare-rss-digest-input: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
