"""Seated WS-only lock: no 60s rediscover, no REST fallback, single process.

Detector (GOAL_BID_JUMP_CENTS / qty 500 / walked_bid / VAR) is untouched.
"""

from __future__ import annotations

import inspect
from pathlib import Path
from unittest.mock import MagicMock, patch

from suspension_lab.config import (
    GOAL_ASK_CONFIRM_CENTS,
    GOAL_BID_JUMP_CENTS,
    GOAL_MIN_BID_QTY,
    GOAL_MIN_PREV_BID_CENTS,
    SCALP_TARGET_CENTS,
    VAR_REVERT_CENTS,
    LabConfig,
)
from suspension_lab.instance_lock import LabInstanceLock, LabLockHeld
from suspension_lab.kalshi_client import KalshiBookFeed
from suspension_lab.lab_runtime import LabRuntime
from suspension_lab.rate_limit import DEFAULT_RETRY_AFTER_S, get_json_with_retry, retry_after_seconds
from suspension_lab.soccer_discovery import (
    DISCOVERY_MAX_WORKERS,
    DiscoveryGate,
    DiscoveryResult,
    FetchStats,
    SoccerGame,
    fetch_open_soccer_markets,
)

UI_PY = Path(__file__).resolve().parents[1] / "suspension_lab" / "ui.py"


def _udinese() -> SoccerGame:
    return SoccerGame(
        event_ticker="KXCOPPAITALIAGAME-26SEP02UDIVEN",
        title="Udinese vs Venezia",
        home_team="Udinese",
        away_team="Venezia",
        close_time="",
        home_ml_ticker="KXCOPPAITALIAGAME-26SEP02UDIVEN-UDI",
        away_ml_ticker="KXCOPPAITALIAGAME-26SEP02UDIVEN-VEN",
    )


class TestDetectorUntouched:
    def test_goal_fire_constants(self):
        assert GOAL_BID_JUMP_CENTS == 10
        assert GOAL_MIN_BID_QTY == 500
        assert GOAL_MIN_PREV_BID_CENTS == 15
        assert GOAL_ASK_CONFIRM_CENTS == 3
        assert SCALP_TARGET_CENTS == 7
        assert VAR_REVERT_CENTS == 10


class TestKnownMarketsNeverRediscover:
    def _runtime(self, tmp_path) -> LabRuntime:
        game = _udinese()
        config = LabConfig(
            tickers=game.get_tickers(),
            game_label="Udinese vs Venezia",
            output_dir=tmp_path,
        )
        config.games = [game]
        return LabRuntime(config, auto_discover=True)

    def test_seated_tickers_skip_discover_soccer_games(self, tmp_path):
        runtime = self._runtime(tmp_path)
        assert runtime.has_known_markets()
        with patch("suspension_lab.lab_runtime.discover_soccer_games") as mock:
            runtime._run_discover(force=False)
            runtime._run_discover(force=True)
            mock.assert_not_called()

    def test_start_does_not_queue_60s_rediscover(self, tmp_path):
        runtime = self._runtime(tmp_path)
        queued: list[object] = []
        runtime.request_discover = lambda **_k: queued.append("discover")
        runtime.feed.start = lambda: None
        with patch("threading.Thread.start", lambda self: None):
            runtime.start()
        assert queued == []

    def test_discover_loop_bails_on_known_markets(self):
        src = inspect.getsource(LabRuntime._discover_loop)
        assert "has_known_markets" in src
        start = inspect.getsource(LabRuntime.start)
        assert "has_known_markets" in start
        assert "request_discover(force=False)" not in start

    def test_cli_pins_force_auto_discover_off(self):
        from suspension_lab import cli

        src = inspect.getsource(cli.main)
        assert "auto_discover = False" in src

    def test_ui_does_not_schedule_60s_rediscover(self):
        src = UI_PY.read_text(encoding="utf-8")
        assert "after(60_000" not in src
        assert "after(30_000" not in src
        assert "No 60s rediscover" in src


class TestWsOnlyNoRestFallback:
    def test_ws_loop_never_calls_rest_loop(self):
        ws = inspect.getsource(KalshiBookFeed._ws_loop)
        run = inspect.getsource(KalshiBookFeed._run)
        whole = inspect.getsource(KalshiBookFeed)
        assert "_rest_loop" not in ws
        assert "WS_FAILS_BEFORE_REST" not in whole
        assert "reconnect" in ws
        assert "_rest_loop" in run
        assert "not polling REST" in run
        assert "asyncio.gather(" not in whole

    def test_add_ticker_does_not_rest_on_ws(self):
        feed = KalshiBookFeed(LabConfig(tickers=[], use_ws=True))
        called: list[str] = []
        feed._fetch_rest_snapshot = lambda *_a, **_k: called.append("rest") or True
        assert feed.add_ticker("KXTESTGAME-26SEP02AB-A")
        assert called == []
        assert "KXTESTGAME-26SEP02AB-A" in feed._pending_subscribe

    def test_fetch_rest_snapshot_429_no_raise_for_status(self):
        src = inspect.getsource(KalshiBookFeed._fetch_rest_snapshot)
        assert "raise_for_status" not in src
        assert "429" in src
        assert "_mark_rate_limit" in src


class TestRetryAfter:
    def test_header_seconds(self):
        assert retry_after_seconds({"Retry-After": "7"}) == 7.0

    def test_header_default_five(self):
        assert retry_after_seconds({}) == DEFAULT_RETRY_AFTER_S

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

    def test_snapshot_429_logs_note(self):
        notes: list[str] = []
        feed = KalshiBookFeed(
            LabConfig(tickers=["KXTESTGAME-26SEP02AB-A"], use_ws=True),
            on_note=notes.append,
        )
        session = MagicMock()
        resp = MagicMock()
        resp.status_code = 429
        resp.headers = {"Retry-After": "5"}
        session.get.return_value = resp
        with patch("suspension_lab.kalshi_client.time.sleep", lambda *_a, **_k: None):
            ok = feed._fetch_rest_snapshot(session, "KXTESTGAME-26SEP02AB-A")
        assert ok is False
        assert notes
        assert "429" in notes[0]


class TestDiscoveryWorkersAndScan:
    def test_max_workers_constant(self):
        assert DISCOVERY_MAX_WORKERS <= 2

    def test_series_429_skips_global_scan(self):
        labels: list[str] = []

        def fake_get(_session, _url, _params, _timeout, label, **_kwargs):
            labels.append(label)
            from suspension_lab.rate_limit import HttpFetch

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
        assert not any(str(label).startswith("markets-page") for label in labels)

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
