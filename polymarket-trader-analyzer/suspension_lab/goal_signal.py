from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass
from decimal import Decimal

from suspension_lab.exit_engine import get_per_line_exit_mode, is_bond_spoof_bid, is_total_05_ticker
from suspension_lab.config import (
    BOND_MID_THRESHOLD,
    BOND_HOLD_BID_CENTS,
    GOAL_ASK_CONFIRM_CENTS,
    GOAL_ASK_LOOKBACK_MAX_BID_DRIFT_CENTS,
    GOAL_ASK_LOOKBACK_MS,
    GOAL_BID_JUMP_CENTS,
    GOAL_DELAYED_MIN_MS,
    GOAL_DELAYED_WINDOW_MS,
    GOAL_FAST_WINDOW_MS,
    GOAL_MIN_BID_QTY,
    GOAL_MIN_BLOWOUT_JUMP_CENTS,
    GOAL_MIN_PREV_BID_CENTS,
    GOAL_SIGNAL_COOLDOWN_MS,
    GOAL_SPREAD_BLOWOUT_CENTS,
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


@dataclass
class DelayedStateNotice:
    """Gradual reprice — red card / delayed news / VAR-ending grind. Do not scalp."""

    ticker: str
    ts_ms: int
    bid_change_cents: int
    seconds: float
    reason: str


class GoalSignalDetector:
    """Detect bid-side goal momentum (not ask-only scares). Point-in-time only."""

    def __init__(self) -> None:
        self._prev: dict[str, tuple[Decimal | None, Decimal | None, Decimal | None]] = {}
        self._history: dict[str, deque[tuple[int, Decimal | None, Decimal | None]]] = {}
        self._last_signal_ms: dict[str, int] = {}
        self._signal_peak_bid: dict[str, tuple[int, Decimal]] = {}
        self._primed: set[str] = set()
        self._spoof_active: set[str] = set()
        self._delayed_ms: dict[str, int] = {}

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
        # Exclude the current tick — bid just jumped; look at ask leading in prior ~2.5s.
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
    ) -> GoalSignal | VarRevertAlert | SpoofBidNotice | DelayedStateNotice | None:
        levels = book.top_levels()
        new_bid = _d(levels.get("yes_bid"))
        new_ask = _d(levels.get("yes_ask"))
        bid_qty = _d(levels.get("yes_bid_qty")) or Decimal(0)
        ts_ms = int(levels.get("updated_ms") or time.time() * 1000)

        prev_bid, prev_ask, _ = self._prev.get(ticker, (None, None, None))

        hist = self._history.setdefault(ticker, deque(maxlen=80))
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
        blowout = self._spread_blowout(prev_bid, prev_ask, new_bid, new_ask, jump_cents)
        ask_ok = self._ask_confirmed(ticker, prev_bid, prev_ask, new_ask, ts_ms)
        start_bid, window_jump, window_span = self._window_move(ticker, ts_ms, GOAL_FAST_WINDOW_MS)
        fast_walk = window_jump >= GOAL_BID_JUMP_CENTS and window_span <= GOAL_FAST_WINDOW_MS
        tick_jump = jump_cents >= GOAL_BID_JUMP_CENTS

        # +10c within 4s on a live ML/ATM is a GOAL. Do not classify as delayed_grind.
        if fast_walk or tick_jump or blowout:
            signal_prev = start_bid if fast_walk and start_bid is not None else prev_bid
            signal_jump = window_jump if fast_walk else jump_cents
            if int(round(signal_prev * 100)) >= GOAL_MIN_PREV_BID_CENTS:
                size_ok = bid_qty >= GOAL_MIN_BID_QTY or fast_walk
                confirm_ok = fast_walk or ask_ok or blowout
                if size_ok and confirm_ok:
                    last = self._last_signal_ms.get(ticker)
                    if last is None or ts_ms - last >= GOAL_SIGNAL_COOLDOWN_MS:
                        self._last_signal_ms[ticker] = ts_ms
                        self._signal_peak_bid[ticker] = (ts_ms, new_bid)
                        self._spoof_active.discard(ticker)
                        exit_mode = self._exit_mode(ticker, new_bid, new_ask, levels)
                        reason = "bid_jump_with_size_and_ask_confirm"
                        if fast_walk and not tick_jump:
                            reason = "bid_walk_plus10c_within_4s"
                        elif blowout and not ask_ok:
                            reason = "spread_blowout_books_pulled"
                        elif (
                            prev_ask
                            and new_ask
                            and new_ask - prev_ask < Decimal(GOAL_ASK_CONFIRM_CENTS) / 100
                        ):
                            reason = "bid_jump_ask_led_within_2s"
                        return GoalSignal(
                            ticker=ticker,
                            ts_ms=ts_ms,
                            prev_bid=signal_prev,
                            new_bid=new_bid,
                            bid_jump_cents=signal_jump,
                            bid_qty=bid_qty,
                            prev_ask=prev_ask,
                            new_ask=new_ask,
                            reason=reason,
                            exit_mode=exit_mode,
                        )

        delayed = self._delayed_grind(ticker, ts_ms, ask_ok=ask_ok, blowout=blowout)
        if delayed:
            return delayed
        return None

    def _spread_blowout(
        self,
        prev_bid: Decimal,
        prev_ask: Decimal | None,
        new_bid: Decimal,
        new_ask: Decimal | None,
        jump_cents: int,
    ) -> bool:
        if prev_ask is None or new_ask is None:
            return False
        if jump_cents < GOAL_MIN_BLOWOUT_JUMP_CENTS:
            return False
        prev_spread = int(round((prev_ask - prev_bid) * 100))
        new_spread = int(round((new_ask - new_bid) * 100))
        if prev_spread > 5:
            return False
        return new_spread - prev_spread >= GOAL_SPREAD_BLOWOUT_CENTS

    def _window_move(
        self, ticker: str, ts_ms: int, window_ms: int
    ) -> tuple[Decimal | None, int, int]:
        hist = [
            (h[0], h[1])
            for h in self._history.get(ticker, deque())
            if ts_ms - h[0] <= window_ms and h[1] is not None
        ]
        if len(hist) < 2:
            return None, 0, 0
        first_ts, first_bid = hist[0]
        last_ts, last_bid = hist[-1]
        jump = int(round((last_bid - first_bid) * 100))
        span = max(int(last_ts - first_ts), 0)
        return first_bid, jump, span

    def _delayed_grind(
        self,
        ticker: str,
        ts_ms: int,
        *,
        ask_ok: bool,
        blowout: bool,
    ) -> DelayedStateNotice | None:
        """Skip only slow walks with no ask-confirm and no blowout, or moves > ~6-8s."""
        if ask_ok or blowout:
            return None
        hist = [h for h in self._history.get(ticker, deque()) if ts_ms - h[0] <= GOAL_DELAYED_WINDOW_MS]
        bids = [(h[0], h[1]) for h in hist if h[1] is not None]
        if len(bids) < 4:
            return None
        first_ts, first_bid = bids[0]
        last_ts, last_bid = bids[-1]
        span_ms = last_ts - first_ts
        if span_ms < GOAL_DELAYED_MIN_MS:
            return None
        fast_bids = [(t, b) for t, b in bids if last_ts - t <= GOAL_FAST_WINDOW_MS]
        if len(fast_bids) >= 2:
            fast_jump = int(round((fast_bids[-1][1] - fast_bids[0][1]) * 100))
            if fast_jump >= GOAL_BID_JUMP_CENTS:
                return None
        total = int(round((last_bid - first_bid) * 100))
        if total < GOAL_BID_JUMP_CENTS:
            return None
        steps = [
            int(round((bids[i][1] - bids[i - 1][1]) * 100))
            for i in range(1, len(bids))
        ]
        if max(steps) >= GOAL_BID_JUMP_CENTS:
            return None
        last = self._delayed_ms.get(ticker)
        if last is not None and ts_ms - last < GOAL_SIGNAL_COOLDOWN_MS:
            return None
        self._delayed_ms[ticker] = ts_ms
        seconds = max(span_ms / 1000.0, 0.1)
        return DelayedStateNotice(
            ticker=ticker,
            ts_ms=ts_ms,
            bid_change_cents=total,
            seconds=seconds,
            reason="delayed_grind_red_card_like",
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
