from __future__ import annotations

import csv
import json
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from suspension_lab.config import MARKOUT_SECONDS


def _now_ms() -> int:
    return int(time.time() * 1000)


def _iso(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).isoformat()


@dataclass
class BookFlags:
    b365: str = "UP"
    fanduel: str = "UP"
    draftkings: str = "UP"


@dataclass
class SessionLogger:
    session_dir: Path
    tickers: list[str]
    game_label: str = ""
    flags: BookFlags = field(default_factory=BookFlags)
    _event_id: int = 0
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)
    _get_books: Any = None

    def __post_init__(self) -> None:
        self.session_dir.mkdir(parents=True, exist_ok=True)
        meta = {
            "game_label": self.game_label,
            "tickers": self.tickers,
            "started_at": _iso(_now_ms()),
            "markout_seconds": list(MARKOUT_SECONDS),
        }
        (self.session_dir / "session.json").write_text(json.dumps(meta, indent=2))
        self._events_path = self.session_dir / "events.csv"
        self._books_path = self.session_dir / "books.csv"
        self._init_csv(self._events_path, self._event_headers())
        self._init_csv(self._books_path, self._book_headers())

    def bind_book_provider(self, fn) -> None:
        self._get_books = fn

    def _init_csv(self, path: Path, headers: list[str]) -> None:
        if not path.exists():
            with path.open("w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(headers)

    def _ticker_cols(self) -> list[str]:
        return [
            "yes_bid",
            "yes_ask",
            "yes_mid",
            "spread",
            "spread_cents",
            "yes_bid_qty",
            "yes_ask_qty",
            "bid_depth_3",
            "ask_depth_3",
            "tight_spread",
            "wide_spread",
            "untradeable",
            "suggested_bid_plus_2c",
            "is_bond",
            "book_json",
        ]

    def _event_headers(self) -> list[str]:
        cols = [
            "event_id",
            "event_ts_ms",
            "event_ts_iso",
            "event_type",
            "b365_state",
            "fd_state",
            "dk_state",
        ]
        for t in self.tickers:
            safe = t.replace(",", "_")
            for col in self._ticker_cols():
                cols.append(f"{safe}_{col}")
        for sec in MARKOUT_SECONDS:
            for t in self.tickers:
                safe = t.replace(",", "_")
                cols.extend(
                    [
                        f"{safe}_mid_{sec}s",
                        f"{safe}_spread_cents_{sec}s",
                    ]
                )
        return cols

    def _book_headers(self) -> list[str]:
        cols = ["ts_ms", "ts_iso"]
        for t in self.tickers:
            safe = t.replace(",", "_")
            for col in (
                "yes_bid",
                "yes_ask",
                "yes_mid",
                "spread_cents",
                "yes_bid_qty",
                "yes_ask_qty",
                "tight_spread",
                "wide_spread",
                "untradeable",
            ):
                cols.append(f"{safe}_{col}")
        cols.extend(["b365_state", "fd_state", "dk_state"])
        return cols

    def _book_row_values(self, b: dict) -> list[Any]:
        return [
            b.get("yes_bid", ""),
            b.get("yes_ask", ""),
            b.get("yes_mid", ""),
            b.get("spread_cents", ""),
            b.get("yes_bid_qty", ""),
            b.get("yes_ask_qty", ""),
            b.get("tight_spread", ""),
            b.get("wide_spread", ""),
            b.get("untradeable", ""),
        ]

    def log_book_sample(self, books: dict[str, dict]) -> None:
        row = [_now_ms(), _iso(_now_ms())]
        for t in self.tickers:
            row.extend(self._book_row_values(books.get(t, {})))
        row.extend([self.flags.b365, self.flags.fanduel, self.flags.draftkings])
        with self._lock:
            with self._books_path.open("a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(row)

    def toggle_book(self, book: str) -> str:
        mapping = {
            "b365": "b365",
            "b": "b365",
            "fanduel": "fanduel",
            "f": "fanduel",
            "fd": "fanduel",
            "dk": "draftkings",
            "draftkings": "draftkings",
        }
        key = mapping.get(book.lower())
        if not key:
            raise ValueError(f"Unknown book: {book}")

        attr = {"b365": "b365", "fanduel": "fanduel", "draftkings": "draftkings"}[key]
        current = getattr(self.flags, attr)
        new_state = "DOWN" if current == "UP" else "UP"
        setattr(self.flags, attr, new_state)
        event_type = f"{attr.upper()}_{new_state}"
        self.log_event(event_type)
        return event_type

    def log_event(self, event_type: str, *, extra_books: dict[str, dict] | None = None) -> int:
        books = extra_books or (self._get_books() if self._get_books else {})
        ts = _now_ms()
        with self._lock:
            self._event_id += 1
            eid = self._event_id

        row: list[Any] = [
            eid,
            ts,
            _iso(ts),
            event_type,
            self.flags.b365,
            self.flags.fanduel,
            self.flags.draftkings,
        ]
        for t in self.tickers:
            b = books.get(t, {})
            row.extend([b.get(col, "") for col in self._ticker_cols()[:-1]])
            row.append(b.get("book_json", json.dumps(b, separators=(",", ":"))))
        for _ in MARKOUT_SECONDS:
            for _t in self.tickers:
                row.extend(["", ""])

        with self._lock:
            with self._events_path.open("a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(row)

        threading.Thread(
            target=self._fill_markouts,
            args=(eid, ts, books),
            daemon=True,
            name=f"markout-{eid}",
        ).start()
        return eid

    def _fill_markouts(self, event_id: int, event_ts: int, baseline: dict[str, dict]) -> None:
        snapshots: dict[int, dict[str, dict]] = {}
        for sec in MARKOUT_SECONDS:
            target = event_ts + sec * 1000
            delay = max(0, (target - _now_ms()) / 1000.0)
            time.sleep(delay)
            if self._get_books:
                snapshots[sec] = self._get_books()
            else:
                snapshots[sec] = baseline

        rows: list[list[Any]] = []
        with self._events_path.open("r", newline="", encoding="utf-8") as f:
            rows = list(csv.reader(f))
        if event_id >= len(rows):
            return

        header = rows[0]
        row = rows[event_id]
        idx = 7 + len(self.tickers) * len(self._ticker_cols())
        for sec in MARKOUT_SECONDS:
            snap = snapshots.get(sec, {})
            for t in self.tickers:
                b = snap.get(t, {})
                if idx + 1 < len(row):
                    row[idx] = b.get("yes_mid", "")
                    row[idx + 1] = b.get("spread_cents", "")
                idx += 2

        with self._lock:
            with self._events_path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(rows)
