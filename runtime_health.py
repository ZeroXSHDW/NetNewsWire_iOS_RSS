#!/usr/bin/env python3
"""Write a small machine-readable health record for the unattended digest."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from state_utils import atomic_write_text


HEALTH_SCHEMA_VERSION = 1
COLLECTION_FIELDS = (
    "status",
    "source_profile",
    "feeds_considered",
    "feeds_succeeded",
    "feeds_not_modified",
    "feeds_failed",
    "feeds_with_consecutive_failures",
    "retry_count_total",
    "article_candidates",
)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _load_previous(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def _package_summary(path: Path) -> tuple[int | None, dict | None]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("runtime package must be a JSON object")
    article_count = payload.get("article_count")
    if isinstance(article_count, bool) or not isinstance(article_count, int):
        article_count = None
    raw_collection = payload.get("collection")
    collection = None
    if isinstance(raw_collection, dict):
        collection = {
            key: raw_collection[key]
            for key in COLLECTION_FIELDS
            if key in raw_collection and isinstance(raw_collection[key], (str, int, float, type(None)))
        }
    return article_count, collection


def write_health(
    path: Path,
    *,
    status: str,
    run_id: str,
    started_at: str,
    finished_at: str | None = None,
    exit_code: int | None = None,
    message: str = "",
    package_path: Path | None = None,
) -> dict:
    """Write status without retaining article text or failed-feed bodies."""

    if status not in {"running", "succeeded", "failed"}:
        raise ValueError("health status must be running, succeeded, or failed")
    previous = _load_previous(path)
    article_count = None
    collection = None
    if package_path is not None:
        article_count, collection = _package_summary(package_path)

    finished = finished_at or (None if status == "running" else now_utc())
    payload = {
        "schema_version": HEALTH_SCHEMA_VERSION,
        "status": status,
        "run_id": run_id,
        "pid": os.getpid(),
        "started_at": started_at,
        "finished_at": finished,
        "exit_code": exit_code,
        "message": message[:500],
        "article_count": article_count,
        "collection": collection,
        "last_success_at": previous.get("last_success_at"),
        "last_success_run_id": previous.get("last_success_run_id"),
    }
    if status == "succeeded":
        payload["last_success_at"] = finished
        payload["last_success_run_id"] = run_id
    atomic_write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", required=True, type=Path)
    parser.add_argument("--status", required=True, choices=("running", "succeeded", "failed"))
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--finished-at")
    parser.add_argument("--exit-code", type=int)
    parser.add_argument("--message", default="")
    parser.add_argument("--package", type=Path, help="extract bounded counts from a prepared package")
    args = parser.parse_args()
    try:
        write_health(
            args.path,
            status=args.status,
            run_id=args.run_id,
            started_at=args.started_at,
            finished_at=args.finished_at,
            exit_code=args.exit_code,
            message=args.message,
            package_path=args.package,
        )
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        print(f"runtime-health: {exc}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
