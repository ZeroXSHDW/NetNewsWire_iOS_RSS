#!/usr/bin/env python3
"""Print a compact, read-only health snapshot for the RSS project."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from bundle_config import load_manifest, profile_includes_feed, profile_settings


DISPLAY_PROFILE_ORDER = ("master", "iphone-air", "iphone-lite")
REPORT_ROOT = Path("artifacts/validation")


def _format_bytes(value: object) -> str:
    """Format a byte count without requiring a third-party package."""

    try:
        number = float(value)
    except (TypeError, ValueError):
        return "unknown"
    if number < 1024:
        return f"{number:.0f} B"
    for unit in ("KiB", "MiB", "GiB"):
        number /= 1024
        if number < 1024 or unit == "GiB":
            return f"{number:.2f} {unit}"
    return "unknown"


def _profile_order(profiles: dict[str, dict]) -> list[str]:
    preferred = [name for name in DISPLAY_PROFILE_ORDER if name in profiles]
    return preferred + [name for name in profiles if name not in preferred]


def _report_path(root: Path, config: dict) -> Path:
    opml_name = Path(config["opml_file"]).name
    return root / REPORT_ROOT / f"{Path(opml_name).stem}-VALIDATION-REPORT.json"


def _load_report(path: Path) -> tuple[dict | None, str | None]:
    if not path.is_file():
        return None, "missing"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, f"unreadable: {exc}"
    if not isinstance(data, dict):
        return None, "root is not an object"
    return data, None


def _local_timestamp(value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        return "unknown"
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return value
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(ZoneInfo("Europe/Dublin")).strftime("%Y-%m-%d %H:%M %Z")


def _report_summary(report: dict, expected_count: int, path: Path, root: Path) -> dict:
    summary = report.get("summary")
    if not isinstance(summary, dict):
        summary = {}
    feeds = report.get("feeds")
    if not isinstance(feeds, list):
        feeds = []
    failed_feeds = report.get("failed_feeds")
    if not isinstance(failed_feeds, list):
        failed_feeds = []
    attention_feeds = report.get("attention_feeds")
    if not isinstance(attention_feeds, list):
        attention_feeds = []
    warnings = report.get("regression_warnings")
    if not isinstance(warnings, list):
        warnings = []
    budget_failures = report.get("device_budget_failures")
    if not isinstance(budget_failures, list):
        budget_failures = []

    failed_count = int(summary.get("failed_feed_count", len(failed_feeds)) or 0)
    feed_count = int(summary.get("feed_count", len(feeds)) or 0)
    passed_count = sum(
        1 for feed in feeds if isinstance(feed, dict) and feed.get("passed") == "yes"
    )
    critical_warnings = sum(
        1
        for warning in warnings
        if isinstance(warning, dict) and warning.get("severity") == "critical"
    )
    actual_failures = [
        feed
        for feed in failed_feeds
        if isinstance(feed, dict) and feed.get("passed") == "no"
    ]
    # Reports before schema version 2 did not always include the per-feed
    # passed flag. Preserve useful names for those snapshots, but never mix
    # passed attention entries (for example tolerated future-date items) into
    # the actual failure list when the flag is available.
    if not actual_failures and failed_count and failed_feeds and not any(
        isinstance(feed, dict) and "passed" in feed for feed in failed_feeds
    ):
        actual_failures = failed_feeds[:failed_count]

    failure_names = []
    for feed in actual_failures:
        if not isinstance(feed, dict):
            continue
        label = feed.get("feed_title") or feed.get("manifest_id") or feed.get("url")
        if isinstance(label, str) and label.strip():
            failure_names.append(" ".join(label.split()))

    attention_keys = set()
    for feed in [*failed_feeds, *attention_feeds]:
        if not isinstance(feed, dict):
            continue
        key = feed.get("url") or feed.get("manifest_id") or feed.get("feed_title")
        if isinstance(key, str) and key.strip():
            attention_keys.add(key.strip())

    return {
        "path": path.relative_to(root).as_posix(),
        "profile": report.get("profile"),
        "feed_count": feed_count,
        "expected_count": expected_count,
        "passed_count": passed_count,
        "failed_count": failed_count,
        "attention_count": len(attention_keys),
        "warning_count": len(warnings),
        "critical_warning_count": critical_warnings,
        "device_budget_failure_count": len(budget_failures),
        "payload_bytes_total": summary.get("payload_bytes_total"),
        "wire_bytes_total": summary.get("wire_bytes_total"),
        "generated_at": report.get("generated_at"),
        "generated_at_local": _local_timestamp(report.get("generated_at")),
        "failure_names": failure_names,
    }


def build_status(root: Path) -> dict:
    """Build a JSON-serializable status object without changing repository files."""

    manifest = load_manifest(root / "feed-manifest.json")
    profiles = profile_settings(manifest)
    feeds = manifest["feeds"]
    section_counts = dict(sorted(Counter(feed["section"] for feed in feeds).items()))

    profile_status: dict[str, dict] = {}
    for profile in _profile_order(profiles):
        config = profiles[profile]
        profile_status[profile] = {
            "label": config["label"],
            "feed_count": sum(
                1 for feed in feeds if profile_includes_feed(manifest, profile, feed)
            ),
            "opml_file": config["opml_file"],
            "source_table_file": config["source_table_file"],
        }

    artifact_paths: list[Path] = []
    for config in profiles.values():
        artifact_paths.extend(
            [root / config["opml_file"], root / config["source_table_file"]]
        )
    artifact_paths.extend(
        [
            root / "artifacts/notifications/NetNewsWire-Notification-Profile.md",
            root / "artifacts/notifications/NetNewsWire-Notification-Profile.json",
            root / "artifacts/AirDrop/README.txt",
            root / "artifacts/AirDrop/NetNewsWire-Finance-Cyber-iPhone-Air.opml",
        ]
    )
    missing_artifacts = [
        path.relative_to(root).as_posix() for path in artifact_paths if not path.is_file()
    ]

    validation: dict[str, dict] = {}
    findings: list[str] = []
    for profile in _profile_order(profiles):
        path = _report_path(root, profiles[profile])
        report, error = _load_report(path)
        if error:
            validation[profile] = {
                "path": path.relative_to(root).as_posix(),
                "error": error,
                "expected_count": profile_status[profile]["feed_count"],
            }
            findings.append(f"{profile}: validation snapshot {error} ({path.name})")
            continue

        details = _report_summary(
            report,
            profile_status[profile]["feed_count"],
            path,
            root,
        )
        validation[profile] = details
        if details["feed_count"] != details["expected_count"]:
            findings.append(
                f"{profile}: validation snapshot covers {details['feed_count']} feeds; "
                f"current profile contains {details['expected_count']}"
            )
        if details["failed_count"]:
            labels = ", ".join(details["failure_names"][:3]) or "unnamed feed"
            suffix = "" if len(details["failure_names"]) <= 3 else ", …"
            findings.append(f"{profile}: {details['failed_count']} failed feed(s): {labels}{suffix}")
        if details["critical_warning_count"]:
            findings.append(
                f"{profile}: {details['critical_warning_count']} critical drift warning(s)"
            )
        if details["device_budget_failure_count"]:
            findings.append(
                f"{profile}: {details['device_budget_failure_count']} device-budget failure(s)"
            )

    if missing_artifacts:
        findings.insert(0, f"missing generated artifacts: {', '.join(missing_artifacts)}")

    return {
        "status": "attention" if findings else "ready",
        "manifest": {
            "feed_count": len(feeds),
            "section_counts": section_counts,
            "profile_count": len(profiles),
        },
        "profiles": profile_status,
        "artifacts": {
            "expected_count": len(artifact_paths),
            "present_count": len(artifact_paths) - len(missing_artifacts),
            "missing": missing_artifacts,
        },
        "validation": validation,
        "findings": findings,
    }


def render_text(status: dict) -> str:
    """Render the status object as concise maintainer-facing text."""

    manifest = status["manifest"]
    sections = manifest["section_counts"]
    lines = [
        f"Project status: {status['status']}",
        f"manifest: {manifest['feed_count']} feeds "
        f"({sections.get('Finance', 0)} Finance, {sections.get('Cyber Security', 0)} Cyber Security)",
    ]
    profile_parts = [
        f"{profile}={details['feed_count']}"
        for profile, details in status["profiles"].items()
    ]
    lines.append(f"profiles: {', '.join(profile_parts)}")
    artifacts = status["artifacts"]
    lines.append(
        f"artifacts: {artifacts['present_count']}/{artifacts['expected_count']} present"
    )
    lines.append("validation snapshots:")
    for profile, details in status["validation"].items():
        if "error" in details:
            lines.append(f"  {profile}: {details['error']}")
            continue
        lines.append(
            f"  {profile}: {details['passed_count']}/{details['feed_count']} passed, "
            f"failed={details['failed_count']}, warnings={details['warning_count']} "
            f"(critical={details['critical_warning_count']}), "
            f"generated={details['generated_at_local']}"
        )
        if details.get("payload_bytes_total") is not None:
            lines.append(
                f"    payload={_format_bytes(details['payload_bytes_total'])}, "
                f"wire={_format_bytes(details.get('wire_bytes_total'))}"
            )
    if status["findings"]:
        lines.append("findings:")
        lines.extend(f"  - {finding}" for finding in status["findings"])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit the machine-readable status object instead of text",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="return non-zero when the snapshot contains findings",
    )
    args = parser.parse_args()
    try:
        status = build_status(args.root.resolve())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"project-status failed: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(status, indent=2, sort_keys=True))
    else:
        print(render_text(status))
    return 1 if args.strict and status["findings"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
