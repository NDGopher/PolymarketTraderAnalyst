from __future__ import annotations

import time
from dataclasses import dataclass
from decimal import Decimal

from suspension_lab.config import (
    BOND_MID_THRESHOLD,
    GOAL_ASK_CONFIRM_CENTS,
    GOAL_BID_JUMP_CENTS,
    GOAL_MIN_BID_QTY,
    GOAL_MIN_PREV_BID_CENTS,
    GOAL_SIGNAL_COOLDOWN_MS,
)
from suspension_lab.orderbook import OrderBook


def _d(val: str | Decimal | None) -> Decimal | None:
    if val is None or val == "":
        return None
    try:
        return Decimal(str(val))
    except Exception:  # noqa: BLE001
        return None


@dataclass(frozen=True)
class GoalSignal:
    ticker: str
    ts_ms: int
    prev_bid: Decimal
    new_bid: Decimal
    bid_jump_cents: int
    bid_qty: Decimal
    prev_ask: Decimal | None
    new_ask: Decimal | None
    reason: str

    @property
    def summary(self) -> str:
        ask_part = ""
        if self.prev_ask is not None and self.new_ask is not None:
            ask_part = f" ask {self.prev_ask:.2f}->{self.new_ask:.2f}"
        return (
            f"GOAL SIGNAL bid {self.prev_bid:.2f}->{self.new_bid:.2f} "
            f"(+{self.bid_jump_cents}c) qty={self.bid_qty:.0f}{ask_part}"
        )


class GoalSignalDetector:
    """Detect bid-side goal momentum (not ask-only scares). Point-in-time only."""

    def __init__(self) -> None:
        self._prev: dict[str, tuple[Decimal | None, Decimal | None, Decimal | None]] = {}
        self._last_signal_ms: dict[str, int] = {}
        self._primed: set[str] = set()

    def evaluate(self, ticker: str, book: OrderBook) -> GoalSignal | None:
        levels = book.top_levels()
        new_bid = _d(levels.get("yes_bid"))
        new_ask = _d(levels.get("yes_ask"))
        bid_qty = _d(levels.get("yes_bid_qty")) or Decimal(0)
        ts_ms = int(levels.get("updated_ms") or time.time() * 1000)

        prev_bid, prev_ask, _ = self._prev.get(ticker, (None, None, None))

        # Store current for next tick before early returns
        self._prev[ticker] = (new_bid, new_ask, bid_qty)

        if ticker not in self._primed:
            self._primed.add(ticker)
            return None

        if new_bid is None or prev_bid is None:
            return None

        jump_cents = int(round((new_bid - prev_bid) * 100))
        if jump_cents < GOAL_BID_JUMP_CENTS:
            return None

        if int(round(prev_bid * 100)) < GOAL_MIN_PREV_BID_CENTS:
            return None

        if bid_qty < GOAL_MIN_BID_QTY:
            return None

        if levels.get("is_bond"):
            return None

        mid = _d(levels.get("yes_mid"))
        if mid is not None and (mid >= Decimal(str(BOND_MID_THRESHOLD)) or mid <= Decimal("0.10")):
            return None

        # Ask must confirm (full book reprice). Ask-only scares keep bid flat.
        if new_ask is None:
            return None
        if prev_ask is not None:
            ask_jump = int(round((new_ask - prev_ask) * 100))
            if ask_jump < GOAL_ASK_CONFIRM_CENTS:
                return None
        elif prev_bid == new_bid:
            return None

        last = self._last_signal_ms.get(ticker, 0)
        if ts_ms - last < GOAL_SIGNAL_COOLDOWN_MS:
            return None

        self._last_signal_ms[ticker] = ts_ms
        return GoalSignal(
            ticker=ticker,
            ts_ms=ts_ms,
            prev_bid=prev_bid,
            new_bid=new_bid,
            bid_jump_cents=jump_cents,
            bid_qty=bid_qty,
            prev_ask=prev_ask,
            new_ask=new_ask,
            reason="bid_jump_with_size_and_ask_confirm",
        )
