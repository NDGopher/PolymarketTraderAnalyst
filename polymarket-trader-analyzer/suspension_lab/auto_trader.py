"""Paper auto-trader (no live orders yet). Hooks into goal signals + book updates."""

from __future__ import annotations

import csv
import threading
import time
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path

from suspension_lab.exit_engine import check_exit, scalp_target_cents
from suspension_lab.goal_signal import GoalSignal


@dataclass
class TraderConfig:
    enabled: bool = False
    live: bool = False  # must stay False until explicitly enabled
    contracts: int = 50
    bid_offset_cents: int = 1  # bid +1¢ for queue priority
    max_open_positions: int = 3

    @classmethod
    def from_env(cls) -> TraderConfig:
        import os

        return cls(
            enabled=os.environ.get("LAB_TRADER_ENABLED", "").lower() in ("1", "true", "yes"),
            live=False,
            contracts=int(os.environ.get("LAB_TRADER_CONTRACTS", "50")),
            bid_offset_cents=int(os.environ.get("LAB_TRADER_BID_OFFSET_CENTS", "1")),
        )


@dataclass
class PaperPosition:
    trade_id: int
    ticker: str
    market_label: str
    entry_cents: int
    signal_bid_cents: int
    contracts: int
    exit_mode: str
    entry_ts_ms: int
    peak_cents: int = 0
    status: str = "open"  # open | closed
    exit_cents: int | None = None
    exit_reason: str = ""
    exit_ts_ms: int | None = None


class PaperAutoTrader:
    def __init__(self, session_dir: Path, config: TraderConfig | None = None) -> None:
        self.config = config or TraderConfig()
        self.session_dir = session_dir
        self._lock = threading.Lock()
        self._trade_id = 0
        self._positions: dict[str, PaperPosition] = {}
        self._closed: list[PaperPosition] = []
        self._path = session_dir / "paper_trades.csv"
        self._init_csv()

    def _init_csv(self) -> None:
        if not self._path.exists():
            with self._path.open("w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(
                    [
                        "trade_id",
                        "ticker",
                        "market_label",
                        "status",
                        "contracts",
                        "signal_bid_cents",
                        "entry_cents",
                        "exit_cents",
                        "pnl_cents",
                        "exit_mode",
                        "entry_ts_iso",
                        "exit_ts_iso",
                        "exit_reason",
                    ]
                )

    @property
    def mode_label(self) -> str:
        if not self.config.enabled:
            return "OFF"
        if self.config.live:
            return "LIVE"
        return f"PAPER ({self.config.contracts}ct, bid+{self.config.bid_offset_cents}¢)"

    def on_goal_signal(self, signal: GoalSignal, market_label: str) -> PaperPosition | None:
        if not self.config.enabled or self.config.live:
            return None
        if len(self._positions) >= self.config.max_open_positions:
            return None
        if signal.ticker in self._positions:
            return None

        signal_cents = int(round(signal.new_bid * 100))
        entry_cents = min(signal_cents + self.config.bid_offset_cents, 99)

        with self._lock:
            self._trade_id += 1
            tid = self._trade_id
            pos = PaperPosition(
                trade_id=tid,
                ticker=signal.ticker,
                market_label=market_label,
                entry_cents=entry_cents,
                signal_bid_cents=signal_cents,
                contracts=self.config.contracts,
                exit_mode=signal.exit_mode,
                entry_ts_ms=signal.ts_ms,
                peak_cents=entry_cents,
            )
            self._positions[signal.ticker] = pos
            self._write_row(pos)
        return pos

    def on_book(
        self,
        ticker: str,
        bid_cents: int | None,
        *,
        ask_cents: int | None = None,
        bid_qty: float = 0,
    ) -> PaperPosition | None:
        if bid_cents is None:
            return None
        pos = self._positions.get(ticker)
        if not pos or pos.status != "open":
            return None

        now_ms = int(time.time() * 1000)
        pos.peak_cents = max(pos.peak_cents, bid_cents)
        held = (now_ms - pos.entry_ts_ms) / 1000.0

        decision = check_exit(
            exit_mode=pos.exit_mode,
            entry_cents=pos.entry_cents,
            current_bid_cents=bid_cents,
            peak_cents=pos.peak_cents,
            seconds_held=held,
            current_ask_cents=ask_cents,
            bid_qty=bid_qty,
        )

        if decision.action == "exit":
            return self._close(pos, bid_cents, decision.reason, now_ms)
        return None

    def _close(
        self, pos: PaperPosition, exit_cents: int, reason: str, ts_ms: int
    ) -> PaperPosition:
        pos.status = "closed"
        pos.exit_cents = exit_cents
        pos.exit_reason = reason
        pos.exit_ts_ms = ts_ms
        self._positions.pop(pos.ticker, None)
        self._closed.append(pos)
        self._write_row(pos)
        return pos

    def _write_row(self, pos: PaperPosition) -> None:
        from datetime import datetime, timezone

        def _iso(ms: int | None) -> str:
            if ms is None:
                return ""
            return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).isoformat()

        pnl = ""
        if pos.exit_cents is not None:
            pnl = pos.exit_cents - pos.entry_cents
        row = [
            pos.trade_id,
            pos.ticker,
            pos.market_label,
            pos.status,
            pos.contracts,
            pos.signal_bid_cents,
            pos.entry_cents,
            pos.exit_cents if pos.exit_cents is not None else "",
            pnl,
            pos.exit_mode,
            _iso(pos.entry_ts_ms),
            _iso(pos.exit_ts_ms),
            pos.exit_reason,
        ]
        with self._lock:
            with self._path.open("a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(row)

    def open_positions(self) -> list[PaperPosition]:
        return list(self._positions.values())

    def summary_line(self, pos: PaperPosition) -> str:
        target = scalp_target_cents(pos.entry_cents)
        return (
            f"#{pos.trade_id} {pos.ticker[-12:]} entry {pos.entry_cents}¢ "
            f"({pos.contracts}ct, {pos.exit_mode}, tgt {target}¢)"
        )
