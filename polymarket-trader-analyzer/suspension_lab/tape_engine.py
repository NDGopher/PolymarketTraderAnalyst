"""Shared paper tape: log books, detect GOAL from the book, scalp/flatten.

Used by the UI and the headless paper logger. Never places live orders.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from suspension_lab.auto_trader import PaperAutoTrader, PaperPosition, TraderConfig
from suspension_lab.goal_signal import (
    DelayedStateNotice,
    GoalSignal,
    GoalSignalDetector,
    SpoofBidNotice,
    VarRevertAlert,
)
from suspension_lab.market_labels import MarketLabel, MarketLabelCache
from suspension_lab.session import SessionLogger
from suspension_lab.soccer_discovery import SoccerGame


@dataclass
class TapeEvent:
    kind: str
    ticker: str
    label: str
    detail: str
    ts_iso: str
    bucket: str = ""  # would_have | burned | skip | ""


@dataclass
class TapeEngine:
    logger: SessionLogger
    trader: PaperAutoTrader
    detector: GoalSignalDetector
    labels: MarketLabelCache
    games: list[SoccerGame] = field(default_factory=list)
    events: list[TapeEvent] = field(default_factory=list)
    on_event: Callable[[TapeEvent], None] | None = None

    @classmethod
    def create(
        cls,
        session_dir: Path,
        tickers: list[str],
        *,
        game_label: str = "",
        games: list[SoccerGame] | None = None,
        rest_base: str = "",
        paper_enabled: bool = True,
    ) -> TapeEngine:
        logger = SessionLogger(session_dir, tickers, game_label=game_label)
        cfg = TraderConfig.from_env()
        cfg.enabled = paper_enabled
        cfg.live = False
        trader = PaperAutoTrader(session_dir, cfg)
        labels = MarketLabelCache(tickers, rest_base=rest_base)
        engine = cls(
            logger=logger,
            trader=trader,
            detector=GoalSignalDetector(),
            labels=labels,
            games=list(games or []),
        )
        engine._write_discovery_meta(session_dir)
        return engine

    def _write_discovery_meta(self, session_dir: Path) -> None:
        meta_path = session_dir / "session.json"
        meta: dict[str, Any] = {}
        if meta_path.exists():
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        meta["paper_only"] = True
        meta["live_orders"] = False
        meta["games"] = [
            {
                "title": g.title,
                "occurrence_time": g.occurrence_time,
                "tickers": g.get_tickers(),
                "volume_24h": g.total_24h_volume,
                "totals": g.totals_summary(),
                "totals_repick": g.totals_repick,
            }
            for g in self.games
        ]
        meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    def _emit(self, event: TapeEvent) -> None:
        self.events.append(event)
        line = f"[{event.kind}] {event.label}: {event.detail}"
        self.logger.append_note(line)
        if self.on_event:
            self.on_event(event)

    def handle_book(self, ticker: str, book) -> PaperPosition | None:
        result = self.detector.evaluate(ticker, book)
        levels = book.top_levels()
        bid_s = levels.get("yes_bid", "")
        bid_cents = int(round(float(bid_s) * 100)) if bid_s else None
        ask_s = levels.get("yes_ask", "")
        ask_cents = int(round(float(ask_s) * 100)) if ask_s else None
        bid_qty = float(levels.get("yes_bid_qty") or 0)
        label = self.labels.get(ticker)
        display = label.display if label else ticker
        now = datetime.now(tz=timezone.utc).isoformat()

        if isinstance(result, GoalSignal):
            self.logger.log_goal_signal(
                ticker=result.ticker,
                market_label=display,
                prev_bid=f"{result.prev_bid:.4f}",
                new_bid=f"{result.new_bid:.4f}",
                bid_jump_cents=result.bid_jump_cents,
                bid_qty=f"{result.bid_qty:.2f}",
                prev_ask=f"{result.prev_ask:.4f}" if result.prev_ask is not None else "",
                new_ask=f"{result.new_ask:.4f}" if result.new_ask is not None else "",
                reason=result.reason,
                exit_mode=result.exit_mode,
                ts_ms=result.ts_ms,
            )
            pos = self.trader.on_goal_signal(result, display)
            detail = result.summary
            if pos:
                detail += f" → paper make {pos.entry_cents}¢"
            elif self.trader.skipped:
                detail += f" → skip {self.trader.skipped[-1]}"
            self._emit(TapeEvent("GOAL", ticker, display, detail, now))
            return pos

        if isinstance(result, VarRevertAlert):
            closed = self.trader.flatten(ticker, bid_cents, f"VAR flatten -{result.drop_cents}c")
            self._emit(
                TapeEvent(
                    "VAR",
                    ticker,
                    display,
                    f"bid {result.peak_bid:.2f}→{result.current_bid:.2f} (-{result.drop_cents}c) flatten",
                    now,
                    "burned",
                )
            )
            return closed

        if isinstance(result, SpoofBidNotice):
            self._emit(
                TapeEvent(
                    "SPOOF",
                    ticker,
                    display,
                    f"bid {result.current_bid:.2f} ask {result.current_ask:.2f} — hold, not VAR",
                    now,
                    "skip",
                )
            )
            return None

        if isinstance(result, DelayedStateNotice):
            closed = self.trader.flatten(
                ticker, bid_cents, f"flatten delayed/red-card-like +{result.bid_change_cents}c"
            )
            self._emit(
                TapeEvent(
                    "SKIP",
                    ticker,
                    display,
                    f"{result.reason} +{result.bid_change_cents}c over {result.seconds:.1f}s — no scalp",
                    now,
                    "burned" if closed else "skip",
                )
            )
            return closed

        if bid_cents is not None and self.trader.config.enabled:
            closed = self.trader.on_book(
                ticker, bid_cents, ask_cents=ask_cents, bid_qty=bid_qty
            )
            if closed:
                bucket = "burned" if closed.exit_reason.lower().startswith("var") else "would_have"
                pnl = (closed.exit_cents or 0) - closed.entry_cents
                self._emit(
                    TapeEvent(
                        "EXIT",
                        ticker,
                        display,
                        f"{closed.exit_reason} @ {closed.exit_cents}¢ ({pnl:+d}¢/ct) [paper]",
                        now,
                        bucket,
                    )
                )
                return closed
        return None
