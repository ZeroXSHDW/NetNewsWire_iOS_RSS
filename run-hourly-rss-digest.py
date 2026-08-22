#!/usr/bin/env python3
"""Run the RSS collector and prepare one bounded Apple Intelligence batch."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from state_utils import atomic_write_text


def _prepare_module(root: Path):
    module_path = root / "prepare-rss-digest-input.py"
    spec = importlib.util.spec_from_file_location("prepare_rss_digest_input", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run(command: list[str], *, root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )


def _print_process_failure(label: str, process: subprocess.CompletedProcess[str]) -> None:
    detail = process.stderr.strip() or process.stdout.strip() or f"exit {process.returncode}"
    print(f"{label}: {detail}", file=sys.stderr)


def _default_since(fetch_state: Path, *, initial_hours: float, overlap_minutes: float) -> str:
    """Return a publication cursor that prevents old feed archives leaking into each run."""

    previous_run = ""
    if fetch_state.exists():
        try:
            decoded = json.loads(fetch_state.read_text(encoding="utf-8"))
            previous_run = str(decoded.get("last_run", "")) if isinstance(decoded, dict) else ""
        except (OSError, json.JSONDecodeError):
            previous_run = ""
    if previous_run:
        try:
            cursor = datetime.fromisoformat(previous_run)
            if cursor.tzinfo is None:
                cursor = cursor.replace(tzinfo=ZoneInfo("Europe/Dublin"))
            cursor -= timedelta(minutes=overlap_minutes)
            return cursor.isoformat(timespec="seconds")
        except ValueError:
            pass
    cursor = datetime.now(ZoneInfo("Europe/Dublin")) - timedelta(hours=initial_hours)
    return cursor.isoformat(timespec="seconds")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path("feed-manifest.json"))
    parser.add_argument("--source-profile", default="master", help="profile fetched from the manifest")
    parser.add_argument("--digest-profile", default="master", help="profile budget used for Apple Intelligence input")
    parser.add_argument("--fetch-state", type=Path, default=Path(".rss-fetch-state.json"))
    parser.add_argument("--digest-state", type=Path, default=Path(".digest-state.json"))
    parser.add_argument("--output", type=Path, default=Path("hourly-digest-input.json"))
    parser.add_argument("--shortcut-output", type=Path, default=Path("shortcut-digest.txt"))
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--max-items-per-feed", type=int, default=20)
    parser.add_argument("--digest-max-items", type=int, help="override the prepared digest item budget")
    parser.add_argument("--digest-max-item-chars", type=int, help="override the prepared per-item text budget")
    parser.add_argument("--digest-max-total-chars", type=int, help="override the prepared total text budget")
    parser.add_argument("--max-response-bytes", type=int)
    parser.add_argument("--user-agent")
    parser.add_argument("--since", help="explicit publication cursor; otherwise use the previous collection run")
    parser.add_argument("--initial-lookback-hours", type=float, default=24.0)
    parser.add_argument("--overlap-minutes", type=float, default=15.0)
    parser.add_argument("--prompt-file", type=Path, default=Path("docs/Apple-Intelligence-RSS-Summary-Prompt.md"))
    parser.add_argument("--dry-run", action="store_true", help="do not update either state file")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    manifest = (root / args.manifest).resolve() if not args.manifest.is_absolute() else args.manifest
    fetch_state = args.fetch_state.resolve()
    if args.initial_lookback_hours <= 0:
        parser.error("--initial-lookback-hours must be positive")
    if args.overlap_minutes < 0:
        parser.error("--overlap-minutes must not be negative")
    since = args.since or _default_since(
        fetch_state,
        initial_hours=args.initial_lookback_hours,
        overlap_minutes=args.overlap_minutes,
    )
    output = args.output.resolve()
    shortcut_output = args.shortcut_output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    shortcut_output.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix=".hourly-rss-", dir=output.parent) as temporary:
        temporary_dir = Path(temporary)
        raw_output = temporary_dir / "rss-articles.json"
        prepared_output = temporary_dir / "digest-input.json"
        prepared_shortcut = temporary_dir / "shortcut-digest.txt"
        fetch_command = [
            sys.executable,
            str(root / "fetch-rss-digest-input.py"),
            "--manifest",
            str(manifest),
            "--profile",
            args.source_profile,
            "--state",
            str(fetch_state),
            "--output",
            str(raw_output),
            "--timeout",
            str(args.timeout),
            "--workers",
            str(args.workers),
            "--max-items-per-feed",
            str(args.max_items_per_feed),
        ]
        if args.max_response_bytes is not None:
            fetch_command.extend(["--max-response-bytes", str(args.max_response_bytes)])
        if args.user_agent:
            fetch_command.extend(["--user-agent", args.user_agent])
        if args.dry_run:
            fetch_command.append("--dry-run")
        fetched = _run(fetch_command, root=root)
        if fetched.returncode != 0:
            _print_process_failure("RSS collection failed", fetched)
            return fetched.returncode

        raw_payload = json.loads(raw_output.read_text(encoding="utf-8"))
        prepare_command = [
            sys.executable,
            str(root / "prepare-rss-digest-input.py"),
            "--input",
            str(raw_output),
            "--output",
            str(prepared_output),
            "--shortcut-output",
            str(prepared_shortcut),
            "--manifest",
            str(manifest),
            "--state",
            str(args.digest_state.resolve()),
            "--profile",
            args.digest_profile,
            "--prompt-file",
            str(args.prompt_file),
            "--since",
            since,
        ]
        if args.dry_run:
            prepare_command.append("--dry-run")
        for option, value in (
            ("--max-items", args.digest_max_items),
            ("--max-item-chars", args.digest_max_item_chars),
            ("--max-total-chars", args.digest_max_total_chars),
        ):
            if value is not None:
                prepare_command.extend([option, str(value)])
        prepared = _run(prepare_command, root=root)
        if prepared.returncode != 0:
            _print_process_failure("Digest preparation failed", prepared)
            return prepared.returncode

        package = json.loads(prepared_output.read_text(encoding="utf-8"))
        collection_summary = raw_payload.get("summary", {})
        failed_feeds = raw_payload.get("failed_feeds", [])
        package["collection"] = {
            "status": "partial" if failed_feeds else "ok",
            "source_profile": raw_payload.get("profile", args.source_profile),
            "feeds_considered": collection_summary.get("feeds_considered", 0),
            "feeds_succeeded": collection_summary.get("feeds_succeeded", 0),
            "feeds_not_modified": collection_summary.get("feeds_not_modified", 0),
            "feeds_failed": collection_summary.get("feeds_failed", 0),
            "article_candidates": collection_summary.get("article_candidates", 0),
            "failed_feeds": failed_feeds,
        }
        prepare_module = _prepare_module(root)
        digest_text = prepare_module.shortcut_text(package)
        atomic_write_text(output, json.dumps(package, indent=2, ensure_ascii=False) + "\n")
        atomic_write_text(shortcut_output, digest_text)

    print(
        json.dumps(
            {
                "profile": args.digest_profile,
                "article_count": package.get("article_count", 0),
                "collection": package.get("collection", {}),
                "output": str(output),
                "shortcut_output": str(shortcut_output),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
