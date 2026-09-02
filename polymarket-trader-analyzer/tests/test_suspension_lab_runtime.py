"""429 backoff, single-instance lock, WS-only L2, Tk-off-thread trader, UI lock."""

from __future__ import annotations

import asyncio
import inspect
import time
from concurrent.futures import Future
from pathlib import Path
from unittest.mock import MagicMock, patch

UI_PY = Path(__file__).resolve().parents[1] / "suspension_lab" / "ui.py"

from suspension_lab.config import LabConfig
from suspension_lab.instance_lock import LabInstanceLock, LabLockHeld
from suspension_lab.kalshi_client import (
    REST_CYCLE_MIN_S,
    REST_TICKER_GAP_S,
    KalshiBookFeed,
)
from suspension_lab.lab_runtime import ENGINE_THREAD_NAME, LabRuntime
from suspension_lab.rate_limit import DEFAULT_RETRY_AFTER_S, HttpFetch, get_json_with_retry, retry_after_seconds
from suspension_lab.soccer_discovery import (
    DISCOVERY_MAX_WORKERS,
    DiscoveryGate,
    DiscoveryResult,
    FetchStats,
    SoccerGame,
    fetch_open_soccer_markets,
)
from suspension_lab.ui_layout import (
    GRID_BREAK_PX,
    WINDOW_GEOMETRY,
    WINDOW_MIN_HEIGHT,
    WINDOW_MIN_WIDTH,
    format_yes_price,
    matchup_hero,
    tile_columns_for_width,
)


class TestRetryAfter:
    def test_header_seconds(self):
        assert retry_after_seconds({"Retry-After": "7"}) == 7.0

    def test_header_default_five(self):
        assert retry_after_seconds({}) == DEFAULT_RETRY_AFTER_S
        assert retry_after_seconds(None) == DEFAULT_RETRY_AFTER_S

    def test_get_json_sleeps_retry_after(self):
        sleeps: list[float] = []
        session = MagicMock()
        resp = MagicMock()
        resp.status_code = 429
        resp.headers = {"Retry-After": "7"}
        session.get.return_value = resp
        out = get_json_with_retry(
            session,
            "https://example.test/markets",
            {},
            1.0,
            "lab",
            max_attempts=2,
            sleep=sleeps.append,
        )
        assert sleeps
        assert sleeps[0] == 7.0
        assert out.rate_limited or session.get.call_count >= 2


class TestDiscoveryWorkersAndScan:
    def test_max_workers_constant(self):
        assert DISCOVERY_MAX_WORKERS <= 2

    def test_threadpool_workers_capped(self):
        recorded: list[int] = []

        class FakePool:
            def __init__(self, max_workers=None, **_kwargs):
                recorded.append(int(max_workers))

            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def submit(self, fn, *args):
                fut = Future()
                fut.set_result(([], False, 0.0))
                return fut

        with patch("suspension_lab.soccer_discovery.ThreadPoolExecutor", FakePool):
            with patch(
                "suspension_lab.soccer_discovery.fetch_soccer_series_tickers",
                return_value=[f"KXTESTGAME{i}" for i in range(70)],
            ):
                with patch(
                    "suspension_lab.soccer_discovery.get_json_with_retry",
                    return_value=HttpFetch(payload={"markets": []}),
                ):
                    fetch_open_soccer_markets("https://example.test")
        assert recorded
        assert all(workers <= 2 for workers in recorded)

    def test_series_429_skips_global_scan(self):
        labels: list[str] = []

        def fake_get(_session, _url, _params, _timeout, label, **_kwargs):
            labels.append(label)
            return HttpFetch(payload={"markets": []})

        with patch(
            "suspension_lab.soccer_discovery.fetch_soccer_series_tickers",
            return_value=["KXEPLGAME"],
        ):
            with patch(
                "suspension_lab.soccer_discovery._fetch_series_markets",
                return_value=([], True, 5.0),
            ):
                with patch(
                    "suspension_lab.soccer_discovery.get_json_with_retry",
                    side_effect=fake_get,
                ):
                    stats = FetchStats()
                    fetch_open_soccer_markets("https://example.test", stats=stats)
        assert stats.series_429 or stats.skipped_global_scan
        assert not any(label.startswith("markets-page") for label in labels)

    def test_gate_keeps_last_good_on_429_cooldown(self):
        gate = DiscoveryGate()
        seated = DiscoveryResult(
            games=[],
            tickers=["KXCOPPAITALIAGAME-26SEP02UDIVEN-UDI"],
            log_lines=["seed"],
        )
        gate.store(seated)
        gate.note_rate_limit(8)
        allowed, cached = gate.allow(force=True)
        assert allowed is False
        assert cached is not None
        assert "UDIVEN" in cached.tickers[0]

    def test_runtime_429_does_not_blank_seated(self, tmp_path):
        game = SoccerGame(
            event_ticker="KXCOPPAITALIAGAME-26SEP02UDIVEN",
            title="Udinese vs Venezia",
            home_team="Udinese",
            away_team="Venezia",
            close_time="",
            home_ml_ticker="KXCOPPAITALIAGAME-26SEP02UDIVEN-UDI",
            away_ml_ticker="KXCOPPAITALIAGAME-26SEP02UDIVEN-VEN",
        )
        config = LabConfig(
            tickers=game.get_tickers(),
            game_label="Udinese vs Venezia",
            output_dir=tmp_path,
        )
        config.games = [game]
        runtime = LabRuntime(config, auto_discover=False)
        empty = DiscoveryResult(
            games=[],
            tickers=[],
            log_lines=["429"],
            rate_limited=True,
            retry_after=5,
        )
        with patch("suspension_lab.lab_runtime.discover_soccer_games", return_value=empty):
            runtime._run_discover(force=True)
        assert runtime.engine.games
        assert runtime.engine.games[0].title == "Udinese vs Venezia"
        assert "KXCOPPAITALIAGAME-26SEP02UDIVEN-UDI" in runtime.feed.books


class TestRestLoopPacing:
    def test_constants_and_no_gather(self):
        assert REST_TICKER_GAP_S >= 1.0
        assert REST_CYCLE_MIN_S >= 3.0
        src = inspect.getsource(KalshiBookFeed)
        assert "asyncio.gather(" not in src
        slow = inspect.getsource(KalshiBookFeed._slow_rest_loop)
        assert "gather(" not in slow

    def test_add_ticker_does_not_rest_on_caller(self):
        feed = KalshiBookFeed(LabConfig(tickers=[]))
        called: list[str] = []
        feed._fetch_rest_snapshot = lambda *_a, **_k: called.append("rest") or True
        assert feed.add_ticker("KXTESTGAME-26SEP02AB-A")
        assert called == []
        assert "KXTESTGAME-26SEP02AB-A" in feed._pending_snapshots

    def test_slow_rest_one_ticker_per_second(self):
        feed = KalshiBookFeed(LabConfig(tickers=["T1", "T2"], use_ws=False))
        stamps: list[float] = []

        def fake(_session, _ticker):
            stamps.append(time.monotonic())
            return True

        feed._fetch_rest_snapshot = fake

        async def _run() -> None:
            task = asyncio.create_task(feed._slow_rest_loop())
            await asyncio.sleep(2.15)
            feed._stop.set()
            await asyncio.wait_for(task, timeout=3)

        asyncio.run(_run())
        assert len(stamps) >= 2
        assert stamps[1] - stamps[0] >= 0.99


class TestInstanceLock:
    def test_second_lock_fails(self, tmp_path):
        path = tmp_path / "lab.lock"
        first = LabInstanceLock(path)
        first.acquire("headless")
        second = LabInstanceLock(path)
        try:
            second.acquire("gui")
            raise AssertionError("second process must not acquire the lab lock")
        except LabLockHeld as exc:
            assert "already running" in str(exc).lower()
            assert exc.mode == "headless"
        finally:
            first.release()


class TestTkIsNotKalshiClient:
    def test_engine_thread_name(self):
        assert ENGINE_THREAD_NAME == "lab-engine"
        assert ENGINE_THREAD_NAME != "MainThread"

    def test_ui_does_not_construct_feed_or_discover(self):
        src = UI_PY.read_text(encoding="utf-8")
        assert "KalshiBookFeed" not in src
        assert "discover_soccer_games" not in src
        assert "discover_tickers_for_lab" not in src
        assert "request_add_tickers" in src
        assert "self.feed.add_ticker" not in src
        on_book = inspect.getsource(LabRuntime._on_book)
        assert "_book_q" in on_book

    def test_handle_book_runs_on_engine_loop(self):
        src = inspect.getsource(LabRuntime._engine_loop)
        assert "handle_book" in src
        ui_src = UI_PY.read_text(encoding="utf-8")
        assert "engine.handle_book" not in ui_src


class TestDesignerLock:
    def test_geometry_and_grid_break(self):
        assert WINDOW_GEOMETRY == "1100x720"
        assert WINDOW_MIN_WIDTH == 900
        assert WINDOW_MIN_HEIGHT == 600
        assert tile_columns_for_width(1000) == 3
        assert tile_columns_for_width(1100) == 3
        assert tile_columns_for_width(999) == 2
        assert GRID_BREAK_PX == 1000

    def test_missing_price_is_ascii_hyphen(self):
        assert format_yes_price(None) == "-"
        assert format_yes_price("") == "-"
        assert format_yes_price("?") == "-"
        assert "\u2014" not in format_yes_price(None)
        assert "\u2013" not in format_yes_price(None)

    def test_matchup_hero_is_english(self):
        game = SoccerGame(
            event_ticker="KXCOPPAITALIAGAME-26SEP02UDIVEN",
            title="Udinese vs Venezia",
            home_team="Udinese",
            away_team="Venezia",
            close_time="",
        )
        assert matchup_hero(game) == "Udinese vs Venezia"
        raw = SoccerGame(
            event_ticker="KXCOPPAITALIAGAME-26SEP02UDIVEN",
            title="KXCOPPAITALIAGAME-26SEP02UDIVEN",
            home_team="Udinese",
            away_team="Venezia",
            close_time="",
        )
        assert matchup_hero(raw) == "Udinese vs Venezia"

    def test_ui_source_lock(self):
        src = UI_PY.read_text(encoding="utf-8")
        layout = (UI_PY.parent / "ui_layout.py").read_text(encoding="utf-8")
        assert "\u2014" not in src
        assert "\u2013" not in src
        assert "\u2014" not in layout
        assert "1100x720" in layout
        assert "MouseWheel" in src
        assert "Button-4" in src
        assert "Button-5" in src
        assert "winfo_width" in src
        start = src.index("def _create_book_box")
        end = src.index("def _sync_trader_toggle")
        box_src = src[start:end]
        assert 'side="left"' not in box_src
        assert "side=left" not in box_src
        grid_start = src.index("class BookGrid")
        grid_end = src.index("class SuspensionLabApp")
        grid_src = src[grid_start:grid_end]
        assert ".grid(" in grid_src
        assert 'pack(side="left"' not in grid_src
        assert "STALE" in src
        assert "FROZEN" in src
        assert "429" in src
        configure = src[src.index("def _on_canvas_configure") : src.index("def _on_cards_configure")]
        assert "itemconfigure" in configure
        assert "scrollregion" in configure
