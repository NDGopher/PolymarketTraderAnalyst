"""Shared paper-lab engine: one Kalshi client, seated-never-rediscover, WS L2.

Used by the Tk GUI and the headless paper logger.
Once CLI/session has tickers, discovery never runs again (no 60s /series+/markets).
Empty launch may discover until a book seats; then discovery stops.
"""

from __future__ import annotations

import queue
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable

from suspension_lab.config import BOOK_SAMPLE_MS, LabConfig
from suspension_lab.kalshi_client import KalshiBookFeed
from suspension_lab.soccer_discovery import (
    DiscoveryGate,
    DiscoveryResult,
    discover_soccer_games,
    format_discovery_log,
    needs_auto_discover,
    repick_session_totals,
)
from suspension_lab.tape_engine import TapeEngine, TapeEvent

ENGINE_THREAD_NAME = "lab-engine"
SAMPLE_THREAD_NAME = "lab-tape-sample"
DISCOVER_THREAD_NAME = "lab-discover"


@dataclass
class UiPaint:
    """Queued UI update. Tk must only consume these; never call Kalshi from Tk."""

    kind: str
    payload: dict[str, Any] = field(default_factory=dict)


class LabRuntime:
    """Owns the lock-protected Kalshi feed, tape, paper trader, and discovery."""

    def __init__(
        self,
        config: LabConfig,
        *,
        auto_discover: bool = True,
        max_games: int = 5,
        min_volume: float = 50.0,
        rediscover_seconds: float = 30.0,
        on_status: Callable[[str], None] | None = None,
    ) -> None:
        self.config = config
        self.auto_discover = auto_discover
        self.max_games = max_games
        self.min_volume = min_volume
        self.rediscover_seconds = max(float(rediscover_seconds), 1.0)
        self._external_status = on_status

        ts = datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S")
        slug = (config.game_label or "soccer-paper").replace(" ", "_")[:40]
        session_dir = config.output_dir / f"{ts}_{slug}"
        paper_on = bool(config.paper_enabled or True)
        self.engine = TapeEngine.create(
            session_dir,
            list(config.tickers),
            game_label=config.game_label,
            games=list(getattr(config, "games", []) or []),
            rest_base=config.rest_base,
            paper_enabled=paper_on,
        )
        self.engine.on_event = self._on_tape_event
        self.feed = KalshiBookFeed(
            config,
            on_book=self._on_book,
            on_status=self._on_feed_status,
            on_note=self.engine.logger.append_note,
        )
        self.engine.logger.bind_book_provider(self.books_for_log)
        self.gate = DiscoveryGate()
        if config.tickers or getattr(config, "games", None):
            seated = DiscoveryResult(
                games=list(getattr(config, "games", []) or []),
                tickers=list(config.tickers),
                log_lines=["seeded from launch"],
            )
            self.gate.store(seated)

        self._stop = threading.Event()
        self._book_q: queue.Queue[tuple[str, Any] | None] = queue.Queue()
        self.ui_q: queue.Queue[UiPaint] = queue.Queue()
        self._engine_thread: threading.Thread | None = None
        self._sample_thread: threading.Thread | None = None
        self._discover_thread: threading.Thread | None = None
        self._started = time.monotonic()
        self._last_discover = 0.0
        self.last_status = "Starting paper lab"

    @property
    def trader(self):
        return self.engine.trader

    @property
    def logger(self):
        return self.engine.logger

    def books_for_log(self) -> dict[str, dict]:
        out: dict[str, dict] = {}
        for ticker, book in self.feed.books.items():
            levels = book.top_levels()
            levels["book_json"] = book.full_json()
            out[ticker] = levels
        return out

    def _on_book(self, ticker: str, book) -> None:
        self._book_q.put(("book", (ticker, book)))

    def _on_feed_status(self, msg: str) -> None:
        self.last_status = msg
        self._push_ui("status", {"text": msg})
        if self._external_status:
            self._external_status(msg)

    def _on_tape_event(self, event: TapeEvent) -> None:
        self._push_ui("event", {"event": event})

    def _push_ui(self, kind: str, payload: dict[str, Any] | None = None) -> None:
        self.ui_q.put(UiPaint(kind, payload or {}))

    def drain_ui(self, limit: int = 200) -> list[UiPaint]:
        items: list[UiPaint] = []
        while len(items) < limit:
            try:
                items.append(self.ui_q.get_nowait())
            except queue.Empty:
                break
        return items

    def request_add_tickers(self, tickers: list[str]) -> None:
        self._book_q.put(("add", [t.strip() for t in tickers if t and t.strip()]))

    def request_discover(self, *, force: bool = False) -> None:
        self._book_q.put(("discover", force))

    def session_tickers(self) -> list[str]:
        """Tickers already pinned on the CLI or seated in this session."""
        seen: list[str] = []
        for ticker in list(self.config.tickers) + list(self.feed.books):
            text = (ticker or "").strip()
            if text and text not in seen:
                seen.append(text)
        for game in list(self.engine.games):
            for ticker in game.get_tickers():
                text = (ticker or "").strip()
                if text and text not in seen:
                    seen.append(text)
        return seen

    def has_known_markets(self) -> bool:
        """Real KX pins or seated books. That is enough; do not rediscover."""
        tickers = self.session_tickers()
        return bool(tickers) and not needs_auto_discover(tickers)

    def start(self) -> None:
        if self._engine_thread and self._engine_thread.is_alive():
            return
        self._stop.clear()
        self.feed.start()
        self._engine_thread = threading.Thread(
            target=self._engine_loop, name=ENGINE_THREAD_NAME, daemon=True
        )
        self._sample_thread = threading.Thread(
            target=self._sample_loop, name=SAMPLE_THREAD_NAME, daemon=True
        )
        self._discover_thread = threading.Thread(
            target=self._discover_loop, name=DISCOVER_THREAD_NAME, daemon=True
        )
        self._engine_thread.start()
        self._sample_thread.start()
        self._discover_thread.start()
        if self.has_known_markets():
            self._on_feed_status(
                "Known markets pinned - WS only, no /series+/markets rediscover"
            )
        elif self.auto_discover:
            self.request_discover(force=True)

    def stop(self) -> None:
        self._stop.set()
        self._book_q.put(None)
        self.feed.stop()
        for thread in (self._engine_thread, self._sample_thread, self._discover_thread):
            if thread is not None:
                thread.join(timeout=5)

    def _engine_loop(self) -> None:
        while not self._stop.is_set():
            try:
                item = self._book_q.get(timeout=0.2)
            except queue.Empty:
                continue
            if item is None:
                break
            kind, payload = item
            if kind == "book":
                ticker, book = payload
                self.engine.handle_book(ticker, book)
                self._push_ui("book", {"ticker": ticker, "levels": book.top_levels()})
            elif kind == "add":
                self._add_tickers(payload)
            elif kind == "discover":
                self._run_discover(force=bool(payload))

    def _add_tickers(self, tickers: list[str]) -> None:
        added: list[str] = []
        for ticker in tickers:
            if self.feed.add_ticker(ticker):
                self.engine.logger.register_ticker(ticker)
                self.engine.labels.register_ticker(ticker)
                added.append(ticker)
        if added:
            self._push_ui("tickers_added", {"tickers": added})

    def _run_discover(self, *, force: bool = False) -> None:
        if self.has_known_markets():
            self._on_feed_status(
                "Known markets already seated - skip /series+/markets (no AUTO-FUND)"
            )
            self._push_ui("discover_skipped", {"reason": "known_markets"})
            return
        if self.gate.cooldown_remaining() > 0 and not force:
            remain = self.gate.cooldown_remaining()
            self._on_feed_status(f"429 cooldown {remain:.0f}s - keeping seated books")
            self._push_ui("discover_skipped", {"reason": "429", "retry_after": remain})
            return
        allowed, cached = self.gate.allow(force=force)
        if not allowed:
            self._push_ui(
                "discover_skipped",
                {"reason": "interval", "cached_tickers": list(cached.tickers) if cached else []},
            )
            return
        try:
            result = discover_soccer_games(
                rest_base=self.config.rest_base,
                min_volume=self.min_volume,
                max_games=self.max_games,
                gate=self.gate,
                force=force,
            )
        except Exception as exc:  # noqa: BLE001
            self._on_feed_status(f"Discover failed: {exc}")
            return
        self._last_discover = time.monotonic()
        seated = list(self.engine.games)
        seated_tickers = [t for g in seated for t in g.get_tickers()] or list(self.config.tickers)
        if result.rate_limited:
            self._on_feed_status(
                f"429 - keeping seated books ({len(seated_tickers)} tickers), "
                f"Retry-After {result.retry_after:.0f}s"
            )
            if not result.games and seated:
                return
        if result.from_cache and result.rate_limited and not result.games and seated:
            return
        recent_goal = any(e.kind == "GOAL" for e in self.engine.events[-12:])
        grind_ready = (time.monotonic() - self._started) >= 15 * 60 and not recent_goal
        kept, fund, drop = repick_session_totals(
            seated or list(result.games),
            list(result.games),
            drop_far_wing=grind_ready,
        )
        for ticker in drop:
            self.feed.remove_ticker(ticker)
        added = 0
        seen: set[str] = set()
        for ticker in list(result.tickers) + fund:
            if not ticker or ticker in seen:
                continue
            seen.add(ticker)
            if self.feed.add_ticker(ticker):
                self.engine.logger.register_ticker(ticker)
                self.engine.labels.register_ticker(ticker)
                added += 1
        self.engine.games[:] = kept
        if not self.config.game_label and kept:
            self.config.game_label = " | ".join(g.title[:28] for g in kept[:2])
        self._push_ui(
            "discover",
            {
                "result": result,
                "kept": kept,
                "fund": fund,
                "drop": drop,
                "added": added,
                "log": format_discovery_log(result),
            },
        )

    def _discover_loop(self) -> None:
        # Do not reschedule 30s/60s /series+/markets. start() may one-shot
        # empty seats after Tk exists. Seated never scans. has_known_markets
        # stays the bail condition if a caller queues discover anyway.
        while not self._stop.wait(1.0):
            if self.has_known_markets():
                continue

    def _sample_loop(self) -> None:
        interval = max(self.config.poll_ms, BOOK_SAMPLE_MS, 100) / 1000.0
        while not self._stop.wait(interval):
            books = self.books_for_log()
            if books:
                self.engine.logger.log_book_sample(books)

    def wait_until_stopped(self, *, duration_seconds: float = 0) -> None:
        started = time.time()
        while not self._stop.is_set():
            if duration_seconds > 0 and (time.time() - started) >= duration_seconds:
                break
            time.sleep(0.25)


def build_runtime(
    config: LabConfig,
    *,
    auto_discover: bool = True,
    max_games: int = 5,
    min_volume: float = 50.0,
    on_status: Callable[[str], None] | None = None,
) -> LabRuntime:
    return LabRuntime(
        config,
        auto_discover=auto_discover,
        max_games=max_games,
        min_volume=min_volume,
        on_status=on_status,
    )
