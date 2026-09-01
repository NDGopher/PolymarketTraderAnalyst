"""Replay goal-signal detector against a saved session books.csv."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

from suspension_lab.goal_signal import GoalSignal, GoalSignalDetector, VarRevertAlert
from suspension_lab.orderbook import OrderBook


@dataclass
class ReplayEvent:
    ts_iso: str
    ticker: str
    kind: str
    detail: str


def _ticker_prefixes(headers: list[str]) -> list[str]:
    return [h[: -len("_yes_bid")] for h in headers if h.endswith("_yes_bid")]


def replay_session(session_dir: Path) -> list[ReplayEvent]:
    books_path = session_dir / "books.csv"
    if not books_path.exists():
        raise FileNotFoundError(books_path)

    meta_path = session_dir / "session.json"
    tickers = []
    if meta_path.exists():
        tickers = json.loads(meta_path.read_text(encoding="utf-8")).get("tickers", [])

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
            result = detectors[prefix].evaluate(prefix, book)
            if isinstance(result, GoalSignal):
                events.append(
                    ReplayEvent(
                        ts_iso=ts_iso,
                        ticker=prefix,
                        kind="GOAL",
                        detail=result.summary,
                    )
                )
            elif isinstance(result, VarRevertAlert):
                events.append(
                    ReplayEvent(
                        ts_iso=ts_iso,
                        ticker=prefix,
                        kind="VAR",
                        detail=(
                            f"peak {result.peak_bid:.2f} -> {result.current_bid:.2f} "
                            f"(-{result.drop_cents}c in {result.seconds_since_signal:.0f}s)"
                        ),
                    )
                )
    return events


def print_replay(session_dir: Path) -> None:
    for ev in replay_session(session_dir):
        print(f"{ev.ts_iso} [{ev.kind}] {ev.ticker}: {ev.detail}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m suspension_lab.replay_goal_signals <session_folder>")
        raise SystemExit(1)
    print_replay(Path(sys.argv[1]).resolve())
