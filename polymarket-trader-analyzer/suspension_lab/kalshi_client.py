from __future__ import annotations

import asyncio
import json
import random
import threading
import time
from typing import Callable

import requests
import websockets
from websockets.exceptions import ConnectionClosed

from suspension_lab.config import LabConfig, WS_PATH
from suspension_lab.kalshi_auth import load_private_key_from_config, ws_auth_headers
from suspension_lab.orderbook import OrderBook

BookCallback = Callable[[str, OrderBook], None]
StatusCallback = Callable[[str], None]

WS_FAILS_BEFORE_REST = 4


class KalshiBookFeed:
    """Maintains live Kalshi orderbooks via WebSocket (preferred) or REST polling."""

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

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, name="kalshi-book-feed", daemon=True)
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
            else:
                if self.config.use_ws and not self.config.has_ws_auth:
                    self._emit_status("No WS creds — using REST polling")
                self._loop.run_until_complete(self._rest_loop())
        finally:
            self._loop.close()

    def _fetch_rest_snapshot(self, session: requests.Session, ticker: str) -> bool:
        try:
            url = f"{self.config.rest_base}/markets/{ticker}/orderbook"
            resp = session.get(url, params={"depth": 0}, timeout=5)
            resp.raise_for_status()
            payload = resp.json().get("orderbook_fp") or resp.json().get("orderbook") or {}
            now_ms = int(time.time() * 1000)
            self.books[ticker].load_snapshot(payload, updated_ms=now_ms)
            self._emit_book(ticker)
            return True
        except Exception as exc:  # noqa: BLE001
            self._emit_status(f"REST {ticker}: {exc}")
            return False

    async def _rest_loop(self) -> None:
        session = requests.Session()
        session.headers.update({"User-Agent": "suspension-lab/0.1"})
        interval = max(self.config.poll_ms, 100) / 1000.0
        self._emit_status(f"REST polling every {int(interval * 1000)}ms")
        while not self._stop.is_set():
            for ticker in self.config.tickers:
                if self._stop.is_set():
                    break
                await asyncio.to_thread(self._fetch_rest_snapshot, session, ticker)
            await asyncio.sleep(interval)

    def _snapshot_payload(self, msg: dict) -> dict:
        if "yes_dollars" in msg or "yes" in msg:
            return msg
        nested = msg.get("orderbook_fp") or msg.get("orderbook") or {}
        return nested if isinstance(nested, dict) else {}

    async def _ws_loop(self) -> None:
        private_key = load_private_key_from_config(self.config)
        session = requests.Session()
        session.headers.update({"User-Agent": "suspension-lab/0.1"})
        attempt = 0
        ws_failures = 0

        while not self._stop.is_set():
            if ws_failures >= WS_FAILS_BEFORE_REST:
                self._emit_status("WS unstable — switching to REST polling (still works for lab)")
                await self._rest_loop()
                return

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
                    ws_failures = 0
                    host = ws_url.split("/")[2]
                    self._emit_status(f"Kalshi WS connected ({host})")

                    # Seed books via REST so UI has data even before snapshots arrive
                    for ticker in self.config.tickers:
                        await asyncio.to_thread(self._fetch_rest_snapshot, session, ticker)

                    sub = {
                        "id": 1,
                        "cmd": "subscribe",
                        "params": {
                            "channels": ["orderbook_delta"],
                            "market_tickers": self.config.tickers,
                        },
                    }
                    await ws.send(json.dumps(sub))

                    # Kalshi seq is per subscription stream (sid), NOT per ticker
                    last_seq: int | None = None
                    last_emit_ms: dict[str, int] = {t: 0 for t in self.config.tickers}
                    emit_gap_ms = 50

                    async for raw in ws:
                        if self._stop.is_set():
                            break
                        event = json.loads(raw)
                        etype = event.get("type")
                        if etype == "error":
                            self._emit_status(f"WS error: {event.get('msg', event)}")
                            continue
                        if etype == "subscribed":
                            self._emit_status(f"Subscribed: {event.get('msg', {}).get('channel')}")
                            continue

                        msg = event.get("msg") or {}
                        ticker = msg.get("market_ticker")
                        if not ticker or ticker not in self.books:
                            continue

                        seq = event.get("seq")
                        if seq is not None:
                            if last_seq is not None and seq != last_seq + 1:
                                self._emit_status(f"Seq gap ({last_seq}->{seq}) — refreshing books")
                                for t in self.config.tickers:
                                    await asyncio.to_thread(self._fetch_rest_snapshot, session, t)
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
                            continue

                        if now_ms - last_emit_ms[ticker] >= emit_gap_ms:
                            last_emit_ms[ticker] = now_ms
                            self._emit_book(ticker)

            except Exception as exc:  # noqa: BLE001
                if self._stop.is_set():
                    break
                ws_failures += 1
                attempt = min(attempt + 1, 6)
                delay = min(0.5 * (2**attempt), 15) + random.uniform(0, 0.25)
                self._emit_status(
                    f"WS disconnected ({exc}) — retry {ws_failures}/{WS_FAILS_BEFORE_REST} in {delay:.1f}s"
                )
                await asyncio.sleep(delay)
