"""Single-process lock so only one paper lab Kalshi client is open.

START_SUSPENSION_LAB.bat (GUI) and START_PAPER_LOGGER.bat (headless)
share this lock. A second process exits instead of opening another WS.
Does not touch the SharpMoney MM process.
"""

from __future__ import annotations

import atexit
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from suspension_lab.env_loader import project_root

LOCK_RELATIVE = Path("data") / "suspension_lab" / "lab.lock"


class LabLockHeld(Exception):
    """Another lab process already owns the Kalshi paper client."""

    def __init__(self, message: str, *, pid: int | None = None, mode: str = "") -> None:
        super().__init__(message)
        self.pid = pid
        self.mode = mode


def default_lock_path() -> Path:
    return project_root() / LOCK_RELATIVE


def _pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    except SystemError:
        return False
    return True


def _try_lock_fd(handle) -> bool:
    try:
        import fcntl

        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        return True
    except ImportError:
        pass
    except OSError:
        return False
    try:
        import msvcrt

        handle.seek(0)
        msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        return True
    except ImportError:
        return False
    except OSError:
        return False


def _unlock_fd(handle) -> None:
    try:
        import fcntl

        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        return
    except (ImportError, OSError, ValueError):
        pass
    try:
        import msvcrt

        handle.seek(0)
        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
    except (ImportError, OSError, ValueError):
        pass


class LabInstanceLock:
    """Exclusive file lock at data/suspension_lab/lab.lock."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = Path(path) if path is not None else default_lock_path()
        self._handle = None
        self.mode = ""
        self.pid = os.getpid()

    @property
    def held(self) -> bool:
        return self._handle is not None

    def acquire(self, mode: str = "lab") -> None:
        if self._handle is not None:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        handle = open(self.path, "a+", encoding="utf-8")
        if not _try_lock_fd(handle):
            info = _read_lock_info(handle)
            handle.close()
            other_pid = info.get("pid")
            other_mode = str(info.get("mode") or "lab")
            pid_txt = str(other_pid) if other_pid else "unknown"
            raise LabLockHeld(
                (
                    f"Lab already running (PID {pid_txt}, mode={other_mode}). "
                    "Only one Kalshi paper client is allowed. "
                    "Close that lab/paper_logger first. "
                    "SharpMoney MM can keep running. "
                    "Refusing a second WebSocket/REST client."
                ),
                pid=int(other_pid) if other_pid else None,
                mode=other_mode,
            )
        self._handle = handle
        self.mode = mode
        self.pid = os.getpid()
        self._write_info()
        atexit.register(self.release)

    def _write_info(self) -> None:
        if self._handle is None:
            return
        payload = {
            "pid": self.pid,
            "mode": self.mode,
            "started_at": datetime.now(tz=timezone.utc).isoformat(),
            "argv": " ".join(sys.argv[:4]),
        }
        self._handle.seek(0)
        self._handle.truncate()
        self._handle.write(json.dumps(payload))
        self._handle.flush()

    def release(self) -> None:
        handle = self._handle
        if handle is None:
            return
        self._handle = None
        try:
            _unlock_fd(handle)
        finally:
            try:
                handle.close()
            except OSError:
                pass


def _read_lock_info(handle) -> dict:
    try:
        handle.seek(0)
        raw = handle.read().strip()
        if not raw:
            return {}
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def acquire_lab_lock(mode: str = "lab", path: Path | None = None) -> LabInstanceLock:
    lock = LabInstanceLock(path)
    lock.acquire(mode)
    return lock


def lock_held_message(exc: LabLockHeld) -> str:
    return str(exc)
