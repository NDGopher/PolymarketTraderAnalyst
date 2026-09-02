from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass
from decimal import Decimal

from suspension_lab.exit_engine import get_per_line_exit_mode, is_bond_spoof_bid
from suspension_lab.config import (
    BOND_MID_THRESHOLD,
    BOND_HOLD_BID_CENTS,
    GOAL_ASK_CONFIRM_CENTS,
    GOAL_ASK_LOOKBACK_MAX_BID_DRIFT_CENTS,
    GOAL_ASK_LOOKBACK_MS,
    GOAL_BID_JUMP_CENTS,
    GOAL_MIN_BID_QTY,
    GOAL_MIN_PREV_BID_CENTS,
    GOAL_SIGNAL_COOLDOWN_MS,
    VAR_REVERT_CENTS,
    VAR_REVERT_WINDOW_MS,
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
    exit_mode: str  # "hold_bond" | "scalp" | "var_watch"

    @property
    def summary(self) -> str:
        ask_part = ""
        if self.prev_ask is not None and self.new_ask is not None:
            ask_part = f" ask {self.prev_ask:.2f}->{self.new_ask:.2f}"
        return (
            f"GOAL SIGNAL bid {self.prev_bid:.2f}->{self.new_bid:.2f} "
            f"(+{self.bid_jump_cents}c) qty={self.bid_qty:.0f}{ask_part} "
            f"[{self.exit_mode}]"
        )


@dataclass
class VarRevertAlert:
    ticker: str
    ts_ms: int
    peak_bid: Decimal
    current_bid: Decimal
    drop_cents: int
    seconds_since_signal: float
    is_spoof: bool = False  # lowball bid on bonded market; ask stayed high


@dataclass
class SpoofBidNotice:
    """Thin lowball bid on a bonded market — not VAR, game still live."""

    ticker: str
    ts_ms: int
    peak_bid: Decimal
    current_bid: Decimal
    current_ask: Decimal
    bid_qty: Decimal
    drop_cents: int


class GoalSignalDetector:
    """One-tick bid jump + MM size + ask confirm. Point-in-time only.

    Fire rule is fd32045 (PR #5) with GOAL_MIN_BID_QTY=500. Spoof/VAR is PR #8.
    No delayed_grind, no grind-as-GOAL, no spread-blowout GOAL.
    """

    def __init__(self) -> None:
        self._prev: dict[str, tuple[Decimal | None, Decimal | None, Decimal | None]] = {}
        self._history: dict[str, deque[tuple[int, Decimal | None, Decimal | None]]] = {}
        self._last_signal_ms: dict[str, int] = {}
        self._signal_peak_bid: dict[str, tuple[int, Decimal]] = {}
        self._primed: set[str] = set()
        self._spoof_active: set[str] = set()

    def _history_window(self, ticker: str, now_ms: int) -> list[tuple[int, Decimal | None, Decimal | None]]:
        hist = self._history.get(ticker, deque())
        return [h for h in hist if now_ms - h[0] <= GOAL_ASK_LOOKBACK_MS]

    def _ask_confirmed(
        self,
        ticker: str,
        prev_bid: Decimal,
        prev_ask: Decimal | None,
        new_ask: Decimal | None,
        ts_ms: int,
    ) -> bool:
        if new_ask is None:
            return False
        confirm = Decimal(GOAL_ASK_CONFIRM_CENTS) / 100
        if prev_ask is not None and new_ask - prev_ask >= confirm:
            return True
        window = self._history_window(ticker, ts_ms)
        # Extra confirm: ask led in prior ~2.5s (fd32045). Not a standalone trigger.
        prior = window[:-1] if len(window) > 1 else []
        if len(prior) < 2:
            return False
        bids = [h[1] for h in prior if h[1] is not None]
        asks = [h[2] for h in prior if h[2] is not None]
        if not bids or not asks:
            return False
        max_bid_drift = Decimal(GOAL_ASK_LOOKBACK_MAX_BID_DRIFT_CENTS) / 100
        if max(bids) - min(bids) > max_bid_drift:
            return False
        ask_move = max(asks) - min(asks)
        if ask_move >= confirm:
            return True
        return new_ask - min(asks) >= confirm

    def _was_bond(self, prev_bid: Decimal, prev_ask: Decimal | None) -> bool:
        if prev_ask is not None:
            mid = (prev_bid + prev_ask) / 2
        else:
            mid = prev_bid
        return mid >= Decimal(str(BOND_MID_THRESHOLD)) or mid <= Decimal("0.10")

    def _exit_mode(self, ticker: str, new_bid: Decimal, new_ask: Decimal | None, levels: dict) -> str:
        bid_cents = int(new_bid * 100)
        is_bonded = bid_cents >= BOND_HOLD_BID_CENTS or new_ask is None or levels.get("is_bond")

        if is_bonded:
            return "hold_bond"

        base_mode = "var_watch" if bid_cents >= 70 else "scalp"
        return get_per_line_exit_mode(ticker, base_mode, is_bonded=False)

    def evaluate(
        self, ticker: str, book: OrderBook
    ) -> GoalSignal | VarRevertAlert | SpoofBidNotice | None:
        levels = book.top_levels()
        new_bid = _d(levels.get("yes_bid"))
        new_ask = _d(levels.get("yes_ask"))
        bid_qty = _d(levels.get("yes_bid_qty")) or Decimal(0)
        ts_ms = int(levels.get("updated_ms") or time.time() * 1000)

        prev_bid, prev_ask, _ = self._prev.get(ticker, (None, None, None))

        hist = self._history.setdefault(ticker, deque(maxlen=30))
        hist.append((ts_ms, new_bid, new_ask))
        self._prev[ticker] = (new_bid, new_ask, bid_qty)

        var_alert = self._check_var_revert(ticker, new_bid, new_ask, bid_qty, ts_ms)
        if var_alert:
            return var_alert

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

        if self._was_bond(prev_bid, prev_ask):
            return None

        if not self._ask_confirmed(ticker, prev_bid, prev_ask, new_ask, ts_ms):
            return None

        last = self._last_signal_ms.get(ticker, 0)
        if ts_ms - last < GOAL_SIGNAL_COOLDOWN_MS:
            return None

        self._last_signal_ms[ticker] = ts_ms
        self._signal_peak_bid[ticker] = (ts_ms, new_bid)
        self._spoof_active.discard(ticker)
        exit_mode = self._exit_mode(ticker, new_bid, new_ask, levels)
        reason = "bid_jump_with_size_and_ask_confirm"
        if prev_ask and new_ask and new_ask - prev_ask < Decimal(GOAL_ASK_CONFIRM_CENTS) / 100:
            reason = "bid_jump_ask_led_within_2s"

        return GoalSignal(
            ticker=ticker,
            ts_ms=ts_ms,
            prev_bid=prev_bid,
            new_bid=new_bid,
            bid_jump_cents=jump_cents,
            bid_qty=bid_qty,
            prev_ask=prev_ask,
            new_ask=new_ask,
            reason=reason,
            exit_mode=exit_mode,
        )

    def _check_var_revert(
        self,
        ticker: str,
        new_bid: Decimal | None,
        new_ask: Decimal | None,
        bid_qty: Decimal,
        ts_ms: int,
    ) -> VarRevertAlert | SpoofBidNotice | None:
        peak_info = self._signal_peak_bid.get(ticker)
        if not peak_info or new_bid is None:
            return None
        signal_ms, peak_bid = peak_info
        if ts_ms - signal_ms > VAR_REVERT_WINDOW_MS:
            self._signal_peak_bid.pop(ticker, None)
            return None
        if new_bid > peak_bid:
            self._signal_peak_bid[ticker] = (signal_ms, new_bid)
            return None
        drop = int(round((peak_bid - new_bid) * 100))
        if drop < VAR_REVERT_CENTS:
            return None

        _, prev_ask, _ = self._prev.get(ticker, (None, None, None))
        ask_ref = new_ask if new_ask is not None else prev_ask
        peak_cents = int(round(peak_bid * 100))
        bid_cents = int(round(new_bid * 100))
        ask_cents = int(round(ask_ref * 100)) if ask_ref is not None else None

        if is_bond_spoof_bid(
            peak_cents=peak_cents,
            current_bid_cents=bid_cents,
            current_ask_cents=ask_cents,
            bid_qty=float(bid_qty),
        ):
            if ticker not in self._spoof_active:
                self._spoof_active.add(ticker)
                return SpoofBidNotice(
                    ticker=ticker,
                    ts_ms=ts_ms,
                    peak_bid=peak_bid,
                    current_bid=new_bid,
                    current_ask=ask_ref or new_bid,
                    bid_qty=bid_qty,
                    drop_cents=drop,
                )
            return None

        self._spoof_active.discard(ticker)
        self._signal_peak_bid.pop(ticker, None)
        return VarRevertAlert(
            ticker=ticker,
            ts_ms=ts_ms,
            peak_bid=peak_bid,
            current_bid=new_bid,
            drop_cents=drop,
            seconds_since_signal=(ts_ms - signal_ms) / 1000.0,
            is_spoof=False,
        )
