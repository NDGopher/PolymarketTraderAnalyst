"""Kalshi HTTP 429 helpers. Paper lab only - no live orders."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from email.utils import parsedate_to_datetime
from typing import Any, Mapping

DEFAULT_RETRY_AFTER_S = 5.0
MAX_RETRY_SLEEP_S = 60.0


def retry_after_seconds(
    headers: Mapping[str, Any] | None,
    *,
    default: float = DEFAULT_RETRY_AFTER_S,
) -> float:
    """Parse Retry-After (seconds or HTTP-date). Default 5s when missing/invalid."""
    if not headers:
        return max(default, 0.1)
    raw = ""
    for key, value in headers.items():
        if str(key).lower() == "retry-after":
            raw = str(value or "").strip()
            break
    if not raw:
        return max(default, 0.1)
    try:
        return max(float(raw), 0.1)
    except ValueError:
        pass
    try:
        dt = parsedate_to_datetime(raw)
        return max(dt.timestamp() - time.time(), 0.1)
    except (TypeError, ValueError, OverflowError):
        return max(default, 0.1)


@dataclass
class FetchStats:
    """Out-band result of a discovery HTTP burst."""

    rate_limited: bool = False
    retry_after: float = 0.0
    series_429: bool = False
    skipped_global_scan: bool = False
    workers: int = 0
    requests: int = 0

    def note_429(self, wait: float) -> None:
        self.rate_limited = True
        self.retry_after = max(self.retry_after, wait, DEFAULT_RETRY_AFTER_S)


@dataclass
class HttpFetch:
    payload: dict | None = None
    rate_limited: bool = False
    retry_after: float = 0.0
    status: int = 0


def get_json_with_retry(
    session: Any,
    url: str,
    params: dict,
    timeout: float,
    label: str,
    *,
    max_attempts: int = 4,
    sleep: Any = time.sleep,
    stats: FetchStats | None = None,
) -> HttpFetch:
    """GET JSON. On 429 honor Retry-After (default 5s) then exponential backoff."""
    import logging

    import requests

    logger = logging.getLogger(__name__)
    backoff = DEFAULT_RETRY_AFTER_S
    last_wait = 0.0
    last_status = 0
    for attempt in range(max_attempts):
        try:
            resp = session.get(url, params=params, timeout=timeout)
        except requests.RequestException as exc:
            logger.warning("Failed %s: %s", label, exc)
            return HttpFetch(status=0)
        if stats is not None:
            stats.requests += 1
        last_status = int(resp.status_code)
        if resp.status_code == 429:
            wait = retry_after_seconds(getattr(resp, "headers", None), default=backoff)
            wait = min(max(wait, 0.1), MAX_RETRY_SLEEP_S)
            last_wait = wait
            logger.warning(
                "HTTP 429 on %s - Retry-After %.1fs (attempt %s/%s)",
                label,
                wait,
                attempt + 1,
                max_attempts,
            )
            if stats is not None:
                stats.note_429(wait)
            sleep(wait)
            backoff = min(backoff * 2.0, MAX_RETRY_SLEEP_S)
            continue
        if resp.status_code != 200:
            logger.warning("HTTP %s on %s", resp.status_code, label)
            return HttpFetch(status=last_status)
        payload = resp.json()
        if not isinstance(payload, dict):
            return HttpFetch(status=last_status)
        return HttpFetch(payload=payload, status=last_status)
    if stats is not None:
        stats.note_429(last_wait or DEFAULT_RETRY_AFTER_S)
    return HttpFetch(
        rate_limited=True,
        retry_after=last_wait or DEFAULT_RETRY_AFTER_S,
        status=last_status or 429,
    )
