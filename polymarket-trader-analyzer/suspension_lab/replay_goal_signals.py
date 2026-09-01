"""Replay goal-signal detector against a saved session books.csv."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

from suspension_lab.goal_signal import GoalSignal, GoalSignalDetector, SpoofBidNotice, VarRevertAlert
from suspension_lab.orderbook import OrderBook


@dataclass
class ReplayEvent:
    ts_iso: str
    ticker: str
    kind: str
    detail: str


def _ticker_prefixes(headers: list[str]) -> list[str]:
    return [h[: -len("_yes_bid")] for h in headers if h.endswith("_yes_bid")]


def _replay_from_wide(session_dir: Path, tickers: list[str]) -> list[ReplayEvent]:
    books_path = session_dir / "books.csv"
    with books_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        prefixes = _ticker_prefixes(headers) or [t.replace(",", "_") for t in tickers]
        rows = list(reader)

    detectors: dict[str, GoalSignalDetector] = {p: GoalSignalDetector() for p in prefixes}
    events: list[ReplayEvent] = []

    for row in rows:
        ts_ms = int(row["ts_ms"])
        ts_iso = row["ts_iso"]
        for prefix in prefixes:
            bid = row.get(f"{prefix}_yes_bid", "")
            ask = row.get(f"{prefix}_yes_ask", "")
            if not bid or not ask:
                continue
            book = OrderBook(prefix)
            book.set_from_top(
                bid=bid,
                ask=ask,
                bid_qty=row.get(f"{prefix}_yes_bid_qty", "0") or "0",
                ask_qty=row.get(f"{prefix}_yes_ask_qty", "0") or "0",
                updated_ms=ts_ms,
            )
            events.extend(_collect_event(detectors[prefix].evaluate(prefix, book), ts_iso, prefix))
    return events


def _replay_from_long(session_dir: Path) -> list[ReplayEvent]:
    long_path = session_dir / "books_long.csv"
    with long_path.open(encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r.get("yes_bid") and r.get("yes_ask")]

    tickers = sorted({r["ticker"] for r in rows})
    detectors: dict[str, GoalSignalDetector] = {t: GoalSignalDetector() for t in tickers}
    events: list[ReplayEvent] = []

    for row in rows:
        ticker = row["ticker"]
        ts_ms = int(row["ts_ms"])
        book = OrderBook(ticker)
        book.set_from_top(
            bid=row["yes_bid"],
            ask=row["yes_ask"],
            bid_qty=row.get("yes_bid_qty", "0") or "0",
            ask_qty=row.get("yes_ask_qty", "0") or "0",
            updated_ms=ts_ms,
        )
        events.extend(_collect_event(detectors[ticker].evaluate(ticker, book), row["ts_iso"], ticker))
    return events


def _collect_event(result, ts_iso: str, ticker: str) -> list[ReplayEvent]:
    if isinstance(result, GoalSignal):
        return [ReplayEvent(ts_iso=ts_iso, ticker=ticker, kind="GOAL", detail=result.summary)]
    if isinstance(result, VarRevertAlert):
        return [
            ReplayEvent(
                ts_iso=ts_iso,
                ticker=ticker,
                kind="VAR",
                detail=(
                    f"peak {result.peak_bid:.2f} -> {result.current_bid:.2f} "
                    f"(-{result.drop_cents}c in {result.seconds_since_signal:.0f}s)"
                ),
            )
        ]
    if isinstance(result, SpoofBidNotice):
        return [
            ReplayEvent(
                ts_iso=ts_iso,
                ticker=ticker,
                kind="SPOOF",
                detail=(
                    f"bid {result.current_bid:.2f} x{result.bid_qty:.0f} "
                    f"ask {result.current_ask:.2f} (-{result.drop_cents}c from peak, bonded)"
                ),
            )
        ]
    return []


def replay_session(session_dir: Path) -> list[ReplayEvent]:
    long_path = session_dir / "books_long.csv"
    if long_path.exists():
        return _replay_from_long(session_dir)

    books_path = session_dir / "books.csv"
    if not books_path.exists():
        raise FileNotFoundError(f"No books.csv or books_long.csv in {session_dir}")

    meta_path = session_dir / "session.json"
    tickers: list[str] = []
    if meta_path.exists():
        tickers = json.loads(meta_path.read_text(encoding="utf-8")).get("tickers", [])
    return _replay_from_wide(session_dir, tickers)


def print_replay(session_dir: Path) -> None:
    for ev in replay_session(session_dir):
        print(f"{ev.ts_iso} [{ev.kind}] {ev.ticker}: {ev.detail}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m suspension_lab.replay_goal_signals <session_folder>")
        raise SystemExit(1)
    print_replay(Path(sys.argv[1]).resolve())
