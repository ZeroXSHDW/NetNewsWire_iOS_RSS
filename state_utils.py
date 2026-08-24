"""Small Unix-safe primitives for local state and report writes."""

from __future__ import annotations

import fcntl
import os
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


def lock_path(path: str | Path) -> Path:
    """Return a predictable sibling lock path for a state file."""

    target = Path(path)
    return target.with_name(f"{target.name}.lock")


@contextmanager
def file_lock(
    path: str | Path,
    *,
    timeout_seconds: float = 15.0,
    poll_seconds: float = 0.05,
) -> Iterator[object]:
    """Hold an advisory lock and record enough metadata to diagnose contention."""

    lock_path = Path(path)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+", encoding="utf-8") as handle:
        deadline = time.monotonic() + timeout_seconds
        while True:
            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise TimeoutError(f"timed out waiting for lock: {lock_path}")
                time.sleep(poll_seconds)

        handle.seek(0)
        handle.truncate()
        handle.write(f"pid={os.getpid()} acquired_at={time.time():.3f}\n")
        handle.flush()
        try:
            yield handle
        finally:
            handle.seek(0)
            handle.truncate()
            handle.flush()
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


@contextmanager
def directory_lock(
    path: str | Path,
    *,
    timeout_seconds: float = 0.0,
    poll_seconds: float = 0.05,
) -> Iterator[Path]:
    """Hold a portable process lock shared with the shell launch wrapper."""

    target = Path(path)
    deadline = time.monotonic() + timeout_seconds
    while True:
        try:
            target.mkdir(parents=True, exist_ok=False)
            break
        except FileExistsError:
            owner_path = target / "pid"
            try:
                owner_pid = int(owner_path.read_text(encoding="utf-8").strip())
            except (OSError, ValueError):
                owner_pid = 0
            if not owner_pid:
                # Never steal a directory while its creator may still be
                # between mkdir and writing the PID. A crashed process that
                # died in that tiny window requires manual cleanup.
                if time.monotonic() >= deadline:
                    raise TimeoutError(f"run lock has no valid owner: {target}")
                time.sleep(poll_seconds)
                continue
            if owner_pid:
                try:
                    os.kill(owner_pid, 0)
                except ProcessLookupError:
                    owner_pid = 0
                except PermissionError:
                    # A live process owned by another user is still a lock owner.
                    pass
            if not owner_pid:
                try:
                    owner_path.unlink(missing_ok=True)
                    target.rmdir()
                    continue
                except OSError:
                    pass
            if time.monotonic() >= deadline:
                raise TimeoutError(f"timed out waiting for run lock: {target}")
            time.sleep(poll_seconds)

    try:
        (target / "pid").write_text(f"{os.getpid()}\n", encoding="utf-8")
        yield target
    finally:
        try:
            (target / "pid").unlink(missing_ok=True)
            target.rmdir()
        except OSError:
            pass


def atomic_write_text(path: str | Path, text: str) -> None:
    """Write text through a unique same-directory temporary file and replace."""

    atomic_write_bytes(path, text.encode("utf-8"))


def atomic_write_bytes(path: str | Path, data: bytes) -> None:
    """Write bytes through a unique same-directory temporary file and replace."""

    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    file_descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        suffix=".tmp",
        dir=destination.parent,
        text=True,
    )
    try:
        with os.fdopen(file_descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, destination)
        _fsync_directory(destination.parent)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise

def _fsync_directory(directory: Path) -> None:
    """Best-effort sync of the containing directory after an atomic replace."""

    try:
        descriptor = os.open(directory, os.O_RDONLY)
    except OSError:
        return
    try:
        try:
            os.fsync(descriptor)
        except OSError:
            # Some filesystems do not permit directory fsync. The replace is
            # still atomic, so retain the stronger behavior where available
            # without making otherwise healthy local writes fail.
            pass
    finally:
        os.close(descriptor)
