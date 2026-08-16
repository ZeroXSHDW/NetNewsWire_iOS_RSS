#!/usr/bin/env python3
"""Generate NetNewsWire OPML and source-table artifacts from one manifest."""

from __future__ import annotations

import argparse
import json
import os
import sys
import xml.etree.ElementTree as ET
from collections import OrderedDict
from pathlib import Path

from bundle_config import (
    NOTIFICATION_DISPLAY,
    item_link_policy,
    load_manifest as load_manifest_file,
    profile_device_budget,
    profile_includes_feed,
    profile_config,
    profile_settings,
)


def load_manifest(path: Path) -> dict:
    return load_manifest_file(path)


def selected_feeds(data: dict, profile: str) -> list[dict]:
    profile_config(data, profile)
    return [feed for feed in data["feeds"] if profile_includes_feed(data, profile, feed)]


def _xml_text(value: str) -> str:
    return str(value)


def write_opml(data: dict, feeds: list[dict], destination: Path, profile: str) -> None:
    root = ET.Element("opml", {"version": "2.0"})
    head = ET.SubElement(root, "head")
    ET.SubElement(head, "title").text = _xml_text(profile_config(data, profile)["opml_title"])
    body = ET.SubElement(root, "body")

    sections: OrderedDict[str, OrderedDict[str, list[dict]]] = OrderedDict()
    for feed in feeds:
        sections.setdefault(feed["section"], OrderedDict()).setdefault(feed["folder"], []).append(feed)

    for section, folders in sections.items():
        section_outline = ET.SubElement(body, "outline", {"text": section, "title": section})
        for folder, folder_feeds in folders.items():
            folder_outline = ET.SubElement(
                section_outline,
                "outline",
                {"text": folder, "title": folder},
            )
            for feed in folder_feeds:
                attributes = {
                    "type": "rss",
                    "text": feed["title"],
                    "title": feed["title"],
                    "xmlUrl": feed["url"],
                    "htmlUrl": feed["html_url"],
                }
                if feed.get("event_driven"):
                    attributes["eventDriven"] = "true"
                policy = item_link_policy(feed)
                if policy != "default":
                    attributes["itemLinkPolicy"] = policy
                ET.SubElement(folder_outline, "outline", attributes)

    ET.indent(root, space="  ")
    tree = ET.ElementTree(root)
    destination.parent.mkdir(parents=True, exist_ok=True)
    tree.write(destination, encoding="utf-8", xml_declaration=True)


def escape_markdown(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def _reference_link(repository_root: Path, link_directory: Path, target: str) -> str:
    """Return a Markdown link from an artifact directory to a repository file."""

    absolute_target = (repository_root / target).resolve()
    return Path(os.path.relpath(absolute_target, link_directory.resolve())).as_posix()


def _operating_reference_links(repository_root: Path, link_directory: Path) -> dict[str, str]:
    targets = {
        "setup": "docs/NetNewsWire-Setup-and-Notification-Plan.md",
        "coverage": "docs/Coverage-Gap-Assessment.md",
        "apple": "docs/Apple-Intelligence-RSS-Summary-Prompt.md",
        "digest": "docs/NetNewsWire-Daily-Digest-Workflow.md",
        "matrix": "docs/NetNewsWire-Feature-and-Automation-Matrix.md",
    }
    return {
        name: _reference_link(repository_root, link_directory, target)
        for name, target in targets.items()
    }


def write_source_table(
    data: dict,
    feeds: list[dict],
    destination: Path,
    profile: str,
    *,
    repository_root: Path = Path("."),
    link_directory: Path | None = None,
) -> None:
    lines = [
        "# NetNewsWire Finance + Cyber source table",
        "",
        f"Generated from `feed-manifest.json` for the **{profile}** profile.",
        "",
    ]
    current_section = None
    for feed in feeds:
        if feed["section"] != current_section:
            current_section = feed["section"]
            lines.extend([
                f"## {current_section}",
                "",
                "| Folder | Feed | URL | Purpose / class / focus | Signal type | Paywall / registration | Reliability / cadence | Notifications | Validated |",
                "|---|---|---|---|---|---|---|---|---|",
            ])
        lines.append(
            "| "
            + " | ".join(
                escape_markdown(value)
                for value in (
                    feed["folder"],
                    feed["title"],
                    feed["url"],
                    feed["purpose"],
                    feed["signal_type"],
                    feed["access"],
                    feed["cadence"],
                    NOTIFICATION_DISPLAY[feed["notification"]],
                    feed["validated"],
                )
            )
            + " |"
        )
    links = _operating_reference_links(
        repository_root,
        link_directory or destination.parent,
    )
    lines.extend([
        "",
        "## Profile notes",
        "",
        profile_config(data, profile).get("note", ""),
        "",
        "## Operating references",
        "",
        f"- [Setup and notification plan]({links['setup']})",
        f"- [Coverage-gap assessment]({links['coverage']})",
        f"- [Apple Intelligence summary prompt]({links['apple']})",
        f"- [Daily digest workflow]({links['digest']})",
        f"- [Feature and automation matrix]({links['matrix']})",
        "",
        "## Maintenance",
        "",
        "Run `make check`, `make validate`, `make validate-lite` and `make validate-air` after manifest changes and during the monthly live health review.",
        "",
    ])
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("\n".join(lines), encoding="utf-8")


def notification_matrix_data(data: dict) -> dict:
    profiles = OrderedDict()
    manifest_profiles = profile_settings(data)
    for profile, config in manifest_profiles.items():
        feeds = selected_feeds(data, profile)
        counts = OrderedDict((policy, 0) for policy in NOTIFICATION_DISPLAY)
        for feed in feeds:
            counts[feed["notification"]] += 1
        profiles[profile] = {
            "label": config["label"],
            "feed_count": len(feeds),
            "recommended": bool(config.get("recommended", False)),
            "device_budget": profile_device_budget(config),
            "notification_counts": counts,
            "feed_ids": [feed["id"] for feed in feeds],
        }
    return {
        "schema_version": 2,
        "manifest_version": data.get("manifest_version"),
        "profiles": profiles,
        "feeds": [
            {
                "id": feed["id"],
                "section": feed["section"],
                "folder": feed["folder"],
                "title": feed["title"],
                "url": feed["url"],
                "notification": feed["notification"],
                "notification_display": NOTIFICATION_DISPLAY[feed["notification"]],
                "signal_type": feed["signal_type"],
                "profiles": {
                    profile: profile_includes_feed(data, profile, feed)
                    for profile in manifest_profiles
                },
            }
            for feed in data["feeds"]
        ],
    }


def write_notification_matrix(
    data: dict,
    destination: Path,
    *,
    repository_root: Path = Path("."),
    link_directory: Path | None = None,
) -> None:
    matrix = notification_matrix_data(data)
    lines = [
        "# NetNewsWire notification and profile matrix",
        "",
        "Generated from `feed-manifest.json`; regenerate with `make generate` after manifest changes.",
        "",
        "OPML imports carry the feed structure but do not reliably carry NetNewsWire notification settings. Apply the policy below manually after import.",
        "",
        "## Profile summary",
        "",
        "| Profile | Recommended | Feeds | On | Optional | Optional French | Off |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for profile, profile_data in matrix["profiles"].items():
        counts = profile_data["notification_counts"]
        lines.append(
            f"| {profile_data['label']} | {'Yes' if profile_data['recommended'] else 'No'} | {profile_data['feed_count']} | {counts['on']} | {counts['optional']} | {counts['optional-french']} | {counts['off']} |"
        )

    profile_names = list(matrix["profiles"])
    profile_headers = [matrix["profiles"][profile]["label"] for profile in profile_names]
    recommended_profile = next(
        (matrix["profiles"][profile]["label"] for profile in profile_names if matrix["profiles"][profile]["recommended"]),
        profile_headers[-1],
    )
    full_profile = next(
        (matrix["profiles"][profile]["label"] for profile in profile_names if profile_settings(data)[profile]["include_all"]),
        profile_headers[0],
    )
    links = _operating_reference_links(
        repository_root,
        link_directory or destination.parent,
    )
    lines.extend([
        "",
        "## Policy meanings",
        "",
        "| Policy | Meaning |",
        "|---|---|",
        "| On | Enable immediate notifications for urgent, high-signal alerts. |",
        "| Optional | Keep off by default; enable when the topic is actively relevant. |",
        "| Optional French | Same as Optional; translate/summarize in the daily digest when useful. |",
        "| Off | Do not interrupt; include in the daily Apple Intelligence digest. |",
        "",
        "## Per-feed matrix",
        "",
        "| Section | Folder | Feed | " + " | ".join(profile_headers) + " | Notification policy | Signal type |",
        "|---|---|---|" + "---|" * len(profile_headers) + "---|---|",
    ])
    for feed in matrix["feeds"]:
        lines.append(
            "| "
            + " | ".join(
                escape_markdown(value)
                for value in (
                    feed["section"],
                    feed["folder"],
                    feed["title"],
                    *["Yes" if feed["profiles"].get(profile, False) else "No" for profile in profile_names],
                    feed["notification_display"],
                    feed["signal_type"],
                )
            )
            + " |"
        )

    lines.extend([
        "",
        "## Import checklist",
        "",
        f"1. Import exactly one profile: the **{recommended_profile}** OPML as the default, the Lite OPML for constrained connections, or the **{full_profile}** OPML for full coverage.",
        "2. NetNewsWire adds imported feeds to the current subscription list; remove or separate an older copy before importing if you are replacing a previous bundle.",
        "3. Apply **On** only to the four urgent official alert feeds unless your operating needs justify more interruptions.",
        "4. Review **Optional** feeds after import; leave them off during normal use.",
        "5. Leave **Off** feeds notification-disabled and process them in the daily digest.",
        "6. Re-check this matrix after any manifest change; the generated OPML and source tables should be regenerated together.",
        "",
        f"See [NetNewsWire setup and notification plan]({links['setup']}) for the operating rationale and [daily digest workflow]({links['digest']}) for batch review.",
        "",
    ])
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("\n".join(lines), encoding="utf-8")


def write_notification_json(data: dict, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(notification_matrix_data(data), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default="feed-manifest.json", type=Path)
    parser.add_argument("--profile", default="master")
    parser.add_argument("--all", dest="all_profiles", action="store_true", help="generate every manifest-defined profile")
    parser.add_argument("--output-root", type=Path, default=Path("."))
    parser.add_argument("--opml", type=Path)
    parser.add_argument("--source-table", type=Path)
    parser.add_argument("--notification-table", type=Path)
    parser.add_argument("--notification-json", type=Path)
    args = parser.parse_args()

    try:
        data = load_manifest(args.manifest)
        if args.all_profiles and (args.opml or args.source_table):
            raise ValueError("--all cannot be combined with --opml or --source-table")
        if args.all_profiles:
            generated_profiles = []
            for profile, config in profile_settings(data).items():
                feeds = selected_feeds(data, profile)
                if not feeds:
                    raise ValueError(f"profile contains no feeds: {profile}")
                write_opml(data, feeds, args.output_root / config["opml_file"], profile)
                source_table_path = args.output_root / config["source_table_file"]
                write_source_table(
                    data,
                    feeds,
                    source_table_path,
                    profile,
                    repository_root=args.manifest.parent,
                )
                generated_profiles.append(f"{profile}={len(feeds)}")
        else:
            feeds = selected_feeds(data, args.profile)
            if not feeds:
                raise ValueError(f"profile contains no feeds: {args.profile}")
            if args.opml:
                write_opml(data, feeds, args.opml, args.profile)
            if args.source_table:
                write_source_table(
                    data,
                    feeds,
                    args.source_table,
                    args.profile,
                    repository_root=args.manifest.parent,
                )
            generated_profiles = [f"{args.profile}={len(feeds)}"]
        if args.notification_table:
            write_notification_matrix(
                data,
                args.notification_table,
                repository_root=args.manifest.parent,
            )
        if args.notification_json:
            write_notification_json(data, args.notification_json)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"generate-bundle: {exc}", file=sys.stderr)
        return 2

    print(f"profiles={' '.join(generated_profiles)} notification_matrix={'yes' if args.notification_table or args.notification_json else 'no'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
