#!/usr/bin/env python3
"""Record local validation history and surface repeated failures."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from rss_validation import feed_snapshot
from state_utils import atomic_write_text, file_lock, lock_path


def parse_report_time(value: object) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("report is missing generated_at")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("report generated_at is not ISO-8601") from exc
    if parsed.tzinfo is None:
        raise ValueError("report generated_at must include a timezone")
    return parsed.astimezone(timezone.utc)


def load_report(path: Path, profile: str, current_run: bool, max_age_seconds: float) -> dict:
    if not path.exists():
        raise ValueError(f"report does not exist: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read validation report: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("validation report must be a JSON object")
    if current_run:
        schema_version = data.get("schema_version", 0)
        if isinstance(schema_version, bool) or not isinstance(schema_version, int) or schema_version < 2:
            raise ValueError("current validation report must have schema_version >= 2")
        if data.get("profile") != profile:
            raise ValueError("validation report profile does not match requested profile")
        generated_at = parse_report_time(data.get("generated_at"))
        age = (datetime.now(timezone.utc) - generated_at).total_seconds()
        if age < -60 or age > max_age_seconds:
            raise ValueError("validation report is outside the current-run time window")
        if not isinstance(data.get("feeds"), list) or not data["feeds"]:
            raise ValueError("current validation report has no feed details")
    return data


def record_history(args: argparse.Namespace, report_data: dict) -> tuple[int, dict]:
    """Update one profile while holding the history lock for the full read/modify/write."""

    with file_lock(lock_path(args.history)):
        if args.history.exists():
            history = json.loads(args.history.read_text(encoding="utf-8"))
        else:
            history = {"version": 2, "profiles": {}}
        if not isinstance(history, dict):
            raise ValueError("validation history must be a JSON object")
        version = history.get("version", 1)
        if isinstance(version, bool) or not isinstance(version, int):
            raise ValueError("validation history version must be an integer")
        history["version"] = max(2, version)
        if not isinstance(history.get("profiles", {}), dict):
            raise ValueError("validation history profiles field must be an object")

        profile_history = history.setdefault("profiles", {}).setdefault(
            args.profile,
            {"consecutive_failures": 0, "runs": [], "feed_snapshots": {}},
        )
        if not isinstance(profile_history, dict):
            raise ValueError("validation history profile must be an object")
        runs = profile_history.setdefault("runs", [])
        snapshots = profile_history.setdefault("feed_snapshots", {})
        if not isinstance(runs, list):
            raise ValueError("validation history runs field must be an array")
        if not isinstance(snapshots, dict):
            raise ValueError("validation history feed_snapshots field must be an object")

        healthy = args.healthy == "yes"
        previous_failures = profile_history.get("consecutive_failures", 0)
        if isinstance(previous_failures, bool) or not isinstance(previous_failures, int):
            raise ValueError("validation history consecutive_failures must be an integer")
        consecutive = 0 if healthy else previous_failures + 1
        profile_history["consecutive_failures"] = consecutive
        report_summary = report_data.get("summary", {})
        if not isinstance(report_summary, dict):
            raise ValueError("validation report summary must be an object")

        current_snapshots = {
            str(snapshot["url"]): snapshot
            for snapshot in (feed_snapshot(detail) for detail in report_data.get("feeds", []))
            if snapshot.get("url")
        }
        if current_snapshots:
            profile_history["feed_snapshots"] = current_snapshots
        now = datetime.now(ZoneInfo("Europe/Dublin")).isoformat(timespec="seconds")
        runs.append(
            {
                "at": now,
                "report_generated_at": report_data.get("generated_at"),
                "healthy": healthy,
                "consecutive_failures": consecutive,
                "failed_feed_count": report_summary.get("failed_feed_count"),
                "metadata_mismatch_count": report_summary.get("metadata_mismatch_count"),
                "noisy_feed_count": report_summary.get("noisy_feed_count"),
                "regression_warning_count": report_summary.get("regression_warning_count"),
                "regression_critical_count": report_summary.get("regression_critical_count"),
            }
        )
        profile_history["runs"] = runs[-20:]
        atomic_write_text(args.history, json.dumps(history, indent=2, ensure_ascii=False) + "\n")
        return consecutive, report_summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--history", required=True, type=Path)
    parser.add_argument("--profile", default="master")
    parser.add_argument("--healthy", choices=("yes", "no"), required=True)
    parser.add_argument("--current-run", action="store_true", help="reject stale or incomplete reports")
    parser.add_argument("--max-report-age-seconds", type=float, default=900)
    args = parser.parse_args()

    try:
        if args.max_report_age_seconds <= 0:
            raise ValueError("--max-report-age-seconds must be positive")
        report_data = load_report(args.report, args.profile, args.current_run, args.max_report_age_seconds)
        consecutive, report_summary = record_history(args, report_data)
    except (OSError, TypeError, ValueError, json.JSONDecodeError, TimeoutError) as exc:
        print(f"record-validation-result: {exc}")
        return 2

    alert = "yes" if consecutive >= 3 else "no"
    print(
        f"profile={args.profile} healthy={args.healthy} consecutive_failures={consecutive} "
        f"regression_warnings={report_summary.get('regression_warning_count', 0)} "
        f"alert_after_three={alert}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
