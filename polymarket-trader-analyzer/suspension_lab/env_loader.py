from __future__ import annotations

import os
import re
from pathlib import Path

_SINGLE_LINE_KEYS = (
    "LAB_TICKERS",
    "LAB_GAME",
    "KALSHI_KEY_ID",
    "KALSHI_API_KEY_ID",
    "KALSHI_API_KEY",
    "KALSHI_PRIVATE_KEY_PATH",
    "KALSHI_PRIVATE_KEY_FILE",
    "KALSHI_DEMO",
    "LAB_OUTPUT_DIR",
)


def project_root() -> Path:
    """Directory containing pyproject.toml for this package."""
    here = Path(__file__).resolve().parent
    candidate = here.parent
    if (candidate / "pyproject.toml").exists():
        return candidate
    return Path.cwd()


def find_env_file() -> Path | None:
    """Search common locations for .env (Windows users often put it one folder up)."""
    root = project_root()
    candidates = [
        root / ".env",
        Path.cwd() / ".env",
        root.parent / ".env",
    ]
    seen: set[str] = set()
    for path in candidates:
        key = str(path.resolve())
        if key in seen:
            continue
        seen.add(key)
        if path.exists():
            return path.resolve()
    return None


def _extract_single_line_value(text: str, key: str) -> str | None:
    pattern = re.compile(rf"^{re.escape(key)}=(.*)$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return None
    val = match.group(1).strip()
    if not val:
        return ""
    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
        val = val[1:-1]
    return val.strip()


def _ensure_single_line_keys_from_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8-sig")
    for key in _SINGLE_LINE_KEYS:
        if os.environ.get(key, "").strip():
            continue
        val = _extract_single_line_value(text, key)
        if val is not None:
            os.environ[key] = val


def load_project_env() -> Path | None:
    """Load .env into os.environ. Returns path if found."""
    env_path = find_env_file()
    if not env_path:
        return None

    try:
        from dotenv import load_dotenv

        try:
            load_dotenv(env_path, override=True, encoding="utf-8")
        except TypeError:
            load_dotenv(env_path, override=True)
    except ImportError:
        _load_env_simple(env_path)

    # Always re-read single-line keys (PEM blocks can confuse dotenv on Windows)
    _ensure_single_line_keys_from_file(env_path)
    return env_path


def env_status_message() -> str:
    path = find_env_file()
    if not path:
        root = project_root()
        return (
            "No .env file found. Looked in:\n"
            f"  {root / '.env'}\n"
            f"  {Path.cwd() / '.env'}\n"
            f"  {root.parent / '.env'}"
        )
    load_project_env()
    tickers = os.environ.get("LAB_TICKERS", "").strip()
    key_id = resolve_api_key_id()
    lines = [f"Using .env: {path}"]
    lines.append(
        f"LAB_TICKERS: {'set (' + str(len(tickers)) + ' chars)' if tickers else 'auto-discover (empty)'}"
    )
    lines.append(f"KALSHI_KEY_ID: {'set' if key_id else 'MISSING'}")
    return "\n".join(lines)


def _load_env_simple(path: Path) -> None:
    """Minimal .env parser when python-dotenv is unavailable."""
    text = path.read_text(encoding="utf-8-sig")
    i = 0
    lines = text.splitlines()
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip()
        if val.startswith('"') and not val.endswith('"'):
            parts = [val[1:]]
            while i < len(lines):
                chunk = lines[i]
                i += 1
                if chunk.rstrip().endswith('"'):
                    parts.append(chunk.rstrip()[:-1])
                    break
                parts.append(chunk)
            val = "\n".join(parts)
        elif val.startswith("'") and not val.endswith("'"):
            parts = [val[1:]]
            while i < len(lines):
                chunk = lines[i]
                i += 1
                if chunk.rstrip().endswith("'"):
                    parts.append(chunk.rstrip()[:-1])
                    break
                parts.append(chunk)
            val = "\n".join(parts)
        else:
            val = val.strip('"').strip("'")
        if key:
            os.environ[key] = val

    _ensure_single_line_keys_from_file(path)


def resolve_api_key_id() -> str:
    return (
        os.environ.get("KALSHI_KEY_ID", "")
        or os.environ.get("KALSHI_API_KEY_ID", "")
        or os.environ.get("KALSHI_API_KEY", "")
    )


def resolve_private_key_pem() -> str:
    raw = os.environ.get("KALSHI_PRIVATE_KEY", "").strip()
    if raw:
        return raw.replace("\\n", "\n")
    path = os.environ.get("KALSHI_PRIVATE_KEY_PATH") or os.environ.get("KALSHI_PRIVATE_KEY_FILE")
    if path and Path(path).exists():
        return Path(path).read_text(encoding="utf-8")
    return ""


def resolve_private_key_path() -> str:
    path = os.environ.get("KALSHI_PRIVATE_KEY_PATH") or os.environ.get("KALSHI_PRIVATE_KEY_FILE", "")
    if path and Path(path).exists():
        return path
    pem = resolve_private_key_pem()
    if not pem:
        return ""
    cache = project_root() / ".kalshi_key.pem"
    if not cache.exists() or cache.read_text(encoding="utf-8") != pem:
        cache.write_text(pem, encoding="utf-8")
    return str(cache)
