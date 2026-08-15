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


def article_record(article: dict) -> dict:
    title = " ".join(str(article.get("title", "")).split())
    link = str(article.get("link", "")).strip()
    if not title:
        raise ValueError("article title is empty")
    if not url_is_web(link):
        raise ValueError(f"article link is not an HTTP(S) URL: {link!r}")
    published = str(article.get("published", "")).strip()
    parsed = parse_date(published) if published else None
    return {
        "id": article_id(article),
        "title": title,
        "link": link,
        "feed": " ".join(str(article.get("feed", "")).split()),
        "published": parsed.isoformat() if parsed else published,
        "summary": " ".join(str(article.get("summary", "")).split()),
        "content": " ".join(str(article.get("content", "")).split()),
        "source_class": str(article.get("source_class", "")).strip(),
        "language": str(article.get("language", "")).strip(),
    }


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
    parser.add_argument("--state", type=Path, default=Path(".digest-state.json"))
    parser.add_argument("--since", help="optional ISO-8601 lower bound; otherwise use the last state timestamp")
    parser.add_argument("--max-items", type=int, default=100)
    parser.add_argument("--dry-run", action="store_true", help="do not update digest state")
    parser.add_argument("--prompt-file", default="Apple-Intelligence-RSS-Summary-Prompt.md")
    args = parser.parse_args()

    try:
        raw_articles = load_articles(args.input)
        state = load_state(args.state)
        lower_bound = args.since or state.get("last_run", "")
        lower_date = parse_date(lower_bound) if lower_bound else None
        records: dict[str, dict] = {}
        skipped_seen = 0
        skipped_old = 0
        for raw_article in raw_articles:
            record = article_record(raw_article)
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
        now = datetime.now(ZoneInfo("Europe/Dublin"))
        package = {
            "generated_at": now.isoformat(timespec="seconds"),
            "prompt_file": args.prompt_file,
            "coverage_window": {"since": lower_bound or None, "until": now.isoformat(timespec="seconds")},
            "article_count": len(selected),
            "skipped_seen_count": skipped_seen,
            "skipped_old_count": skipped_old,
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
