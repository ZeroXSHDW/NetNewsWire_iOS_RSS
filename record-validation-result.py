#!/usr/bin/env python3
"""Record local validation history and surface repeated failures."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from rss_validation import feed_snapshot


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--history", required=True, type=Path)
    parser.add_argument("--profile", default="master")
    parser.add_argument("--healthy", choices=("yes", "no"), required=True)
    args = parser.parse_args()

    if args.history.exists():
        history = json.loads(args.history.read_text(encoding="utf-8"))
    else:
        history = {"version": 1, "profiles": {}}
    history["version"] = max(2, int(history.get("version", 1)))
    profile_history = history.setdefault("profiles", {}).setdefault(
        args.profile,
        {"consecutive_failures": 0, "runs": [], "feed_snapshots": {}},
    )
    profile_history.setdefault("feed_snapshots", {})
    healthy = args.healthy == "yes"
    if healthy:
        profile_history["consecutive_failures"] = 0
    else:
        profile_history["consecutive_failures"] = int(profile_history.get("consecutive_failures", 0)) + 1
    report_summary = {}
    report_data = {}
    if args.report.exists():
        try:
            report_data = json.loads(args.report.read_text(encoding="utf-8"))
            report_summary = report_data.get("summary", {})
        except json.JSONDecodeError:
            report_summary = {"report_parse_error": True}
    current_snapshots = {
        str(snapshot["url"]): snapshot
        for snapshot in (feed_snapshot(detail) for detail in report_data.get("feeds", []))
        if snapshot.get("url")
    }
    if current_snapshots:
        profile_history["feed_snapshots"] = current_snapshots
    now = datetime.now(ZoneInfo("Europe/Dublin")).isoformat(timespec="seconds")
    profile_history["runs"].append(
        {
            "at": now,
            "healthy": healthy,
            "consecutive_failures": profile_history["consecutive_failures"],
            "failed_feed_count": report_summary.get("failed_feed_count"),
            "metadata_mismatch_count": report_summary.get("metadata_mismatch_count"),
            "noisy_feed_count": report_summary.get("noisy_feed_count"),
            "regression_warning_count": report_summary.get("regression_warning_count"),
            "regression_critical_count": report_summary.get("regression_critical_count"),
        }
    )
    profile_history["runs"] = profile_history["runs"][-20:]
    args.history.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.history.with_name(f".{args.history.name}.tmp")
    temporary.write_text(json.dumps(history, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(args.history)
    consecutive = profile_history["consecutive_failures"]
    alert = "yes" if consecutive >= 3 else "no"
    print(
        f"profile={args.profile} healthy={args.healthy} consecutive_failures={consecutive} "
        f"regression_warnings={report_summary.get('regression_warning_count', 0)} "
        f"alert_after_three={alert}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
