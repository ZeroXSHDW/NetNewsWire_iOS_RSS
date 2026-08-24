#!/usr/bin/env python3
"""Run the RSS collector and prepare one bounded Apple Intelligence batch."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from state_utils import atomic_write_bytes, atomic_write_text, directory_lock


STATE_TRANSACTION_SCHEMA_VERSION = 1


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


def _stage_state(source: Path, destination: Path) -> None:
    """Copy an existing state snapshot into the run workspace, if present."""

    if source.exists() and not source.is_file():
        raise ValueError(f"state path is not a file: {source}")
    if source.is_file():
        atomic_write_bytes(destination, source.read_bytes())


def _commit_state(source: Path, destination: Path, label: str) -> None:
    """Commit a successfully updated staged state after outputs are durable."""

    if not source.is_file():
        raise ValueError(f"{label} did not produce a state file: {source}")
    atomic_write_bytes(destination, source.read_bytes())


def _remove_transaction(path: Path) -> None:
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass
    except OSError:
        # Leave a committed transaction marker for the next run to remove.
        pass


def _begin_state_transaction(output_parent: Path, states: list[tuple[str, Path]]) -> Path:
    """Back up real state before the multi-file commit and write a recovery journal."""

    transaction = Path(tempfile.mkdtemp(prefix=".hourly-commit.", dir=output_parent))
    entries = []
    try:
        for name, destination in states:
            if destination.exists() and not destination.is_file():
                raise ValueError(f"state path is not a file: {destination}")
            present = destination.is_file()
            backup_name = f"{name}.backup"
            if present:
                atomic_write_bytes(transaction / backup_name, destination.read_bytes())
            entries.append(
                {
                    "destination": str(destination),
                    "present": present,
                    "backup": backup_name,
                }
            )
        atomic_write_text(
            transaction / "journal.json",
            json.dumps(
                {
                    "schema_version": STATE_TRANSACTION_SCHEMA_VERSION,
                    "status": "prepared",
                    "states": entries,
                },
                indent=2,
            )
            + "\n",
        )
    except BaseException:
        _remove_transaction(transaction)
        raise
    return transaction


def _mark_transaction_committed(transaction: Path) -> None:
    journal_path = transaction / "journal.json"
    journal = json.loads(journal_path.read_text(encoding="utf-8"))
    journal["status"] = "committed"
    atomic_write_text(journal_path, json.dumps(journal, indent=2) + "\n")


def _recover_state_transactions(output_parent: Path) -> None:
    """Recover a state commit interrupted between its two atomic replacements."""

    for transaction in sorted(output_parent.glob(".hourly-commit.*")):
        if not transaction.is_dir():
            continue
        journal_path = transaction / "journal.json"
        journal = json.loads(journal_path.read_text(encoding="utf-8"))
        schema_version = journal.get("schema_version")
        if (
            isinstance(schema_version, bool)
            or not isinstance(schema_version, int)
            or schema_version != STATE_TRANSACTION_SCHEMA_VERSION
        ):
            raise ValueError(f"unsupported state transaction schema: {journal_path}")
        states = journal.get("states")
        if not isinstance(states, list):
            raise ValueError(f"invalid state transaction journal: {journal_path}")
        if journal.get("status") == "committed":
            _remove_transaction(transaction)
            continue
        if journal.get("status") != "prepared":
            raise ValueError(f"invalid state transaction status: {journal_path}")
        for entry in states:
            if not isinstance(entry, dict):
                raise ValueError(f"invalid state transaction entry: {journal_path}")
            destination = Path(str(entry.get("destination", "")))
            if entry.get("present"):
                backup = transaction / str(entry.get("backup", ""))
                if not backup.is_file():
                    raise ValueError(f"missing state transaction backup: {backup}")
                atomic_write_bytes(destination, backup.read_bytes())
            else:
                destination.unlink(missing_ok=True)
        _remove_transaction(transaction)


def _prune_stale_run_directories(output_parent: Path) -> None:
    """Remove collector workspaces left behind by a hard process kill."""

    for stale in output_parent.glob(".hourly-rss-*"):
        if stale.is_dir():
            _remove_transaction(stale)


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


def _run_pipeline(
    args: argparse.Namespace,
    *,
    root: Path,
    manifest: Path,
    fetch_state: Path,
    output: Path,
    shortcut_output: Path,
) -> int:
    """Run collection and preparation while the caller holds the pipeline lock."""

    since = args.since or _default_since(
        fetch_state,
        initial_hours=args.initial_lookback_hours,
        overlap_minutes=args.overlap_minutes,
    )
    digest_state = args.digest_state.resolve()

    with tempfile.TemporaryDirectory(prefix=".hourly-rss-", dir=output.parent) as temporary:
        temporary_dir = Path(temporary)
        raw_output = temporary_dir / "rss-articles.json"
        prepared_output = temporary_dir / "digest-input.json"
        prepared_shortcut = temporary_dir / "shortcut-digest.txt"
        staged_fetch_state = temporary_dir / "fetch-state.json"
        staged_digest_state = temporary_dir / "digest-state.json"
        _stage_state(fetch_state, staged_fetch_state)
        _stage_state(digest_state, staged_digest_state)
        fetch_command = [
            sys.executable,
            str(root / "fetch-rss-digest-input.py"),
            "--manifest",
            str(manifest),
            "--profile",
            args.source_profile,
            "--state",
            str(staged_fetch_state),
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
        if not isinstance(raw_payload, dict):
            raise ValueError("RSS collection output must be a JSON object")
        collection_summary = raw_payload.get("summary", {})
        failed_feeds = raw_payload.get("failed_feeds", [])
        if not isinstance(collection_summary, dict) or not isinstance(failed_feeds, list):
            raise ValueError("RSS collection output has an invalid summary")

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
            str(staged_digest_state),
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
        if not isinstance(package, dict):
            raise ValueError("digest preparation output must be a JSON object")
        package["collection"] = {
            "status": "partial" if failed_feeds else "ok",
            "source_profile": raw_payload.get("profile", args.source_profile),
            "feeds_considered": collection_summary.get("feeds_considered", 0),
            "feeds_succeeded": collection_summary.get("feeds_succeeded", 0),
            "feeds_not_modified": collection_summary.get("feeds_not_modified", 0),
            "feeds_failed": collection_summary.get("feeds_failed", 0),
            "feeds_with_consecutive_failures": collection_summary.get(
                "feeds_with_consecutive_failures", 0
            ),
            "retry_count_total": collection_summary.get("retry_count_total", 0),
            "article_candidates": collection_summary.get("article_candidates", 0),
            "failed_feeds": failed_feeds,
        }
        prepare_module = _prepare_module(root)
        digest_text = prepare_module.shortcut_text(package)
        transaction = None
        transaction_committed = False
        try:
            if not args.dry_run:
                transaction = _begin_state_transaction(
                    output.parent,
                    [("fetch-state", fetch_state), ("digest-state", digest_state)],
                )
            atomic_write_text(output, json.dumps(package, indent=2, ensure_ascii=False) + "\n")
            atomic_write_text(shortcut_output, digest_text)
            if not args.dry_run:
                _commit_state(staged_fetch_state, fetch_state, "RSS fetch")
                _commit_state(staged_digest_state, digest_state, "digest preparation")
                _mark_transaction_committed(transaction)
                transaction_committed = True
        finally:
            if transaction is not None and transaction_committed:
                _remove_transaction(transaction)

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
    output = args.output.resolve()
    shortcut_output = args.shortcut_output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    shortcut_output.parent.mkdir(parents=True, exist_ok=True)

    def run_locked() -> int:
        _recover_state_transactions(output.parent)
        _prune_stale_run_directories(output.parent)
        return _run_pipeline(
            args,
            root=root,
            manifest=manifest,
            fetch_state=fetch_state,
            output=output,
            shortcut_output=shortcut_output,
        )

    try:
        run_lock = output.parent / ".hourly-run.lock"
        shell_owner = os.environ.get("NETNEWSWIRE_RUN_LOCK_OWNER", "")
        if shell_owner == str(os.getppid()):
            return run_locked()
        with directory_lock(run_lock, timeout_seconds=0):
            return run_locked()
    except TimeoutError as exc:
        print(f"hourly digest already running: {exc}", file=sys.stderr)
        return 75
    except (OSError, ValueError, json.JSONDecodeError, RuntimeError) as exc:
        print(f"run-hourly-rss-digest: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
