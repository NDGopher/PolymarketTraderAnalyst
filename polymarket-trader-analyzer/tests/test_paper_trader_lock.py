"""Nested lock on paper entry must not hang the WS callback.

Production 2026-09-02 19:20:17Z: Celtic O3.5 0.41→0.58 qty 500 ask-confirm
scalp was logged in goal_signals.csv, then on_goal_signal took Lock and called
_write_row which took the same Lock. paper_trades.csv stayed header-only and
all five books froze until kill.
"""

from __future__ import annotations

import threading
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from suspension_lab.auto_trader import PaperAutoTrader, TraderConfig
from suspension_lab.goal_signal import GoalSignal

CELTIC_O35 = "KXSPLGAME-26SEP02CELXXX-3"
DEADLOCK_TIMEOUT_S = 1.0


def _celtic_scalp_signal() -> GoalSignal:
    ts = datetime(2026, 9, 2, 19, 20, 17, 184000, tzinfo=timezone.utc)
    return GoalSignal(
        ticker=CELTIC_O35,
        ts_ms=int(ts.timestamp() * 1000),
        prev_bid=Decimal("0.41"),
        new_bid=Decimal("0.58"),
        bid_jump_cents=17,
        bid_qty=Decimal("500"),
        prev_ask=Decimal("0.42"),
        new_ask=Decimal("0.59"),
        reason="bid_jump_with_size_and_ask_confirm",
        exit_mode="scalp",
    )


def _paper_trader(tmp_path: Path) -> PaperAutoTrader:
    session_dir = tmp_path / "sess"
    session_dir.mkdir(parents=True, exist_ok=True)
    return PaperAutoTrader(
        session_dir,
        TraderConfig(enabled=True, live=False, contracts=50),
    )


def test_on_goal_signal_writes_paper_row_without_deadlock(tmp_path: Path) -> None:
    trader = _paper_trader(tmp_path)
    signal = _celtic_scalp_signal()
    holder: list[object] = []
    errors: list[BaseException] = []

    def _fire() -> None:
        try:
            holder.append(trader.on_goal_signal(signal, "Celtic Over 3.5"))
        except BaseException as exc:  # noqa: BLE001 — surface in parent thread
            errors.append(exc)

    worker = threading.Thread(target=_fire, name="goal-signal-paper", daemon=True)
    worker.start()
    worker.join(timeout=DEADLOCK_TIMEOUT_S)
    assert not worker.is_alive(), (
        "on_goal_signal deadlocked: nested lock while writing paper_trades.csv"
    )
    assert not errors
    pos = holder[0]
    assert pos is not None
    assert pos.ticker == CELTIC_O35
    assert pos.exit_mode == "scalp"
    assert pos.entry_cents == 59  # 58 + bid+1
    assert pos.signal_bid_cents == 58
    text = trader._path.read_text(encoding="utf-8")
    rows = [line for line in text.strip().splitlines() if line]
    assert len(rows) == 2  # header + paper open
    assert CELTIC_O35 in text
    assert "scalp" in text
    assert "open" in text
