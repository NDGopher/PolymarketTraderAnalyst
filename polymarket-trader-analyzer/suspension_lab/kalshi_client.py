from __future__ import annotations

import asyncio
import json
import random
import threading
import time
from typing import Callable, Sequence

import requests
import websockets

from suspension_lab.config import LabConfig
from suspension_lab.kalshi_auth import load_private_key_from_config, ws_auth_headers
from suspension_lab.orderbook import OrderBook
from suspension_lab.rate_limit import DEFAULT_RETRY_AFTER_S, retry_after_seconds

BookCallback = Callable[[str, OrderBook], None]
StatusCallback = Callable[[str], None]

WS_BACKOFF_CAP_S = 30.0
REST_TICKER_GAP_S = 1.0
REST_CYCLE_MIN_S = 3.0


def orderbook_subscribe_payload(
    tickers: Sequence[str],
    *,
    msg_id: int,
    channels: Sequence[str] | None = None,
) -> dict | None:
    """Kalshi WS subscribe body, or None if market_tickers would be empty.

    Error 2 ("params required") is raised by Kalshi when orderbook_delta is
    subscribed without market_tickers. Never emit that payload.
    """
    markets = [t.strip() for t in tickers if t and str(t).strip()]
    if not markets:
        return None
    return {
        "id": msg_id,
        "cmd": "subscribe",
        "params": {
            "channels": list(channels or ["orderbook_delta"]),
            "market_tickers": markets,
        },
    }


def retry_after_from_exc(exc: BaseException) -> float | None:
    """Pull Retry-After off a WS/HTTP connect error when Kalshi sends one."""
    headers = None
    response = getattr(exc, "response", None)
    if response is not None:
        headers = getattr(response, "headers", None)
    if headers is None:
        headers = getattr(exc, "headers", None)
    if not headers:
        return None
    wait = retry_after_seconds(headers, default=0.0)
    return wait if wait >= 0.1 else None


class KalshiBookFeed:
    """Live L2 via WebSocket. REST is a one-shot subscribe snapshot, not a 200ms poll."""

    def __init__(
        self,
        config: LabConfig,
        on_book: BookCallback | None = None,
        on_status: StatusCallback | None = None,
    ) -> None:
        self.config = config
        self.on_book = on_book
        self.on_status = on_status
        self.books: dict[str, OrderBook] = {t: OrderBook(t) for t in config.tickers}
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._loop: asyncio.AbstractEventLoop | None = None
        self._ws_url_index = 0
        self._subscribe_id = 1
        self._pending_subscribe: list[str] = []
        self._pending_snapshots: list[str] = []
        self._snapshotted: set[str] = set()
        self._snap_lock = threading.Lock()
        self.rate_limit_until: float = 0.0
        self.last_book_monotonic: float = 0.0
        self.ws_connected: bool = False
        self.using_slow_rest: bool = False

    @property
    def thread_name(self) -> str:
        return "kalshi-book-feed"

    def add_ticker(self, ticker: str, *, snapshot: bool = True) -> bool:
        """Register a ticker. REST snapshot is --rest-only only; WS path subscribes."""
        ticker = ticker.strip()
        if not ticker or ticker in self.books:
            return False
        self.books[ticker] = OrderBook(ticker)
        if ticker not in self.config.tickers:
            self.config.tickers.append(ticker)
        self._pending_subscribe.append(ticker)
        if snapshot and not self.config.use_ws:
            self._queue_snapshot(ticker)
        self._emit_status(f"Added ticker {ticker}")
        return True

    def remove_ticker(self, ticker: str) -> bool:
        ticker = ticker.strip()
        if not ticker or ticker not in self.books:
            return False
        self.books.pop(ticker, None)
        if ticker in self.config.tickers:
            self.config.tickers.remove(ticker)
        self._pending_subscribe = [t for t in self._pending_subscribe if t != ticker]
        with self._snap_lock:
            self._pending_snapshots = [t for t in self._pending_snapshots if t != ticker]
            self._snapshotted.discard(ticker)
        self._emit_status(f"Dropped resolved ticker {ticker}")
        return True

    def pending_subscribes(self) -> list[str]:
        pending = [t for t in self._pending_subscribe if t and t.strip()]
        self._pending_subscribe.clear()
        return pending

    def _queue_snapshot(self, ticker: str) -> None:
        with self._snap_lock:
            if ticker in self._snapshotted or ticker in self._pending_snapshots:
                return
            self._pending_snapshots.append(ticker)

    def _pop_snapshot(self) -> str | None:
        with self._snap_lock:
            if not self._pending_snapshots:
                return None
            return self._pending_snapshots.pop(0)

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, name=self.thread_name, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=5)

    def get_book(self, ticker: str) -> OrderBook | None:
        return self.books.get(ticker)

    def snapshot_all(self) -> dict[str, dict]:
        return {t: b.top_levels() for t, b in self.books.items()}

    def _emit_status(self, msg: str) -> None:
        if self.on_status:
            self.on_status(msg)

    def _emit_book(self, ticker: str) -> None:
        self.last_book_monotonic = time.monotonic()
        if self.on_book:
            self.on_book(ticker, self.books[ticker])

    def _ws_urls(self) -> list[str]:
        if self.config.demo:
            return [
                "wss://external-api-ws.demo.kalshi.co/trade-api/ws/v2",
                "wss://demo-api.kalshi.co/trade-api/ws/v2",
            ]
        return [
            "wss://api.elections.kalshi.com/trade-api/ws/v2",
            "wss://external-api-ws.kalshi.com/trade-api/ws/v2",
        ]

    def _next_ws_url(self) -> str:
        urls = self._ws_urls()
        url = urls[self._ws_url_index % len(urls)]
        self._ws_url_index += 1
        return url

    def _run(self) -> None:
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        try:
            if self.config.use_ws and self.config.has_ws_auth:
                self._loop.run_until_complete(self._ws_loop())
            elif self.config.use_ws:
                self._emit_status("No WS creds - idle (WS-only L2, not polling REST)")
                while not self._stop.wait(1.0):
                    pass
            else:
                self._loop.run_until_complete(self._slow_rest_loop())
        finally:
            self.ws_connected = False
            self._loop.close()

    def _mark_rate_limit(self, wait: float) -> None:
        wait = max(wait, DEFAULT_RETRY_AFTER_S)
        self.rate_limit_until = max(self.rate_limit_until, time.monotonic() + wait)
        self._emit_status(f"REST 429 - cooling {wait:.0f}s (Retry-After)")

    def _cooldown_sleep(self) -> None:
        remain = self.rate_limit_until - time.monotonic()
        if remain > 0:
            time.sleep(remain)

    def _fetch_rest_snapshot(self, session: requests.Session, ticker: str) -> bool:
        """One-shot L2 REST. Never called in a parallel gather."""
        if ticker not in self.books:
            return False
        self._cooldown_sleep()
        try:
            session.headers.update({"User-Agent": "suspension-lab/0.1"})
            url = f"{self.config.rest_base}/markets/{ticker}/orderbook"
            resp = session.get(url, params={"depth": 0}, timeout=5)
            if resp.status_code == 429:
                wait = retry_after_seconds(resp.headers, default=DEFAULT_RETRY_AFTER_S)
                self._mark_rate_limit(wait)
                time.sleep(wait)
                return False
            resp.raise_for_status()
            payload = resp.json().get("orderbook_fp") or resp.json().get("orderbook") or {}
            now_ms = int(time.time() * 1000)
            self.books[ticker].load_snapshot(payload, updated_ms=now_ms)
            with self._snap_lock:
                self._snapshotted.add(ticker)
            self._emit_book(ticker)
            return True
        except Exception as exc:  # noqa: BLE001
            headers = getattr(getattr(exc, "response", None), "headers", None)
            if headers:
                wait = retry_after_from_exc(exc)
                if wait:
                    self._mark_rate_limit(wait)
            self._emit_status(f"REST {ticker}: {exc}")
            return False

    def _snapshot_once(self, session: requests.Session, ticker: str) -> bool:
        with self._snap_lock:
            if ticker in self._snapshotted:
                return True
        return self._fetch_rest_snapshot(session, ticker)

    def flush_one_snapshot(self, session: requests.Session | None = None) -> bool:
        ticker = self._pop_snapshot()
        if not ticker:
            return False
        http = session or requests.Session()
        http.headers.update({"User-Agent": "suspension-lab/0.1"})
        return self._snapshot_once(http, ticker)

    async def _slow_rest_loop(self) -> None:
        """Explicit --rest-only only. Never a WS fallback. One ticker, >=1s gap.

        Never fetch all books in parallel. Never poll at BOOK_SAMPLE_MS.
        """
        self.using_slow_rest = True
        self.ws_connected = False
        session = requests.Session()
        session.headers.update({"User-Agent": "suspension-lab/0.1"})
        self._emit_status(
            f"Slow REST snapshots ({REST_TICKER_GAP_S:.1f}s/ticker, "
            f"{REST_CYCLE_MIN_S:.0f}s/cycle) - not 200ms parallel"
        )
        while not self._stop.is_set():
            cycle_start = time.monotonic()
            tickers = list(self.config.tickers)
            if not tickers:
                await asyncio.sleep(REST_CYCLE_MIN_S)
                continue
            for ticker in tickers:
                if self._stop.is_set():
                    return
                await asyncio.to_thread(self._fetch_rest_snapshot, session, ticker)
                await asyncio.sleep(REST_TICKER_GAP_S)
            elapsed = time.monotonic() - cycle_start
            leftover = REST_CYCLE_MIN_S - elapsed
            if leftover > 0:
                await asyncio.sleep(leftover)

    def _snapshot_payload(self, msg: dict) -> dict:
        if "yes_dollars" in msg or "yes" in msg:
            return msg
        nested = msg.get("orderbook_fp") or msg.get("orderbook") or {}
        return nested if isinstance(nested, dict) else {}

    async def _ws_loop(self) -> None:
        private_key = load_private_key_from_config(self.config)
        attempt = 0

        while not self._stop.is_set():
            ws_url = self._next_ws_url()
            try:
                headers = ws_auth_headers(self.config.api_key_id, private_key)
                async with websockets.connect(
                    ws_url,
                    additional_headers=headers,
                    ping_interval=20,
                    ping_timeout=20,
                    close_timeout=5,
                    open_timeout=15,
                    max_size=8 * 1024 * 1024,
                ) as ws:
                    attempt = 0
                    self.ws_connected = True
                    self.using_slow_rest = False
                    host = ws_url.split("/")[2]
                    self._emit_status(f"Kalshi WS connected ({host})")

                    sub = orderbook_subscribe_payload(
                        self.config.tickers, msg_id=self._subscribe_id
                    )
                    self._subscribe_id += 1
                    if sub is None:
                        self._emit_status(
                            "Waiting for live soccer - no WS subscribe (empty market_tickers)"
                        )
                    else:
                        await ws.send(json.dumps(sub))

                    last_seq: int | None = None
                    last_emit_ms: dict[str, int] = {}
                    emit_gap_ms = 50

                    async def _flush_pending() -> None:
                        pending = self.pending_subscribes()
                        extra = orderbook_subscribe_payload(
                            pending, msg_id=self._subscribe_id + 1
                        )
                        if extra is None:
                            return
                        self._subscribe_id += 1
                        extra["id"] = self._subscribe_id
                        await ws.send(json.dumps(extra))
                        self._emit_status(f"WS subscribe added: {', '.join(pending)}")

                    while not self._stop.is_set():
                        try:
                            raw = await asyncio.wait_for(ws.recv(), timeout=2.0)
                        except TimeoutError:
                            await _flush_pending()
                            continue
                        event = json.loads(raw)
                        etype = event.get("type")
                        if etype == "error":
                            self._emit_status(f"WS error: {event.get('msg', event)}")
                            await _flush_pending()
                            continue
                        if etype == "subscribed":
                            self._emit_status(f"Subscribed: {event.get('msg', {}).get('channel')}")
                            await _flush_pending()
                            continue

                        msg = event.get("msg") or {}
                        ticker = msg.get("market_ticker")
                        if not ticker or ticker not in self.books:
                            await _flush_pending()
                            continue

                        seq = event.get("seq")
                        if seq is not None:
                            if last_seq is not None and seq != last_seq + 1:
                                self._emit_status(
                                    f"Seq gap ({last_seq}->{seq}) - waiting for WS snapshot"
                                )
                                last_seq = seq
                            else:
                                last_seq = seq

                        now_ms = int(time.time() * 1000)
                        book = self.books[ticker]
                        if etype == "orderbook_snapshot":
                            book.load_snapshot(self._snapshot_payload(msg), updated_ms=now_ms)
                        elif etype == "orderbook_delta":
                            book.apply_delta(msg, updated_ms=now_ms)
                        else:
                            await _flush_pending()
                            continue

                        if now_ms - last_emit_ms.get(ticker, 0) >= emit_gap_ms:
                            last_emit_ms[ticker] = now_ms
                            self._emit_book(ticker)

                        await _flush_pending()

            except Exception as exc:  # noqa: BLE001
                self.ws_connected = False
                if self._stop.is_set():
                    break
                retry_hdr = retry_after_from_exc(exc)
                if retry_hdr:
                    delay = min(max(retry_hdr, 1.0), WS_BACKOFF_CAP_S)
                    self._mark_rate_limit(retry_hdr)
                else:
                    delay = min(2**attempt, WS_BACKOFF_CAP_S)
                    delay = max(delay, 1.0) + random.uniform(0, 0.25)
                    attempt = min(attempt + 1, 8)
                self._emit_status(
                    f"WS disconnected ({exc}) - reconnect in {delay:.1f}s (no REST fallback)"
                )
                await asyncio.sleep(delay)
