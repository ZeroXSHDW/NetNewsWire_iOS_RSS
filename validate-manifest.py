#!/usr/bin/env python3
"""Validate the feed manifest and prove generated artifacts are reproducible."""

from __future__ import annotations

import argparse
import importlib.util
import json
import tempfile
from datetime import date
from pathlib import Path

from rss_validation import normalize_link, url_is_web


def load_generator_module():
    path = Path(__file__).with_name("generate-bundle.py")
    spec = importlib.util.spec_from_file_location("generate_bundle", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load generator module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_manifest(data: dict, errors: list[str], generator) -> None:
    if not isinstance(data.get("manifest_version"), int) or data["manifest_version"] < 1:
        errors.append("manifest_version must be a positive integer")

    for profile in ("master", "iphone-lite"):
        if not str(data.get("opml_titles", {}).get(profile, "")).strip():
            errors.append(f"opml_titles is missing {profile}")
        if not str(data.get("profile_notes", {}).get(profile, "")).strip():
            errors.append(f"profile_notes is missing {profile}")

    validation = data.get("validation")
    if not isinstance(validation, dict):
        errors.append("validation must be an object")
    else:
        positive_fields = (
            "max_age_days",
            "min_items_for_noise",
            "stale_review_default_days",
            "mobile_review_bytes",
            "mobile_large_bytes",
            "mobile_slow_seconds",
        )
        for key in positive_fields:
            value = validation.get(key)
            if not isinstance(value, (int, float)) or value <= 0:
                errors.append(f"validation.{key} must be positive")
        duplicate_limit = validation.get("duplicate_title_rate_limit")
        if not isinstance(duplicate_limit, (int, float)) or not 0 <= duplicate_limit <= 1:
            errors.append("validation.duplicate_title_rate_limit must be between 0 and 1")

    feeds = data.get("feeds")
    if not isinstance(feeds, list) or not feeds:
        errors.append("feeds must be a non-empty array")
        return

    seen_ids: set[str] = set()
    seen_urls: set[str] = set()
    seen_canonical_urls: set[str] = set()
    for index, feed in enumerate(feeds, start=1):
        if not isinstance(feed, dict):
            errors.append(f"feed {index} is not an object")
            continue
        feed_id = str(feed.get("id", ""))
        feed_url = str(feed.get("url", ""))
        label = feed_id or f"feed {index}"
        if feed_id in seen_ids:
            errors.append(f"duplicate feed id: {feed_id}")
        seen_ids.add(feed_id)
        if feed_url in seen_urls:
            errors.append(f"duplicate feed URL: {feed_url}")
        seen_urls.add(feed_url)
        canonical_url = normalize_link(feed_url)
        if canonical_url and canonical_url in seen_canonical_urls:
            errors.append(f"duplicate canonical feed URL: {feed_url}")
        if canonical_url:
            seen_canonical_urls.add(canonical_url)
        if not url_is_web(feed_url) or not feed_url.lower().startswith("https://"):
            errors.append(f"{label}: feed URL must be HTTPS")
        if not url_is_web(str(feed.get("html_url", ""))):
            errors.append(f"{label}: html_url must be HTTP(S)")
        if not isinstance(feed.get("event_driven"), bool):
            errors.append(f"{label}: event_driven must be boolean")
        if feed.get("event_driven"):
            if not str(feed.get("freshness_reason", "")).strip():
                errors.append(f"{label}: event-driven feed needs freshness_reason")
            stale_days = feed.get("stale_review_days")
            if not isinstance(stale_days, (int, float)) or stale_days <= 0:
                errors.append(f"{label}: event-driven feed needs positive stale_review_days")
        validated = str(feed.get("validated", ""))
        try:
            date.fromisoformat(validated)
        except ValueError:
            errors.append(f"{label}: validated must be YYYY-MM-DD")
        profiles = feed.get("profiles", {})
        if not isinstance(profiles, dict):
            errors.append(f"{label}: profiles must be an object")
        else:
            for profile, enabled in profiles.items():
                if not isinstance(profile, str) or not isinstance(enabled, bool):
                    errors.append(f"{label}: profile flags must be string/boolean pairs")

    master_urls = {str(feed.get("url", "")) for feed in generator.selected_feeds(data, "master")}
    lite_urls = {str(feed.get("url", "")) for feed in generator.selected_feeds(data, "iphone-lite")}
    if not lite_urls:
        errors.append("iphone-lite profile contains no feeds")
    if not lite_urls <= master_urls:
        errors.append("iphone-lite contains a feed outside the master profile")


def compare_generated_artifacts(data: dict, root: Path, errors: list[str], generator) -> None:
    artifacts = (
        (
            "master",
            root / "NetNewsWire-Finance-Cyber.opml",
            root / "NetNewsWire-Finance-Cyber-Source-Table.md",
        ),
        (
            "iphone-lite",
            root / "NetNewsWire-Finance-Cyber-iPhone-Lite.opml",
            root / "NetNewsWire-Finance-Cyber-iPhone-Lite-Source-Table.md",
        ),
    )
    with tempfile.TemporaryDirectory(prefix="nnw-manifest-lint-") as temporary:
        temporary_root = Path(temporary)
        for profile, committed_opml, committed_table in artifacts:
            feeds = generator.selected_feeds(data, profile)
            generated_opml = temporary_root / f"{profile}.opml"
            generated_table = temporary_root / f"{profile}.md"
            generator.write_opml(data, feeds, generated_opml, profile)
            generator.write_source_table(data, feeds, generated_table, profile)
            for generated, committed in ((generated_opml, committed_opml), (generated_table, committed_table)):
                if not committed.exists():
                    errors.append(f"missing generated artifact: {committed.name}")
                elif generated.read_bytes() != committed.read_bytes():
                    errors.append(f"generated artifact is stale: {committed.name}")

        generated_matrix_md = temporary_root / "notifications.md"
        generated_matrix_json = temporary_root / "notifications.json"
        generator.write_notification_matrix(data, generated_matrix_md)
        generator.write_notification_json(data, generated_matrix_json)
        for generated, committed in (
            (generated_matrix_md, root / "NetNewsWire-Notification-Profile.md"),
            (generated_matrix_json, root / "NetNewsWire-Notification-Profile.json"),
        ):
            if not committed.exists():
                errors.append(f"missing generated artifact: {committed.name}")
            elif generated.read_bytes() != committed.read_bytes():
                errors.append(f"generated artifact is stale: {committed.name}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path("feed-manifest.json"))
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()

    errors: list[str] = []
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("manifest root must be an object")
        generator = load_generator_module()
        try:
            generator.load_manifest(args.manifest)
        except ValueError as exc:
            errors.append(str(exc))
        check_manifest(data, errors, generator)
        if not errors:
            compare_generated_artifacts(data, args.root, errors, generator)
    except (OSError, ValueError, json.JSONDecodeError, RuntimeError) as exc:
        errors.append(str(exc))

    if errors:
        for error in errors:
            print(f"ERROR {error}")
        print(f"manifest-lint failed errors={len(errors)}")
        return 1
    feeds = len(data.get("feeds", []))
    lite = len(generator.selected_feeds(data, "iphone-lite"))
    print(f"manifest-lint passed feeds={feeds} iphone-lite={lite} generated-artifacts=verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
