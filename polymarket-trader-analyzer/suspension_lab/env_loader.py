from __future__ import annotations

import os
from pathlib import Path


def project_root() -> Path:
    """Directory containing pyproject.toml for this package."""
    here = Path(__file__).resolve().parent
    candidate = here.parent
    if (candidate / "pyproject.toml").exists():
        return candidate
    return Path.cwd()


def load_project_env() -> Path | None:
    """Load .env from project root into os.environ. Returns path if found."""
    root = project_root()
    env_path = root / ".env"
    if not env_path.exists():
        return None

    try:
        from dotenv import load_dotenv

        load_dotenv(env_path, override=False)
    except ImportError:
        _load_env_simple(env_path)

    return env_path


def _load_env_simple(path: Path) -> None:
    """Minimal .env parser when python-dotenv is unavailable."""
    text = path.read_text(encoding="utf-8")
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
        if key and key not in os.environ:
            os.environ[key] = val


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
