"""Paper tape: today-first discover, fee-aware scalp, book GOAL, no invented fills."""

from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from suspension_lab.goal_signal import (
    DelayedStateNotice,
    GoalSignal,
    GoalSignalDetector,
    VarRevertAlert,
)
from suspension_lab.orderbook import OrderBook
from suspension_lab.scalp_quote import kalshi_fee_cents, make_around_jump
from suspension_lab.kalshi_client import orderbook_subscribe_payload
from suspension_lab.soccer_discovery import (
    DiscoveryResult,
    build_soccer_game,
    discover_soccer_games,
    needs_auto_discover,
    parse_cli_tickers,
    select_ingame_totals,
    TotalBook,
)
from suspension_lab.tape_engine import TapeEngine


def _book(ticker: str, bid: str, ask: str, bid_qty: str = "200", ask_qty: str = "200", ts: int = 1_000) -> OrderBook:
    book = OrderBook(ticker)
    book.set_from_top(bid=bid, ask=ask, bid_qty=bid_qty, ask_qty=ask_qty, updated_ms=ts)
    return book


class TestPlaceholderTickers:
    def test_empty_and_example_tokens(self):
        assert needs_auto_discover([])
        assert needs_auto_discover(["TICKER_O35", "TICKER_O45"])
        assert needs_auto_discover(["auto"])
        assert needs_auto_discover(["run"])
        assert not needs_auto_discover(["KXEPLGAME-26SEP02ARSCHE-ARS"])

    def test_yesterday_melgar_env_does_not_skip_discovery(self, monkeypatch):
        now = datetime(2026, 9, 2, 15, 0, tzinfo=timezone.utc)
        leftover = "KXPERLIGA1GAME-26AUG31CAGMEL-MEL,KXPERLIGA1GAME-26AUG31CAGMEL-CAG"
        monkeypatch.setenv("LAB_TICKERS", leftover)
        monkeypatch.setenv("LAB_GAME", "TEST2-MELGAR-GRAU")
        assert parse_cli_tickers("") == []
        assert needs_auto_discover(leftover.split(","), now=now)
        assert needs_auto_discover(parse_cli_tickers(""), now=now)


class TestEmptySubscribe:
    def test_empty_ticker_list_does_not_emit_subscribe(self):
        assert orderbook_subscribe_payload([], msg_id=1) is None
        assert orderbook_subscribe_payload(["", "  "], msg_id=2) is None

    def test_real_tickers_include_market_tickers(self):
        payload = orderbook_subscribe_payload(
            ["KXEGYPLGAME-26SEP02GOUMOK-GOU"], msg_id=3
        )
        assert payload is not None
        assert payload["params"]["market_tickers"] == ["KXEGYPLGAME-26SEP02GOUMOK-GOU"]
        assert "orderbook_delta" in payload["params"]["channels"]

    def test_cli_options_do_not_bind_env_lab_tickers(self):
        import inspect

        from suspension_lab import cli

        src = inspect.getsource(cli.main)
        assert 'envvar="LAB_TICKERS"' not in src
        assert 'envvar="LAB_GAME"' not in src


class TestEnvCannotSkipDiscover:
    @patch("suspension_lab.paper_logger.discover_soccer_games")
    def test_resolve_tickers_ignores_env_melgar(self, mock_discover, monkeypatch):
        monkeypatch.setenv(
            "LAB_TICKERS",
            "KXPERLIGA1GAME-26AUG31CAGMEL-MEL,KXPERLIGA1TOTAL-26AUG31CAGMEL-4",
        )
        mock_discover.return_value = DiscoveryResult(
            games=[],
            tickers=["KXEGYPLGAME-26SEP02GOUMOK-GOU"],
            log_lines=["discovered egypt"],
        )
        from suspension_lab.paper_logger import _resolve_tickers

        tickers, _games, _log = _resolve_tickers(
            "",
            demo=False,
            auto_discover=True,
            max_games=5,
            min_volume=50,
        )
        mock_discover.assert_called_once()
        assert tickers == ["KXEGYPLGAME-26SEP02GOUMOK-GOU"]


class TestTodayFirstDiscover:
    @patch("suspension_lab.soccer_discovery.fetch_open_soccer_markets")
    def test_picks_tonight_over_weekend_volume(self, mock_fetch):
        mock_fetch.return_value = [
            {
                "ticker": "KXEPLGAME-26SEP07ARSLIV-ARS",
                "event_ticker": "KXEPLGAME-26SEP07ARSLIV",
                "title": "Arsenal vs Liverpool",
                "close_time": "2026-09-10T01:00:00Z",
                "occurrence_datetime": "2026-09-07T15:00:00Z",
                "volume_fp": "900000",
                "volume_24h_fp": "200000",
                "rules_primary": "If Arsenal wins the Arsenal vs Liverpool professional EPL soccer game",
            },
            {
                "ticker": "KXEPLGAME-26SEP07ARSLIV-LIV",
                "event_ticker": "KXEPLGAME-26SEP07ARSLIV",
                "title": "Arsenal vs Liverpool",
                "close_time": "2026-09-10T01:00:00Z",
                "occurrence_datetime": "2026-09-07T15:00:00Z",
                "volume_fp": "800000",
                "volume_24h_fp": "180000",
            },
            {
                "ticker": "KXCOPPAITALIAGAME-26SEP02SASFRO-SAS",
                "event_ticker": "KXCOPPAITALIAGAME-26SEP02SASFRO",
                "title": "Sassuolo vs Frosinone",
                "close_time": "2026-09-05T01:00:00Z",
                "occurrence_datetime": "2026-09-02T12:00:00Z",
                "volume_fp": "10000",
                "volume_24h_fp": "8000",
                "rules_primary": "If Sassuolo wins the Sassuolo vs Frosinone professional Coppa Italia soccer game",
            },
            {
                "ticker": "KXCOPPAITALIAGAME-26SEP02SASFRO-FRO",
                "event_ticker": "KXCOPPAITALIAGAME-26SEP02SASFRO",
                "title": "Sassuolo vs Frosinone",
                "close_time": "2026-09-05T01:00:00Z",
                "occurrence_datetime": "2026-09-02T12:00:00Z",
                "volume_fp": "9000",
                "volume_24h_fp": "7000",
            },
            {
                "ticker": "KXCOPPAITALIATOTAL-26SEP02SASFRO-1",
                "event_ticker": "KXCOPPAITALIATOTAL-26SEP02SASFRO",
                "occurrence_datetime": "2026-09-02T12:00:00Z",
                "volume_fp": "1000",
                "volume_24h_fp": "500",
            },
        ]
        now = datetime(2026, 9, 2, 13, 0, tzinfo=timezone.utc)
        result = discover_soccer_games(max_games=3, now=now)

        titles = [g.title for g in result.games]
        assert any("Sassuolo" in t for t in titles)
        assert not any("Liverpool" in t for t in titles)

    def test_tie_excluded_from_ml(self):
        markets = [
            {
                "ticker": "KXCOPPAITALIAGAME-26SEP02SASFRO-TIE",
                "event_ticker": "KXCOPPAITALIAGAME-26SEP02SASFRO",
                "title": "Tie",
                "volume_fp": "10",
                "volume_24h_fp": "10",
            },
            {
                "ticker": "KXCOPPAITALIAGAME-26SEP02SASFRO-SAS",
                "event_ticker": "KXCOPPAITALIAGAME-26SEP02SASFRO",
                "title": "Sassuolo",
                "volume_fp": "10",
                "volume_24h_fp": "10",
            },
            {
                "ticker": "KXCOPPAITALIAGAME-26SEP02SASFRO-FRO",
                "event_ticker": "KXCOPPAITALIAGAME-26SEP02SASFRO",
                "title": "Frosinone",
                "volume_fp": "10",
                "volume_24h_fp": "10",
            },
        ]
        game = build_soccer_game("26SEP02SASFRO", markets)
        assert game is not None
        assert game.home_ml_ticker and "TIE" not in game.home_ml_ticker
        assert game.away_ml_ticker and "TIE" not in game.away_ml_ticker


class TestScalpQuote:
    def test_never_mid_and_fee_peaks_at_50(self):
        mid_fee = kalshi_fee_cents(50)
        wing_fee = kalshi_fee_cents(10)
        assert mid_fee > wing_fee
        q = make_around_jump(32, 40)
        assert not q.skipped
        assert q.entry_cents == 33
        assert q.entry_cents != 36  # not mid of 32/40

    def test_skip_fee_peak_tight_spread(self):
        q = make_around_jump(49, 51)
        assert q.skipped
        assert "50" in q.skip_reason or "tight" in q.skip_reason or "fee" in q.skip_reason


class TestBookGoalDetection:
    def test_spread_blowout_is_goal(self):
        det = GoalSignalDetector()
        t = "KXCOPPAITALIATOTAL-26SEP02SASFRO-1"
        det.evaluate(t, _book(t, "0.40", "0.42", ts=1000))
        result = det.evaluate(t, _book(t, "0.48", "0.64", bid_qty="250", ts=1200))
        assert isinstance(result, GoalSignal)
        assert "blowout" in result.reason or result.bid_jump_cents >= 6

    def test_plus10c_walk_with_ask_confirm_is_goal(self):
        """Walk +10c in 4s AND ask +3c (Grau/Melgar style) is a GOAL."""
        det = GoalSignalDetector()
        t = "KXCOPPAITALIATOTAL-26SEP02UDIVEN-2"
        det.evaluate(t, _book(t, "0.40", "0.42", ts=16_343_000))
        result = None
        asks = ("0.44", "0.46", "0.48", "0.50", "0.52")
        for i, bid in enumerate(("0.42", "0.44", "0.46", "0.48", "0.50")):
            result = det.evaluate(
                t, _book(t, bid, asks[i], bid_qty="200", ts=16_343_000 + (i + 1) * 740)
            )
        assert isinstance(result, GoalSignal)
        assert result.bid_jump_cents >= 10
        assert result.reason == "bid_walk_plus10c_ask_confirm"

    def test_bid_only_walk_does_not_fire_or_arm_var(self):
        """16:38 CT false fire: bid 0.35->0.45, ask stuck 0.48. Not a goal. No VAR."""
        det = GoalSignalDetector()
        t = "KXCOPPAITALIAGAME-26SEP02UDIVEN-UDI"
        det.evaluate(t, _book(t, "0.35", "0.48", ts=16_382_400))
        seen = []
        for i, bid in enumerate(("0.37", "0.39", "0.41", "0.43", "0.45")):
            seen.append(
                det.evaluate(
                    t, _book(t, bid, "0.48", bid_qty="200", ts=16_382_400 + (i + 1) * 700)
                )
            )
        assert not any(isinstance(r, GoalSignal) for r in seen)
        assert t not in det._signal_peak_bid
        drop = det.evaluate(t, _book(t, "0.36", "0.48", bid_qty="200", ts=16_391_500))
        assert not isinstance(drop, VarRevertAlert)
        assert not isinstance(drop, GoalSignal)

    def test_one_tick_plus10c_ask_flat_is_not_goal(self):
        det = GoalSignalDetector()
        t = "KXEPLGAME-26SEP02TEST-ARS"
        det.evaluate(t, _book(t, "0.35", "0.48", ts=1000))
        result = det.evaluate(t, _book(t, "0.45", "0.48", bid_qty="200", ts=1200))
        assert not isinstance(result, GoalSignal)
        assert t not in det._signal_peak_bid

    def test_one_tick_plus10c_with_ask_confirm_is_goal(self):
        """Yesterday Grau/Melgar: bid and ask jumped together."""
        det = GoalSignalDetector()
        t = "KXPERLIGA1GAME-26AUG31CAGMEL-GRA"
        det.evaluate(t, _book(t, "0.20", "0.22", ts=1000))
        result = det.evaluate(t, _book(t, "0.40", "0.40", bid_qty="200", ts=1200))
        assert isinstance(result, GoalSignal)
        assert result.bid_jump_cents >= 10

    def test_venezia_ml_walk_14c_over_3s_is_goal(self):
        det = GoalSignalDetector()
        t = "KXCOPPAITALIAGAME-26SEP02UDIVEN-VEN"
        det.evaluate(t, _book(t, "0.24", "0.26", ts=16_233_000))
        seen = []
        for i, bid in enumerate(("0.27", "0.30", "0.33", "0.36", "0.38")):
            seen.append(
                det.evaluate(
                    t, _book(t, bid, "0.40", bid_qty="180", ts=16_233_000 + (i + 1) * 700)
                )
            )
        goals = [r for r in seen if isinstance(r, GoalSignal)]
        assert goals
        assert goals[0].bid_jump_cents >= 10

    def test_slow_8s_walk_without_ask_confirm_is_delayed(self):
        det = GoalSignalDetector()
        t = "KXEPLGAME-26SEP02TEST-ARS"
        det.evaluate(t, _book(t, "0.30", "0.31", ts=1000))
        seen = []
        for i, bid in enumerate(("0.31", "0.32", "0.33", "0.34", "0.36", "0.38", "0.40", "0.42")):
            seen.append(
                det.evaluate(
                    t, _book(t, bid, "0.32", bid_qty="200", ts=1000 + (i + 1) * 1000)
                )
            )
        delayed = [r for r in seen if isinstance(r, DelayedStateNotice)]
        assert delayed
        assert delayed[0].seconds >= 6.0
        assert not any(isinstance(r, GoalSignal) for r in seen)


class TestInGameTotalsOnTape:
    def test_live_yes_repick_not_pregame_snapshot(self):
        books = [
            TotalBook(3, "T-3", 0.85, 50, 50, True),
            TotalBook(4, "T-4", 0.51, 50, 50, True),
            TotalBook(5, "T-5", 0.24, 50, 50, True),
        ]
        atm, up = select_ingame_totals(books)
        assert atm is not None and atm.ticker == "T-4"
        assert up is not None and up.ticker == "T-5"

    def test_el_gouna_grind_funds_o15_not_o35(self):
        books = [
            TotalBook(1, "GOUMOK-1", 0.91, 50, 50, True),
            TotalBook(2, "GOUMOK-2", 0.50, 200, 200, True, yes_bid=0.47),
            TotalBook(3, "GOUMOK-3", 0.24, 80, 80, True),
            TotalBook(4, "GOUMOK-4", 0.05, 40, 40, True, yes_bid=0.04),
            TotalBook(5, "GOUMOK-5", 0.02, 20, 20, True, untradeable=True),
        ]
        atm, up = select_ingame_totals(books)
        assert atm is not None and atm.ticker == "GOUMOK-2"
        assert up is not None and up.ticker == "GOUMOK-3"


class TestTapeEnginePaperOnly:
    def test_walk_goal_writes_csv_even_if_trader_skips_bond(self, tmp_path: Path):
        engine = TapeEngine.create(
            tmp_path / "sess",
            ["KXCOPPAITALIATOTAL-26SEP02UDIVEN-2"],
            paper_enabled=True,
        )
        t = "KXCOPPAITALIATOTAL-26SEP02UDIVEN-2"
        engine.handle_book(t, _book(t, "0.88", "0.90", ts=1000))
        result = None
        for i, bid in enumerate(("0.90", "0.92", "0.94", "0.96", "0.98")):
            result = engine.handle_book(
                t, _book(t, bid, "0.99", bid_qty="200", ts=1000 + (i + 1) * 700)
            )
        signals = (tmp_path / "sess" / "goal_signals.csv").read_text(encoding="utf-8")
        assert "KXCOPPAITALIATOTAL-26SEP02UDIVEN-2" in signals
        assert any(e.kind == "GOAL" for e in engine.events)
        assert engine.trader.config.live is False

    def test_goal_logs_paper_not_invented_fill(self, tmp_path: Path):
        engine = TapeEngine.create(
            tmp_path / "sess",
            ["KXTESTGAME-26SEP02AB-A"],
            paper_enabled=True,
        )
        assert engine.trader.config.live is False
        t = "KXTESTGAME-26SEP02AB-A"
        engine.handle_book(t, _book(t, "0.30", "0.32", ts=1))
        engine.handle_book(t, _book(t, "0.45", "0.48", bid_qty="300", ts=2))
        signals = (tmp_path / "sess" / "goal_signals.csv").read_text(encoding="utf-8")
        # Either a GOAL printed or the book was not ask-confirmed — never a fake FILL.
        assert "FILL" not in signals
        trades = (tmp_path / "sess" / "paper_trades.csv").read_text(encoding="utf-8")
        assert "FILL" not in trades
        assert engine.trader.config.live is False
