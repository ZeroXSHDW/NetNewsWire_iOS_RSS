#!/usr/bin/env python3
"""Run one macOS Shortcut with a hard timeout and a fresh output path."""

from __future__ import annotations

import argparse
import os
import signal
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("output_path", type=Path)
    parser.add_argument("--timeout", type=float, default=900.0)
    args = parser.parse_args()
    if not args.name.strip():
        parser.error("Shortcut name must not be empty")
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    if not args.input_path.is_file():
        parser.error(f"Shortcut input does not exist: {args.input_path}")

    args.output_path.unlink(missing_ok=True)
    command = [
        "shortcuts",
        "run",
        args.name,
        "--input-path",
        str(args.input_path),
        "--output-path",
        str(args.output_path),
    ]
    try:
        process = subprocess.Popen(command, start_new_session=True)
    except OSError as exc:
        print(f"could not run Shortcut: {exc}")
        return 127
    try:
        return process.wait(timeout=args.timeout)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()
        print(f"Shortcut timed out after {args.timeout:g} seconds")
        return 124


if __name__ == "__main__":
    raise SystemExit(main())
