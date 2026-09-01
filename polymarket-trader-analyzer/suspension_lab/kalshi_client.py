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

from suspension_lab.config import LabConfig
from suspension_lab.kalshi_auth import load_private_key_from_config, ws_auth_headers
from suspension_lab.orderbook import OrderBook


BookCallback = Callable[[str, OrderBook], None]
StatusCallback = Callable[[str], None]


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

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, name="kalshi-book-feed", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._loop and self._loop.is_running():
            self._loop.call_soon_threadsafe(lambda: None)
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

    def _run(self) -> None:
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        try:
            if self.config.use_ws and self.config.has_ws_auth:
                self._loop.run_until_complete(self._ws_loop())
            else:
                if self.config.use_ws and not self.config.has_ws_auth:
                    self._emit_status("No WS creds — falling back to REST polling")
                self._loop.run_until_complete(self._rest_loop())
        finally:
            self._loop.close()

    async def _rest_loop(self) -> None:
        session = requests.Session()
        session.headers.update({"User-Agent": "suspension-lab/0.1"})
        interval = max(self.config.poll_ms, 100) / 1000.0
        while not self._stop.is_set():
            for ticker in self.config.tickers:
                try:
                    url = f"{self.config.rest_base}/markets/{ticker}/orderbook"
                    resp = session.get(url, params={"depth": 0}, timeout=5)
                    resp.raise_for_status()
                    payload = resp.json().get("orderbook_fp") or resp.json().get("orderbook") or {}
                    now_ms = int(time.time() * 1000)
                    self.books[ticker].load_snapshot(payload, updated_ms=now_ms)
                    self._emit_book(ticker)
                except Exception as exc:  # noqa: BLE001
                    self._emit_status(f"REST {ticker}: {exc}")
            await asyncio.sleep(interval)

    async def _ws_loop(self) -> None:
        private_key = load_private_key_from_config(self.config)
        attempt = 0
        while not self._stop.is_set():
            try:
                headers = ws_auth_headers(self.config.api_key_id, private_key)
                async with websockets.connect(
                    self.config.ws_url,
                    additional_headers=headers,
                    ping_interval=20,
                    ping_timeout=10,
                    close_timeout=5,
                ) as ws:
                    attempt = 0
                    self._emit_status("Kalshi WS connected")
                    sub = {
                        "id": 1,
                        "cmd": "subscribe",
                        "params": {
                            "channels": ["orderbook_delta"],
                            "market_tickers": self.config.tickers,
                        },
                    }
                    await ws.send(json.dumps(sub))
                    last_seq: dict[str, int | None] = {t: None for t in self.config.tickers}

                    async for raw in ws:
                        if self._stop.is_set():
                            break
                        event = json.loads(raw)
                        etype = event.get("type")
                        if etype == "error":
                            self._emit_status(f"WS error: {event}")
                            continue
                        if etype == "subscribed":
                            self._emit_status(f"Subscribed: {event.get('msg', {}).get('channel')}")
                            continue
                        msg = event.get("msg") or {}
                        ticker = msg.get("market_ticker")
                        if not ticker or ticker not in self.books:
                            continue
                        now_ms = int(time.time() * 1000)
                        book = self.books[ticker]
                        seq = event.get("seq")
                        if etype == "orderbook_snapshot":
                            book.load_snapshot(msg, updated_ms=now_ms)
                            last_seq[ticker] = seq
                            self._emit_book(ticker)
                        elif etype == "orderbook_delta":
                            prev = last_seq.get(ticker)
                            if prev is not None and seq is not None and seq != prev + 1:
                                self._emit_status(f"Seq gap on {ticker} — resync needed")
                                raise ConnectionClosed(None, None)
                            book.apply_delta(msg, updated_ms=now_ms)
                            last_seq[ticker] = seq
                            self._emit_book(ticker)
            except Exception as exc:  # noqa: BLE001
                if self._stop.is_set():
                    break
                delay = min(0.5 * (2**attempt), 30) + random.uniform(0, 0.25)
                self._emit_status(f"WS disconnected ({exc}) — retry in {delay:.1f}s")
                await asyncio.sleep(delay)
                attempt = min(attempt + 1, 6)
