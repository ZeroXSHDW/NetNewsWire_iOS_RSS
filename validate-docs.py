#!/usr/bin/env python3
"""Validate public README links and manifest-backed feed/profile claims."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

from bundle_config import load_manifest, profile_includes_feed, profile_settings


MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)\s]+)\)")
EXTERNAL_SCHEMES = ("http://", "https://", "mailto:", "tel:")


def relative_links(text: str) -> list[tuple[int, str]]:
    """Return local Markdown link targets with their one-based line numbers."""

    links: list[tuple[int, str]] = []
    for match in MARKDOWN_LINK.finditer(text):
        target = match.group(1).strip().strip("<>")
        if not target or target.startswith(EXTERNAL_SCHEMES) or target.startswith("#"):
            continue
        target = target.split("#", 1)[0].split("?", 1)[0]
        if target:
            line = text.count("\n", 0, match.start()) + 1
            links.append((line, target))
    return links


def markdown_files(root: Path) -> list[Path]:
    """Return tracked-style Markdown files while ignoring repository metadata."""

    return sorted(
        path
        for path in root.rglob("*.md")
        if ".git" not in path.parts and "__pycache__" not in path.parts
    )


def validate_markdown_links(root: Path) -> tuple[list[str], int]:
    """Check every local Markdown link without attempting network requests."""

    errors: list[str] = []
    link_count = 0
    root_resolved = root.resolve()
    for markdown_path in markdown_files(root):
        text = markdown_path.read_text(encoding="utf-8")
        link_count += len(relative_links(text))
        display_path = markdown_path.relative_to(root)
        for line, target in relative_links(text):
            candidate = (markdown_path.parent / target).resolve()
            try:
                candidate.relative_to(root_resolved)
            except ValueError:
                errors.append(f"{display_path}:{line}: link escapes repository: {target}")
                continue
            if not candidate.exists():
                errors.append(f"{display_path}:{line}: missing local link target: {target}")
    return errors, link_count


def validate_readme(root: Path) -> list[str]:
    """Check README links and claims that are derived from the feed manifest."""

    errors: list[str] = []
    readme_path = root / "README.md"
    manifest_path = root / "feed-manifest.json"
    readme = readme_path.read_text(encoding="utf-8")
    manifest = load_manifest(manifest_path)
    feeds = manifest["feeds"]
    profiles = profile_settings(manifest)
    expected_sections = Counter(feed["section"] for feed in feeds)
    for section, count in expected_sections.items():
        marker = f"### {section} — {count} feeds"
        if marker not in readme:
            errors.append(f"README.md: missing manifest-backed section count: {marker}")

    feed_marker = f"Show all {len(feeds)} feed names"
    if feed_marker not in readme:
        errors.append(f"README.md: missing feed-directory marker: {feed_marker}")
    for feed in feeds:
        if feed["title"] not in readme:
            errors.append(f"README.md: missing feed title: {feed['title']}")

    for profile, config in profiles.items():
        selected_count = sum(
            1 for feed in feeds if profile_includes_feed(manifest, profile, feed)
        )
        marker = f"| **{config['label']}** | {selected_count} |"
        if marker not in readme:
            errors.append(
                f"README.md: profile count is missing or stale for {config['label']}: {selected_count}"
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()

    try:
        errors, link_count = validate_markdown_links(args.root)
        errors.extend(validate_readme(args.root))
    except (OSError, ValueError) as exc:
        errors = [str(exc)]
        link_count = 0

    if errors:
        for error in errors:
            print(f"ERROR {error}")
        print(f"docs-check failed errors={len(errors)}")
        return 1

    manifest = load_manifest(args.root / "feed-manifest.json")
    print(
        "docs-check passed "
        f"relative_links={link_count} "
        f"feed_names={len(manifest['feeds'])} profiles={len(profile_settings(manifest))}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
