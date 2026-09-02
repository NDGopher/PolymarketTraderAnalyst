"""Restore lock: fd32045 fire + PR #8 spoof, GOAL_MIN_BID_QTY=500.

Paper only. Replay Melgar Grau CSV. Thin ask-flat walks must not fire.
"""

from pathlib import Path

from suspension_lab.config import GOAL_MIN_BID_QTY, SCALP_TARGET_CENTS
from suspension_lab.exit_engine import scalp_target_cents
from suspension_lab.goal_signal import (
    GoalSignal,
    GoalSignalDetector,
    SpoofBidNotice,
    VarRevertAlert,
)
from suspension_lab.orderbook import OrderBook
from suspension_lab.replay_goal_signals import replay_session


MELGAR = (
    Path(__file__).resolve().parents[1]
    / "suspension_lab"
    / "sessions"
    / "20260901_210900_TEST2-MELGAR-GRAU"
)
GRAU = "KXPERLIGA1GAME-26AUG31CAGMEL-CAG"
O05 = "KXPERLIGA1TOTAL-26AUG31CAGMEL-1"


def _book(
    ticker: str,
    bid: str,
    ask: str,
    bid_qty: str = "500",
    ask_qty: str = "200",
    ts: int = 1_000,
) -> OrderBook:
    book = OrderBook(ticker)
    book.set_from_top(bid=bid, ask=ask, bid_qty=bid_qty, ask_qty=ask_qty, updated_ms=ts)
    return book


class TestRestoreLock:
    def test_qty_floor_is_500(self):
        assert GOAL_MIN_BID_QTY == 500

    def test_paper_scalp_is_plus_7(self):
        assert SCALP_TARGET_CENTS == 7
        assert scalp_target_cents(34) == 41

    def test_melgar_grau_replay_fires(self):
        events = replay_session(MELGAR)
        grau = [e for e in events if e.kind == "GOAL" and GRAU in e.ticker]
        assert len(grau) == 1, [e.detail for e in events if e.kind == "GOAL"]
        detail = grau[0].detail
        assert "0.19" in detail and "0.34" in detail
        assert "+15c" in detail
        assert "qty=2568" in detail
        assert "0.20" in detail and "0.40" in detail
        assert "[scalp]" in detail

    def test_thin_ask_flat_walk_does_not_fire(self):
        det = GoalSignalDetector()
        t = "KXEPLGAME-26SEP02UDINESE-TIE"
        result = det.evaluate(t, _book(t, "0.38", "0.48", bid_qty="50", ts=1000))
        for i, bid in enumerate(("0.40", "0.42", "0.44", "0.46", "0.48")):
            result = det.evaluate(
                t, _book(t, bid, "0.48", bid_qty="50", ts=1000 + (i + 1) * 800)
            )
            assert result is None, result
        assert result is None
        assert t not in det._signal_peak_bid

    def test_one_tick_qty_50_ask_confirm_does_not_fire(self):
        det = GoalSignalDetector()
        t = "KXEPLGAME-26SEP02THIN-ARS"
        det.evaluate(t, _book(t, "0.19", "0.20", bid_qty="50", ts=1000))
        result = det.evaluate(t, _book(t, "0.34", "0.40", bid_qty="50", ts=1200))
        assert result is None
        assert t not in det._signal_peak_bid

    def test_bid_only_10c_qty_500_ask_flat_does_not_fire(self):
        det = GoalSignalDetector()
        t = "KXEPLGAME-26SEP02FLAT-ARS"
        det.evaluate(t, _book(t, "0.38", "0.48", bid_qty="500", ts=1000))
        result = det.evaluate(t, _book(t, "0.48", "0.48", bid_qty="500", ts=1200))
        assert result is None
        assert t not in det._signal_peak_bid

    def test_grau_style_one_tick_fires(self):
        det = GoalSignalDetector()
        det.evaluate(GRAU, _book(GRAU, "0.19", "0.20", bid_qty="58", ts=1000))
        result = det.evaluate(GRAU, _book(GRAU, "0.34", "0.40", bid_qty="2568", ts=1200))
        assert isinstance(result, GoalSignal)
        assert result.reason == "bid_jump_with_size_and_ask_confirm"
        assert result.bid_jump_cents == 15
        assert result.exit_mode == "scalp"
        assert GRAU in det._signal_peak_bid

    def test_ask_led_lookback_is_extra_confirm_only(self):
        det = GoalSignalDetector()
        t = "KXEPLGAME-26SEP02LED-ARS"
        det.evaluate(t, _book(t, "0.19", "0.20", bid_qty="200", ts=1000))
        det.evaluate(t, _book(t, "0.19", "0.24", bid_qty="200", ts=1800))
        det.evaluate(t, _book(t, "0.20", "0.25", bid_qty="200", ts=2600))
        result = det.evaluate(t, _book(t, "0.34", "0.25", bid_qty="2568", ts=3200))
        assert isinstance(result, GoalSignal)
        assert result.reason == "bid_jump_ask_led_within_2s"

    def test_var_flattens_after_real_goal_only(self):
        det = GoalSignalDetector()
        t = "KXEPLGAME-26SEP02VAR-ARS"
        det.evaluate(t, _book(t, "0.30", "0.32", bid_qty="200", ts=1000))
        goal = det.evaluate(t, _book(t, "0.45", "0.50", bid_qty="800", ts=1200))
        assert isinstance(goal, GoalSignal)
        revert = det.evaluate(t, _book(t, "0.35", "0.38", bid_qty="800", ts=2000))
        assert isinstance(revert, VarRevertAlert)
        assert revert.drop_cents == 10

    def test_spoof_on_bonded_is_not_var(self):
        det = GoalSignalDetector()
        det.evaluate(O05, _book(O05, "0.60", "0.94", bid_qty="200", ts=1000))
        goal = det.evaluate(O05, _book(O05, "0.98", "0.99", bid_qty="500", ts=1200))
        assert isinstance(goal, GoalSignal)
        assert goal.exit_mode == "hold_bond"
        spoof = det.evaluate(O05, _book(O05, "0.75", "0.99", bid_qty="8", ts=5000))
        assert isinstance(spoof, SpoofBidNotice)

    def test_no_delayed_grind_symbol(self):
        import suspension_lab.goal_signal as gs

        assert not hasattr(gs, "DelayedStateNotice")
        assert not hasattr(GoalSignalDetector, "_delayed_grind")
        assert not hasattr(GoalSignalDetector, "_spread_blowout")
