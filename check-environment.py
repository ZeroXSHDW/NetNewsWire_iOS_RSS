#!/usr/bin/env python3
"""Check the local prerequisites for maintaining and validating the bundle."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


REQUIRED_COMMANDS = ("git", "make", "zsh")
LIVE_COMMANDS = ("curl", "xmllint")
REQUIRED_FILES = ("Makefile", "feed-manifest.json", "README.md")


def check_environment(root: Path, *, require_live_tools: bool = False) -> tuple[list[str], list[str]]:
    """Return blocking errors and non-blocking notes for the local environment."""

    errors: list[str] = []
    notes: list[str] = []
    if sys.version_info < (3, 11):
        errors.append(
            f"Python 3.11 or newer is required (found {sys.version_info.major}.{sys.version_info.minor})"
        )

    for relative_path in REQUIRED_FILES:
        if not (root / relative_path).is_file():
            errors.append(f"missing repository file: {relative_path}")

    for command in REQUIRED_COMMANDS:
        if shutil.which(command) is None:
            errors.append(f"required command not found: {command}")

    for command in LIVE_COMMANDS:
        if shutil.which(command) is None:
            message = f"live validation command not found: {command}"
            if require_live_tools:
                errors.append(message)
            else:
                notes.append(message + " (offline checks still work)")

    return errors, notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument(
        "--live",
        action="store_true",
        help="treat curl and xmllint as required for live feed validation",
    )
    args = parser.parse_args()
    root = args.root.resolve()

    try:
        errors, notes = check_environment(root, require_live_tools=args.live)
    except OSError as exc:
        print(f"doctor failed: {exc}", file=sys.stderr)
        return 2

    for note in notes:
        print(f"NOTE {note}")
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        print(f"doctor failed errors={len(errors)}")
        return 1

    mode = "live" if args.live else "offline"
    print(f"doctor passed mode={mode} python={sys.version.split()[0]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
