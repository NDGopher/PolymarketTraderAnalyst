from __future__ import annotations

import csv
import json
import shutil
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _now_ms() -> int:
    return int(time.time() * 1000)


def _iso(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).isoformat()


@dataclass
class SessionLogger:
    session_dir: Path
    tickers: list[str]
    game_label: str = ""
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)
    _get_books: Any = None
    _note_count: int = 0

    def __post_init__(self) -> None:
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self._initial_tickers = list(self.tickers)
        meta = {
            "game_label": self.game_label,
            "tickers": self.tickers,
            "started_at": _iso(_now_ms()),
        }
        (self.session_dir / "session.json").write_text(json.dumps(meta, indent=2))
        self._books_path = self.session_dir / "books.csv"
        self._init_csv(self._books_path, self._book_headers())
        self._signals_path = self.session_dir / "goal_signals.csv"
        self._init_csv(
            self._signals_path,
            [
                "signal_id",
                "signal_ts_ms",
                "signal_ts_iso",
                "ticker",
                "market_label",
                "prev_bid",
                "new_bid",
                "bid_jump_cents",
                "bid_qty",
                "prev_ask",
                "new_ask",
                "reason",
                "exit_mode",
            ],
        )
        self._signal_id = 0
        self._books_long_path = self.session_dir / "books_long.csv"
        self._init_csv(
            self._books_long_path,
            [
                "ts_ms",
                "ts_iso",
                "ticker",
                "yes_bid",
                "yes_ask",
                "yes_mid",
                "no_bid",
                "no_ask",
                "spread_cents",
                "yes_bid_qty",
                "yes_ask_qty",
                "no_bid_qty",
                "tight_spread",
                "wide_spread",
                "untradeable",
            ],
        )
        self._notes_path = self.session_dir / "notes.txt"
        if not self._notes_path.exists():
            self._notes_path.write_text("", encoding="utf-8")
        self._ticker_added_at: dict[str, str] = {}

    def bind_book_provider(self, fn) -> None:
        self._get_books = fn

    def _init_csv(self, path: Path, headers: list[str]) -> None:
        if not path.exists():
            with path.open("w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(headers)

    def _book_headers(self) -> list[str]:
        cols = ["ts_ms", "ts_iso"]
        for t in self.tickers:
            safe = t.replace(",", "_")
            for col in (
                "yes_bid",
                "yes_ask",
                "yes_mid",
                "no_bid",
                "no_ask",
                "spread_cents",
                "yes_bid_qty",
                "yes_ask_qty",
                "no_bid_qty",
                "tight_spread",
                "wide_spread",
                "untradeable",
            ):
                cols.append(f"{safe}_{col}")
        return cols

    def _book_row_values(self, b: dict) -> list[Any]:
        return [
            b.get("yes_bid", ""),
            b.get("yes_ask", ""),
            b.get("yes_mid", ""),
            b.get("no_bid", ""),
            b.get("no_ask", ""),
            b.get("spread_cents", ""),
            b.get("yes_bid_qty", ""),
            b.get("yes_ask_qty", ""),
            b.get("no_bid_qty", ""),
            b.get("tight_spread", ""),
            b.get("wide_spread", ""),
            b.get("untradeable", ""),
        ]

    def log_book_sample(self, books: dict[str, dict]) -> None:
        ts = _now_ms()
        iso = _iso(ts)
        row = [ts, iso]
        for t in self._initial_tickers:
            row.extend(self._book_row_values(books.get(t, {})))
        long_rows: list[list[Any]] = []
        for ticker, b in books.items():
            long_rows.append(
                [
                    ts,
                    iso,
                    ticker,
                    b.get("yes_bid", ""),
                    b.get("yes_ask", ""),
                    b.get("yes_mid", ""),
                    b.get("no_bid", ""),
                    b.get("no_ask", ""),
                    b.get("spread_cents", ""),
                    b.get("yes_bid_qty", ""),
                    b.get("yes_ask_qty", ""),
                    b.get("no_bid_qty", ""),
                    b.get("tight_spread", ""),
                    b.get("wide_spread", ""),
                    b.get("untradeable", ""),
                ]
            )
        with self._lock:
            with self._books_path.open("a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(row)
            if long_rows:
                with self._books_long_path.open("a", newline="", encoding="utf-8") as f:
                    csv.writer(f).writerows(long_rows)

    def register_ticker(self, ticker: str) -> None:
        if ticker in self.tickers:
            return
        with self._lock:
            if ticker not in self.tickers:
                self.tickers.append(ticker)
            self._ticker_added_at[ticker] = _iso(_now_ms())
            meta_path = self.session_dir / "session.json"
            meta: dict[str, Any] = {}
            if meta_path.exists():
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
            meta["tickers"] = list(self.tickers)
            additions = meta.get("tickers_added_late", [])
            additions.append({"ticker": ticker, "added_at": self._ticker_added_at[ticker]})
            meta["tickers_added_late"] = additions
            meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    def append_note(self, text: str) -> str:
        """Append a timestamped note line. Returns the formatted line."""
        stripped = text.strip()
        if not stripped:
            return ""
        ts = _now_ms()
        line = f"[{_iso(ts)}] {stripped}"
        with self._lock:
            with self._notes_path.open("a", encoding="utf-8") as f:
                f.write(line + "\n")
            self._note_count += 1
        return line

    def save_notes_full(self, full_text: str) -> None:
        """Overwrite notes.txt with the full notes pad content on session close."""
        with self._lock:
            self._notes_path.write_text(full_text.rstrip() + "\n", encoding="utf-8")

    def log_goal_signal(
        self,
        *,
        ticker: str,
        market_label: str,
        prev_bid: str,
        new_bid: str,
        bid_jump_cents: int,
        bid_qty: str,
        prev_ask: str,
        new_ask: str,
        reason: str,
        exit_mode: str = "",
        ts_ms: int | None = None,
    ) -> int:
        ts = ts_ms if ts_ms is not None else _now_ms()
        with self._lock:
            self._signal_id += 1
            sid = self._signal_id
        row = [
            sid,
            ts,
            _iso(ts),
            ticker,
            market_label,
            prev_bid,
            new_bid,
            bid_jump_cents,
            bid_qty,
            prev_ask,
            new_ask,
            reason,
            exit_mode,
        ]
        with self._lock:
            with self._signals_path.open("a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(row)
        return sid

    @property
    def note_count(self) -> int:
        return self._note_count

    def finalize(self, *, saved: bool, notes_text: str = "") -> None:
        if notes_text:
            self.save_notes_full(notes_text)
        meta_path = self.session_dir / "session.json"
        meta: dict[str, Any] = {}
        if meta_path.exists():
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        meta["ended_at"] = _iso(_now_ms())
        meta["saved"] = saved
        meta["note_count"] = self.note_count
        meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    def delete_session(self) -> None:
        if self.session_dir.exists():
            shutil.rmtree(self.session_dir)
