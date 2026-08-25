"""HTTP client for Polymarket public APIs with resilient pagination."""

from __future__ import annotations

import logging
import time
from typing import Any, Callable, Iterable, Iterator, Optional
from urllib.parse import urlencode

import requests

log = logging.getLogger(__name__)

DATA_API = "https://data-api.polymarket.com"
GAMMA_API = "https://gamma-api.polymarket.com"

DEFAULT_HEADERS = {
    "User-Agent": "polyanalyst/1.0 (+https://github.com/polyanalyst; research)",
    "Accept": "application/json",
}


class PolymarketClient:
    def __init__(
        self,
        session: Optional[requests.Session] = None,
        min_interval: float = 0.12,
        max_retries: int = 6,
    ) -> None:
        self.session = session or requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)
        self.min_interval = min_interval
        self.max_retries = max_retries
        self._last_request = 0.0

    def _throttle(self) -> None:
        elapsed = time.monotonic() - self._last_request
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)

    def get_json(self, base: str, path: str, params: Optional[dict] = None) -> Any:
        url = f"{base}{path}"
        query = {k: v for k, v in (params or {}).items() if v is not None}
        last_err: Exception | None = None
        for attempt in range(self.max_retries):
            self._throttle()
            try:
                resp = self.session.get(url, params=query, timeout=90)
                self._last_request = time.monotonic()
                if resp.status_code in (429, 500, 502, 503, 504):
                    wait = min(32.0, (2**attempt) * 0.75)
                    log.warning("HTTP %s on %s — retry in %.1fs", resp.status_code, path, wait)
                    time.sleep(wait)
                    continue
                resp.raise_for_status()
                return resp.json()
            except requests.RequestException as exc:
                last_err = exc
                wait = min(32.0, (2**attempt) * 0.75)
                log.warning("Request error %s — retry in %.1fs", exc, wait)
                time.sleep(wait)
        raise RuntimeError(f"Failed GET {path}?{urlencode(query)}: {last_err}")

    # ---- identity ----

    def resolve_trader(self, identifier: str) -> dict[str, Any]:
        """Resolve username or wallet to a profile dict with proxyWallet + name."""
        ident = identifier.strip()
        if ident.startswith("@"):
            ident = ident[1:]
        if ident.startswith("0x") and len(ident) == 42:
            profile = self.get_json(GAMMA_API, "/public-profile", {"address": ident})
            wallet = (profile.get("proxyWallet") or ident).lower()
            return {
                "username": profile.get("name") or profile.get("pseudonym") or wallet,
                "wallet": wallet,
                "profile": profile,
            }

        # Username → leaderboard lookup (works for public usernames)
        for period in ("ALL", "MONTH", "WEEK", "DAY"):
            rows = self.get_json(
                DATA_API,
                "/v1/leaderboard",
                {"timePeriod": period, "userName": ident, "limit": 5},
            )
            if rows:
                row = rows[0]
                wallet = row["proxyWallet"].lower()
                profile = self.get_json(GAMMA_API, "/public-profile", {"address": wallet})
                return {
                    "username": row.get("userName") or ident,
                    "wallet": wallet,
                    "profile": profile,
                    "leaderboard_hint": row,
                }

        raise LookupError(f"Could not resolve trader identifier: {identifier!r}")

    def leaderboard_entry(self, wallet: str, time_period: str = "ALL") -> Optional[dict]:
        rows = self.get_json(
            DATA_API,
            "/v1/leaderboard",
            {"timePeriod": time_period, "user": wallet, "limit": 1},
        )
        return rows[0] if rows else None

    def traded_markets(self, wallet: str) -> int:
        data = self.get_json(DATA_API, "/traded", {"user": wallet})
        return int(data.get("traded") or 0)

    def portfolio_value(self, wallet: str) -> float:
        data = self.get_json(DATA_API, "/value", {"user": wallet})
        if isinstance(data, list) and data:
            return float(data[0].get("value") or 0)
        if isinstance(data, dict):
            return float(data.get("value") or 0)
        return 0.0

    # ---- paginated fetchers ----

    def iter_time_window_pages(
        self,
        fetch_page: Callable[[int, int, int, int], list[dict]],
        start_ts: int,
        end_ts: int,
        window_seconds: int,
        max_offset: int,
        limit: int,
        ts_key: str = "timestamp",
    ) -> Iterator[dict]:
        """Page through [start_ts, end_ts] using sliding windows to avoid offset caps."""
        seen: set[str] = set()
        stack: list[tuple[int, int, int]] = [(start_ts, end_ts, window_seconds)]

        while stack:
            window_start, range_end, win = stack.pop()
            if window_start > range_end:
                continue
            window_end = min(window_start + win - 1, range_end)
            offset = 0
            overflow = False
            while True:
                batch = fetch_page(window_start, window_end, limit, offset)
                if not batch:
                    break
                for row in batch:
                    key = _row_key(row)
                    if key in seen:
                        continue
                    seen.add(key)
                    yield row
                if len(batch) < limit:
                    break
                next_offset = offset + limit
                # offset budget exhausted while more data may remain → bisect window
                if next_offset > max_offset:
                    overflow = True
                    break
                offset = next_offset

            if overflow:
                if window_end <= window_start:
                    log.error(
                        "Unable to page window %s-%s without truncation",
                        window_start,
                        window_end,
                    )
                else:
                    mid = (window_start + window_end) // 2
                    # Push right then left so left is processed first
                    stack.append((mid + 1, window_end, max(1, win // 2)))
                    stack.append((window_start, mid, max(1, win // 2)))
                continue

            # Advance to the next window inside the current range
            nxt = window_end + 1
            if nxt <= range_end:
                stack.append((nxt, range_end, win))

    def fetch_activity(
        self,
        wallet: str,
        start_ts: int = 1,
        end_ts: Optional[int] = None,
        include_deposits: bool = True,
        window_seconds: int = 24 * 3600,
    ) -> list[dict]:
        end = end_ts or int(time.time()) + 60
        # Discover true oldest if start is default
        if start_ts <= 1:
            oldest = self.get_json(
                DATA_API,
                "/activity",
                {
                    "user": wallet,
                    "limit": 1,
                    "sortDirection": "ASC",
                    "start": 1,
                    "excludeDepositsWithdrawals": not include_deposits,
                },
            )
            if oldest:
                start_ts = int(oldest[0]["timestamp"])

        def fetch_page(ws: int, we: int, limit: int, offset: int) -> list[dict]:
            return self.get_json(
                DATA_API,
                "/activity",
                {
                    "user": wallet,
                    "limit": limit,
                    "offset": offset,
                    "start": ws,
                    "end": we,
                    "sortDirection": "ASC",
                    "excludeDepositsWithdrawals": not include_deposits,
                },
            ) or []

        rows = list(
            self.iter_time_window_pages(
                fetch_page, start_ts, end, window_seconds, max_offset=5000, limit=500
            )
        )
        rows.sort(key=lambda r: (r.get("timestamp") or 0, r.get("transactionHash") or ""))
        return rows

    def fetch_trades(
        self,
        wallet: str,
        start_ts: int = 1,
        end_ts: Optional[int] = None,
        window_seconds: int = 24 * 3600,
        taker_only: bool = False,
    ) -> list[dict]:
        end = end_ts or int(time.time()) + 60
        if start_ts <= 1:
            # Use activity ASC to find first trade timestamp cheaply
            oldest = self.get_json(
                DATA_API,
                "/activity",
                {
                    "user": wallet,
                    "limit": 1,
                    "sortDirection": "ASC",
                    "start": 1,
                    "type": "TRADE",
                },
            )
            if oldest:
                start_ts = int(oldest[0]["timestamp"])

        def fetch_page(ws: int, we: int, limit: int, offset: int) -> list[dict]:
            return self.get_json(
                DATA_API,
                "/trades",
                {
                    "user": wallet,
                    "limit": limit,
                    "offset": offset,
                    "start": ws,
                    "end": we,
                    "takerOnly": "true" if taker_only else "false",
                },
            ) or []

        rows = list(
            self.iter_time_window_pages(
                fetch_page, start_ts, end, window_seconds, max_offset=10000, limit=1000
            )
        )
        rows.sort(key=lambda r: (r.get("timestamp") or 0, r.get("transactionHash") or ""))
        return rows

    def fetch_closed_positions(self, wallet: str) -> list[dict]:
        rows: list[dict] = []
        offset = 0
        while True:
            batch = self.get_json(
                DATA_API,
                "/closed-positions",
                {
                    "user": wallet,
                    "limit": 50,
                    "offset": offset,
                    "sortBy": "TIMESTAMP",
                    "sortDirection": "ASC",
                },
            ) or []
            if not batch:
                break
            rows.extend(batch)
            if len(batch) < 50:
                break
            offset += 50
            if offset > 100000:
                break
        return rows

    def fetch_positions(self, wallet: str) -> list[dict]:
        rows: list[dict] = []
        offset = 0
        # API default limit varies; request 100 and page until short page
        while True:
            batch = self.get_json(
                DATA_API,
                "/positions",
                {"user": wallet, "limit": 100, "offset": offset},
            ) or []
            if not batch:
                break
            rows.extend(batch)
            if len(batch) < 100:
                break
            offset += 100
            if offset > 50000:
                break
        return rows


def _row_key(row: dict) -> str:
    return "|".join(
        str(row.get(k, ""))
        for k in (
            "transactionHash",
            "type",
            "side",
            "asset",
            "conditionId",
            "timestamp",
            "size",
            "price",
            "usdcSize",
            "outcomeIndex",
        )
    )


def chunked(items: Iterable[Any], size: int) -> Iterator[list[Any]]:
    buf: list[Any] = []
    for item in items:
        buf.append(item)
        if len(buf) >= size:
            yield buf
            buf = []
    if buf:
        yield buf
