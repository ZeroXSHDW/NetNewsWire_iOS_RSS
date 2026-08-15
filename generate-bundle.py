#!/usr/bin/env python3
"""Generate NetNewsWire OPML and source-table artifacts from one manifest."""

from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from collections import OrderedDict
from pathlib import Path

from rss_validation import url_is_web


NOTIFICATION_DISPLAY = {
    "on": "**On**",
    "optional": "Optional on",
    "optional-french": "Optional on; French",
    "off": "Off; summarize",
}


def load_manifest(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    feeds = data.get("feeds")
    if not isinstance(feeds, list) or not feeds:
        raise ValueError("manifest must contain a non-empty feeds list")

    seen_ids: set[str] = set()
    seen_urls: set[str] = set()
    for feed in feeds:
        for key in (
            "id",
            "section",
            "folder",
            "title",
            "url",
            "html_url",
            "purpose",
            "signal_type",
            "access",
            "cadence",
            "validated",
        ):
            if not str(feed.get(key, "")).strip():
                raise ValueError(f"feed is missing required field {key!r}: {feed!r}")
        feed_id = str(feed["id"])
        url = str(feed["url"])
        if feed_id in seen_ids:
            raise ValueError(f"duplicate feed id: {feed_id}")
        if url in seen_urls:
            raise ValueError(f"duplicate feed URL: {url}")
        seen_ids.add(feed_id)
        seen_urls.add(url)
        if not url_is_web(url) or not url.lower().startswith("https://"):
            raise ValueError(f"feed URL must be a direct HTTPS URL: {feed_id}")
        if not url_is_web(str(feed["html_url"])):
            raise ValueError(f"html_url must be an HTTP(S) URL: {feed_id}")
        if feed.get("notification") not in NOTIFICATION_DISPLAY:
            raise ValueError(f"invalid notification policy for {feed_id}")
        if feed.get("event_driven") and not str(feed.get("freshness_reason", "")).strip():
            raise ValueError(f"event-driven feed has no freshness_reason: {feed_id}")
        profiles = feed.get("profiles", {})
        if not isinstance(profiles, dict):
            raise ValueError(f"profiles must be an object: {feed_id}")
        if not isinstance(profiles.get("iphone-lite", False), bool):
            raise ValueError(f"iphone-lite profile must be boolean: {feed_id}")
    return data


def selected_feeds(data: dict, profile: str) -> list[dict]:
    if profile == "master":
        return list(data["feeds"])
    return [feed for feed in data["feeds"] if feed.get("profiles", {}).get(profile, False)]


def _xml_text(value: str) -> str:
    return str(value)


def write_opml(data: dict, feeds: list[dict], destination: Path, profile: str) -> None:
    root = ET.Element("opml", {"version": "2.0"})
    head = ET.SubElement(root, "head")
    ET.SubElement(head, "title").text = _xml_text(data["opml_titles"][profile])
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
                ET.SubElement(folder_outline, "outline", attributes)

    ET.indent(root, space="  ")
    tree = ET.ElementTree(root)
    destination.parent.mkdir(parents=True, exist_ok=True)
    tree.write(destination, encoding="utf-8", xml_declaration=True)


def escape_markdown(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def write_source_table(data: dict, feeds: list[dict], destination: Path, profile: str) -> None:
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
    lines.extend([
        "",
        "## Profile notes",
        "",
        data.get("profile_notes", {}).get(profile, ""),
        "",
        "## Operating references",
        "",
        "- [Setup and notification plan](NetNewsWire-Setup-and-Notification-Plan.md)",
        "- [Coverage-gap assessment](Coverage-Gap-Assessment.md)",
        "- [Apple Intelligence summary prompt](Apple-Intelligence-RSS-Summary-Prompt.md)",
        "- [Daily digest workflow](NetNewsWire-Daily-Digest-Workflow.md)",
        "",
        "## Maintenance",
        "",
        "Run `make test`, `make validate` and `make validate-lite` after manifest changes and during the monthly live health review.",
        "",
    ])
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("\n".join(lines), encoding="utf-8")


def notification_matrix_data(data: dict) -> dict:
    profiles = OrderedDict()
    for profile, label in (("master", "Master"), ("iphone-lite", "iPhone Lite")):
        feeds = selected_feeds(data, profile)
        counts = OrderedDict((policy, 0) for policy in NOTIFICATION_DISPLAY)
        for feed in feeds:
            counts[feed["notification"]] += 1
        profiles[profile] = {
            "label": label,
            "feed_count": len(feeds),
            "notification_counts": counts,
            "feed_ids": [feed["id"] for feed in feeds],
        }
    return {
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
                    "master": True,
                    "iphone-lite": bool(feed.get("profiles", {}).get("iphone-lite", False)),
                },
            }
            for feed in data["feeds"]
        ],
    }


def write_notification_matrix(data: dict, destination: Path) -> None:
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
        "| Profile | Feeds | On | Optional | Optional French | Off |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for profile, profile_data in matrix["profiles"].items():
        counts = profile_data["notification_counts"]
        lines.append(
            f"| {profile_data['label']} | {profile_data['feed_count']} | {counts['on']} | {counts['optional']} | {counts['optional-french']} | {counts['off']} |"
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
        "| Section | Folder | Feed | Master | iPhone Lite | Notification policy | Signal type |",
        "|---|---|---|---|---|---|---|",
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
                    "Yes",
                    "Yes" if feed["profiles"]["iphone-lite"] else "No",
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
        "1. Import the iPhone Lite OPML for the lower-refresh profile, or the master OPML for full coverage.",
        "2. Apply **On** only to the four urgent official alert feeds unless your operating needs justify more interruptions.",
        "3. Review **Optional** feeds after import; leave them off during normal use.",
        "4. Leave **Off** feeds notification-disabled and process them in the daily digest.",
        "5. Re-check this matrix after any manifest change; the generated OPML and source tables should be regenerated together.",
        "",
        "See [NetNewsWire setup and notification plan](NetNewsWire-Setup-and-Notification-Plan.md) for the operating rationale and [daily digest workflow](NetNewsWire-Daily-Digest-Workflow.md) for batch review.",
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
    parser.add_argument("--profile", choices=("master", "iphone-lite"), default="master")
    parser.add_argument("--opml", type=Path)
    parser.add_argument("--source-table", type=Path)
    parser.add_argument("--notification-table", type=Path)
    parser.add_argument("--notification-json", type=Path)
    args = parser.parse_args()

    try:
        data = load_manifest(args.manifest)
        feeds = selected_feeds(data, args.profile)
        if not feeds:
            raise ValueError(f"profile contains no feeds: {args.profile}")
        if args.opml:
            write_opml(data, feeds, args.opml, args.profile)
        if args.source_table:
            write_source_table(data, feeds, args.source_table, args.profile)
        if args.notification_table:
            write_notification_matrix(data, args.notification_table)
        if args.notification_json:
            write_notification_json(data, args.notification_json)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"generate-bundle: {exc}", file=sys.stderr)
        return 2

    print(f"profile={args.profile} feeds={len(feeds)} notification_matrix={'yes' if args.notification_table or args.notification_json else 'no'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
