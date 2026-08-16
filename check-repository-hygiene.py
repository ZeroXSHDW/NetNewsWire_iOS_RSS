#!/usr/bin/env python3
"""Check tracked files for runtime state, credentials and machine-specific paths."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path


FORBIDDEN_TRACKED_NAMES = {
    ".digest-state.json",
    ".digest-state.json.lock",
    ".validation-history.json",
    ".validation-history.json.lock",
    ".rss-validation-cache",
    ".rss-validation-cache.lock",
}
FORBIDDEN_TRACKED_PARTS = {
    "__pycache__",
    ".rss-validation-cache",
    ".rss-validation-cache.lock",
}
SENSITIVE_NAME_PATTERNS = (
    re.compile(r"(^|/)\.env(?:\..*)?$", re.IGNORECASE),
    re.compile(r"(^|/)(?:credentials|secrets|private-key)(?:\..*)?$", re.IGNORECASE),
    re.compile(r"(^|/)(?:id_rsa|id_ed25519|id_ecdsa)(?:\..*)?$", re.IGNORECASE),
)

# These patterns intentionally target high-confidence secrets and absolute paths.
# They do not reject ordinary URLs, documentation examples or relative paths.
CONTENT_PATTERNS = (
    (
        "private key material",
        re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ),
    (
        "GitHub token",
        re.compile(rb"\b(?:gh[pousr]|github_pat)_[A-Za-z0-9_]{20,}\b"),
    ),
    (
        "AWS access key",
        re.compile(rb"\bAKIA[0-9A-Z]{16}\b"),
    ),
    (
        "secret assignment",
        re.compile(
            rb"(?i)\b(?:aws_secret_access_key|api[_-]?key|secret[_-]?key)\s*[:=]\s*[^\s\"']{8,}"
        ),
    ),
    (
        "OpenAI-style API key",
        re.compile(rb"\bsk-[A-Za-z0-9_-]{20,}\b"),
    ),
    (
        "macOS absolute user path",
        re.compile(rb"(?m)(?:^|[\s\"'(=:])/Users/[A-Za-z0-9._-]+(?:/|$)"),
    ),
    (
        "Linux absolute user path",
        re.compile(rb"(?m)(?:^|[\s\"'(=:])/home/[A-Za-z0-9._-]+(?:/|$)"),
    ),
    (
        "Windows absolute user path",
        re.compile(rb"(?im)(?:^|[\s\"'(=:])[A-Z]:\\Users\\[A-Za-z0-9._-]+(?:\\|$)"),
    ),
)


def tracked_files(root: Path) -> list[Path]:
    """Return repository-relative paths tracked by Git."""

    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"],
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(detail or "git ls-files failed")
    return [Path(value) for value in result.stdout.decode("utf-8").split("\0") if value]


def path_findings(relative_path: Path) -> list[str]:
    """Return findings caused by a tracked path name."""

    path_text = relative_path.as_posix()
    findings: list[str] = []
    if relative_path.name in FORBIDDEN_TRACKED_NAMES:
        findings.append("tracked runtime state")
    if any(part in FORBIDDEN_TRACKED_PARTS for part in relative_path.parts):
        findings.append("tracked runtime state")
    for pattern in SENSITIVE_NAME_PATTERNS:
        if pattern.search(path_text):
            findings.append("sensitive-looking filename")
            break
    return findings


def content_findings(content: bytes) -> list[tuple[str, int]]:
    """Return high-confidence content findings with one-based line numbers."""

    findings: list[tuple[str, int]] = []
    for label, pattern in CONTENT_PATTERNS:
        match = pattern.search(content)
        if match:
            line = content.count(b"\n", 0, match.start()) + 1
            findings.append((label, line))
    return findings


def check_repository(root: Path) -> tuple[list[str], int]:
    """Inspect every tracked file and return errors plus the scanned file count."""

    errors: list[str] = []
    files = tracked_files(root)
    for relative_path in files:
        path_text = relative_path.as_posix()
        for finding in path_findings(relative_path):
            errors.append(f"{path_text}: {finding}")
        absolute_path = root / relative_path
        try:
            content = absolute_path.read_bytes()
        except OSError as exc:
            errors.append(f"{path_text}: cannot read tracked file: {exc}")
            continue
        for finding, line in content_findings(content):
            errors.append(f"{path_text}:{line}: possible {finding}")
    return errors, len(files)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        errors, file_count = check_repository(root)
    except (OSError, RuntimeError, UnicodeError) as exc:
        print(f"hygiene-check failed: {exc}")
        return 2
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        print(f"hygiene-check failed errors={len(errors)}")
        return 1
    print(f"hygiene-check passed tracked_files={file_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
