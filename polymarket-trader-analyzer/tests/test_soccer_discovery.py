"""Tests for soccer auto-discovery from Kalshi API."""

from datetime import datetime, timezone

import pytest
from unittest.mock import patch, MagicMock

from suspension_lab.soccer_discovery import (
    SoccerGame,
    DiscoveryResult,
    TotalBook,
    SOCCER_SERIES_PREFIXES,
    SERIES_WITH_GAMES,
    SERIES_WITH_TOTALS,
    _parse_volume,
    _extract_teams_from_title,
    _match_game_ticker,
    _match_total_ticker,
    _get_event_identifier,
    group_markets_by_event,
    build_soccer_game,
    discover_soccer_games,
    discover_tickers_for_lab,
    select_scalp_totals,
    select_ingame_totals,
    apply_live_totals,
    is_dead_wing,
    is_finished_game,
    is_pregame,
    is_in_play,
    repick_session_totals,
    should_fund_live,
    unfunded_tickers,
    is_soccer_series_ticker,
    is_stale_lab_ticker,
    looks_like_soccer_market,
    filter_soccer_markets,
    needs_auto_discover,
    parse_cli_tickers,
    soccer_series_tickers_from_catalog,
    strike_to_over_label,
)


class TestParseVolume:
    """Tests for _parse_volume helper."""

    def test_valid_volumes(self):
        market = {"volume_fp": "1234.56", "volume_24h_fp": "567.89"}
        vol, vol_24h = _parse_volume(market)
        assert vol == 1234.56
        assert vol_24h == 567.89

    def test_zero_volumes(self):
        market = {"volume_fp": "0", "volume_24h_fp": "0"}
        vol, vol_24h = _parse_volume(market)
        assert vol == 0.0
        assert vol_24h == 0.0

    def test_missing_volumes(self):
        market = {}
        vol, vol_24h = _parse_volume(market)
        assert vol == 0.0
        assert vol_24h == 0.0

    def test_none_volumes(self):
        market = {"volume_fp": None, "volume_24h_fp": None}
        vol, vol_24h = _parse_volume(market)
        assert vol == 0.0
        assert vol_24h == 0.0


class TestExtractTeams:
    """Tests for _extract_teams_from_title."""

    def test_vs_format(self):
        home, away = _extract_teams_from_title("Arsenal vs Chelsea - Aug 31, 2026")
        assert home == "Arsenal"
        assert away == "Chelsea"

    def test_dash_format(self):
        home, away = _extract_teams_from_title("Barcelona - Real Madrid")
        assert home == "Barcelona"
        assert away == "Real Madrid"

    def test_vs_dot_format(self):
        home, away = _extract_teams_from_title("Liverpool vs. Man City")
        assert home == "Liverpool"
        assert away == "Man City"

    def test_single_team(self):
        home, away = _extract_teams_from_title("Arsenal")
        assert home == "Arsenal"
        assert away == ""


class TestTickerMatching:
    """Tests for ticker regex matchers."""

    def test_game_ticker_match(self):
        match = _match_game_ticker("KXEPLGAME-26AUG31ARSCHE-ARS")
        assert match is not None
        assert match.group(1) == "KXEPLGAME"
        assert match.group(2) == "26AUG31ARSCHE"
        assert match.group(3) == "ARS"

    def test_game_ticker_away(self):
        match = _match_game_ticker("KXEPLGAME-26AUG31ARSCHE-CHE")
        assert match is not None
        assert match.group(3) == "CHE"

    def test_total_ticker_o05(self):
        match = _match_total_ticker("KXEPLTOTAL-26AUG31ARSCHE-1")
        assert match is not None
        assert match.group(1) == "KXEPLTOTAL"
        assert match.group(2) == "26AUG31ARSCHE"
        assert match.group(3) == "1"

    def test_total_ticker_o15(self):
        match = _match_total_ticker("KXEPLTOTAL-26AUG31ARSCHE-2")
        assert match is not None
        assert match.group(3) == "2"

    def test_invalid_ticker(self):
        assert _match_game_ticker("SOME-RANDOM-TICKER") is None
        assert _match_total_ticker("NOT-A-TOTAL-TICKER") is None

    def test_event_identifier_game(self):
        event_id = _get_event_identifier("KXEPLGAME-26AUG31ARSCHE-ARS")
        assert event_id == "26AUG31ARSCHE"

    def test_event_identifier_total(self):
        event_id = _get_event_identifier("KXEPLTOTAL-26AUG31ARSCHE-1")
        assert event_id == "26AUG31ARSCHE"


class TestGroupMarketsByEvent:
    """Tests for grouping markets by event."""

    def test_groups_same_game(self):
        markets = [
            {"ticker": "KXEPLGAME-26AUG31ARSCHE-ARS"},
            {"ticker": "KXEPLGAME-26AUG31ARSCHE-CHE"},
            {"ticker": "KXEPLTOTAL-26AUG31ARSCHE-1"},
            {"ticker": "KXEPLTOTAL-26AUG31ARSCHE-2"},
        ]
        groups = group_markets_by_event(markets)
        assert "26AUG31ARSCHE" in groups
        assert len(groups["26AUG31ARSCHE"]) == 4

    def test_groups_multiple_games(self):
        markets = [
            {"ticker": "KXEPLGAME-26AUG31ARSCHE-ARS"},
            {"ticker": "KXEPLGAME-26AUG31LIVMAN-LIV"},
        ]
        groups = group_markets_by_event(markets)
        assert len(groups) == 2
        assert "26AUG31ARSCHE" in groups
        assert "26AUG31LIVMAN" in groups


class TestBuildSoccerGame:
    """Tests for building SoccerGame from markets."""

    def test_builds_full_game(self):
        """Test building a game with all 4 tickers."""
        markets = [
            {
                "ticker": "KXEPLGAME-26AUG31ARSCHE-ARS",
                "event_ticker": "KXEPLGAME-26AUG31ARSCHE",
                "title": "Arsenal vs Chelsea - Aug 31, 2026",
                "close_time": "2026-08-31T18:00:00Z",
                "volume_fp": "100.00",
                "volume_24h_fp": "200.00",
            },
            {
                "ticker": "KXEPLGAME-26AUG31ARSCHE-CHE",
                "event_ticker": "KXEPLGAME-26AUG31ARSCHE",
                "title": "Arsenal vs Chelsea - Aug 31, 2026",
                "close_time": "2026-08-31T18:00:00Z",
                "volume_fp": "150.00",
                "volume_24h_fp": "300.00",
            },
            {
                "ticker": "KXEPLTOTAL-26AUG31ARSCHE-1",
                "event_ticker": "KXEPLTOTAL-26AUG31ARSCHE",
                "title": "Arsenal vs Chelsea O0.5 Goals",
                "close_time": "2026-08-31T18:00:00Z",
                "volume_fp": "50.00",
                "volume_24h_fp": "100.00",
                "yes_bid_dollars": "0.90",
                "yes_ask_dollars": "0.92",
            },
            {
                "ticker": "KXEPLTOTAL-26AUG31ARSCHE-2",
                "event_ticker": "KXEPLTOTAL-26AUG31ARSCHE",
                "title": "Arsenal vs Chelsea O1.5 Goals",
                "close_time": "2026-08-31T18:00:00Z",
                "volume_fp": "75.00",
                "volume_24h_fp": "125.00",
                "yes_bid_dollars": "0.71",
                "yes_ask_dollars": "0.73",
            },
            {
                "ticker": "KXEPLTOTAL-26AUG31ARSCHE-3",
                "event_ticker": "KXEPLTOTAL-26AUG31ARSCHE",
                "title": "Arsenal vs Chelsea O2.5 Goals",
                "close_time": "2026-08-31T18:00:00Z",
                "volume_fp": "80.00",
                "volume_24h_fp": "200.00",
                "yes_bid_dollars": "0.47",
                "yes_ask_dollars": "0.49",
            },
            {
                "ticker": "KXEPLTOTAL-26AUG31ARSCHE-4",
                "event_ticker": "KXEPLTOTAL-26AUG31ARSCHE",
                "title": "Arsenal vs Chelsea O3.5 Goals",
                "close_time": "2026-08-31T18:00:00Z",
                "volume_fp": "60.00",
                "volume_24h_fp": "150.00",
                "yes_bid_dollars": "0.27",
                "yes_ask_dollars": "0.29",
            },
        ]
        game = build_soccer_game("26AUG31ARSCHE", markets)

        assert game is not None
        assert game.home_ml_ticker == "KXEPLGAME-26AUG31ARSCHE-ARS"
        assert game.away_ml_ticker == "KXEPLGAME-26AUG31ARSCHE-CHE"
        assert game.total_atm_ticker == "KXEPLTOTAL-26AUG31ARSCHE-3"
        assert game.total_atm_label == "O2.5"
        assert game.total_up_ticker == "KXEPLTOTAL-26AUG31ARSCHE-4"
        assert game.total_up_label == "O3.5"
        assert len(game.get_tickers()) == 4

    def test_builds_game_no_totals(self):
        """Test building a game with only ML tickers."""
        markets = [
            {
                "ticker": "KXEPLGAME-26AUG31ARSCHE-ARS",
                "event_ticker": "KXEPLGAME-26AUG31ARSCHE",
                "title": "Arsenal vs Chelsea",
                "close_time": "2026-08-31T18:00:00Z",
                "volume_fp": "100.00",
                "volume_24h_fp": "200.00",
            },
            {
                "ticker": "KXEPLGAME-26AUG31ARSCHE-CHE",
                "event_ticker": "KXEPLGAME-26AUG31ARSCHE",
                "title": "Arsenal vs Chelsea",
                "close_time": "2026-08-31T18:00:00Z",
                "volume_fp": "150.00",
                "volume_24h_fp": "300.00",
            },
        ]
        game = build_soccer_game("26AUG31ARSCHE", markets)

        assert game is not None
        assert game.home_ml_ticker is not None
        assert game.away_ml_ticker is not None
        assert game.over_05_ticker is None
        assert game.over_15_ticker is None
        assert len(game.get_tickers()) == 2

    def test_empty_markets(self):
        """Test that empty markets returns None."""
        game = build_soccer_game("NOPE", [])
        assert game is None


class TestSoccerGame:
    """Tests for SoccerGame dataclass."""

    def test_get_tickers_full(self):
        game = SoccerGame(
            event_ticker="TEST",
            title="Test Game",
            home_team="Home",
            away_team="Away",
            close_time="2026-08-31T18:00:00Z",
            home_ml_ticker="ML-HOME",
            away_ml_ticker="ML-AWAY",
            over_05_ticker="TOTAL-1",
            over_15_ticker="TOTAL-2",
        )
        tickers = game.get_tickers()
        assert len(tickers) == 4
        assert "ML-HOME" in tickers
        assert "ML-AWAY" in tickers
        assert "TOTAL-1" in tickers
        assert "TOTAL-2" in tickers

    def test_get_tickers_partial(self):
        game = SoccerGame(
            event_ticker="TEST",
            title="Test Game",
            home_team="Home",
            away_team="Away",
            close_time="2026-08-31T18:00:00Z",
            home_ml_ticker="ML-HOME",
        )
        tickers = game.get_tickers()
        assert len(tickers) == 1
        assert tickers[0] == "ML-HOME"

    def test_has_volume_true(self):
        game = SoccerGame(
            event_ticker="TEST",
            title="Test Game",
            home_team="Home",
            away_team="Away",
            close_time="2026-08-31T18:00:00Z",
            total_volume=100.0,
            total_24h_volume=200.0,
        )
        assert game.has_volume is True

    def test_has_volume_false(self):
        game = SoccerGame(
            event_ticker="TEST",
            title="Test Game",
            home_team="Home",
            away_team="Away",
            close_time="2026-08-31T18:00:00Z",
            total_volume=10.0,
            total_24h_volume=20.0,
        )
        assert game.has_volume is False


class TestDiscoverSoccerGames:
    """Tests for discover_soccer_games with mocked API."""

    @patch("suspension_lab.soccer_discovery.fetch_open_soccer_markets")
    def test_discover_with_volume(self, mock_fetch):
        """Test discovery returns games with sufficient volume."""
        mock_fetch.return_value = [
            {
                "ticker": "KXEPLGAME-26SEP02ARSCHE-ARS",
                "event_ticker": "KXEPLGAME-26SEP02ARSCHE",
                "title": "Arsenal vs Chelsea",
                "close_time": "2026-09-02T18:00:00Z",
                "occurrence_datetime": "2026-09-02T14:00:00Z",
                "volume_fp": "100.00",
                "volume_24h_fp": "500.00",
            },
            {
                "ticker": "KXEPLGAME-26SEP02ARSCHE-CHE",
                "event_ticker": "KXEPLGAME-26SEP02ARSCHE",
                "title": "Arsenal vs Chelsea",
                "close_time": "2026-09-02T18:00:00Z",
                "occurrence_datetime": "2026-09-02T14:00:00Z",
                "volume_fp": "100.00",
                "volume_24h_fp": "500.00",
            },
            {
                "ticker": "KXEPLTOTAL-26SEP02ARSCHE-1",
                "event_ticker": "KXEPLTOTAL-26SEP02ARSCHE",
                "title": "Arsenal vs Chelsea O0.5",
                "close_time": "2026-09-02T18:00:00Z",
                "volume_fp": "50.00",
                "volume_24h_fp": "200.00",
                "yes_bid_dollars": "0.91",
                "yes_ask_dollars": "0.93",
            },
            {
                "ticker": "KXEPLTOTAL-26SEP02ARSCHE-2",
                "event_ticker": "KXEPLTOTAL-26SEP02ARSCHE",
                "title": "Arsenal vs Chelsea O1.5",
                "close_time": "2026-09-02T18:00:00Z",
                "volume_fp": "50.00",
                "volume_24h_fp": "200.00",
                "yes_bid_dollars": "0.70",
                "yes_ask_dollars": "0.72",
            },
            {
                "ticker": "KXEPLTOTAL-26SEP02ARSCHE-3",
                "event_ticker": "KXEPLTOTAL-26SEP02ARSCHE",
                "volume_fp": "80.00",
                "volume_24h_fp": "250.00",
                "yes_bid_dollars": "0.48",
                "yes_ask_dollars": "0.50",
            },
        ]

        now = datetime(2026, 9, 2, 15, 30, tzinfo=timezone.utc)
        result = discover_soccer_games(min_volume=50, min_24h_volume=100, now=now)

        assert len(result.games) == 1
        assert "KXEPLGAME-26SEP02ARSCHE-ARS" in result.tickers
        assert "KXEPLGAME-26SEP02ARSCHE-CHE" in result.tickers
        assert "KXEPLTOTAL-26SEP02ARSCHE-1" not in result.tickers
        assert "KXEPLTOTAL-26SEP02ARSCHE-3" in result.tickers

    @patch("suspension_lab.soccer_discovery.fetch_open_soccer_markets")
    def test_discover_no_markets(self, mock_fetch):
        """Test discovery with no open markets returns empty result."""
        mock_fetch.return_value = []

        result = discover_soccer_games()

        assert len(result.games) == 0
        assert len(result.tickers) == 0
        assert "No open soccer markets found" in "\n".join(result.log_lines)

    @patch("suspension_lab.soccer_discovery.fetch_open_soccer_markets")
    def test_discover_low_volume_filtered(self, mock_fetch):
        """Test that low volume games are filtered out."""
        mock_fetch.return_value = [
            {
                "ticker": "KXEPLGAME-26AUG31ARSCHE-ARS",
                "event_ticker": "KXEPLGAME-26AUG31ARSCHE",
                "title": "Arsenal vs Chelsea",
                "close_time": "2026-08-31T18:00:00Z",
                "volume_fp": "5.00",
                "volume_24h_fp": "10.00",
            },
        ]

        result = discover_soccer_games(min_volume=50, min_24h_volume=100)

        assert len(result.games) == 0
        assert len(result.tickers) == 0

    @patch("suspension_lab.soccer_discovery.fetch_open_soccer_markets")
    def test_discover_max_games_limit(self, mock_fetch):
        """Test that max_games limits the number of returned games."""
        markets = []
        for i in range(10):
            markets.extend([
                {
                    "ticker": f"KXEPLGAME-GAME{i}-HOME",
                    "event_ticker": f"KXEPLGAME-GAME{i}",
                    "title": f"Home vs Away {i}",
                    "close_time": "2026-09-05T18:00:00Z",
                    "occurrence_datetime": "2026-09-02T14:00:00Z",
                    "volume_fp": "100.00",
                    "volume_24h_fp": str(1000 - i * 100),
                },
                {
                    "ticker": f"KXEPLGAME-GAME{i}-AWAY",
                    "event_ticker": f"KXEPLGAME-GAME{i}",
                    "title": f"Home vs Away {i}",
                    "close_time": "2026-09-05T18:00:00Z",
                    "occurrence_datetime": "2026-09-02T14:00:00Z",
                    "volume_fp": "100.00",
                    "volume_24h_fp": str(1000 - i * 100),
                },
            ])
        mock_fetch.return_value = markets

        now = datetime(2026, 9, 2, 15, 0, tzinfo=timezone.utc)
        result = discover_soccer_games(max_games=3, now=now)

        assert len(result.games) == 3


class TestDiscoverTickersForLab:
    """Tests for the CLI convenience function."""

    @patch("suspension_lab.soccer_discovery.fetch_open_soccer_markets")
    def test_returns_tuple(self, mock_fetch):
        """Test that discover_tickers_for_lab returns correct tuple."""
        mock_fetch.return_value = [
            {
                "ticker": "KXEPLGAME-26AUG31ARSCHE-ARS",
                "event_ticker": "KXEPLGAME-26AUG31ARSCHE",
                "title": "Arsenal vs Chelsea",
                "close_time": "2026-08-31T18:00:00Z",
                "volume_fp": "100.00",
                "volume_24h_fp": "500.00",
            },
        ]

        tickers, log_msg, games = discover_tickers_for_lab()

        assert isinstance(tickers, list)
        assert isinstance(log_msg, str)
        assert isinstance(games, list)
        assert len(tickers) >= 0
        assert "Starting soccer discovery" in log_msg


class TestDiscoveryResultEdgeCases:
    """Edge case tests for discovery."""

    def test_discovery_result_defaults(self):
        result = DiscoveryResult(games=[], tickers=[], log_lines=[])
        assert result.discovered_at != ""

    @patch("suspension_lab.soccer_discovery.fetch_open_soccer_markets")
    def test_peruvian_league_tickers(self, mock_fetch):
        """Test that Peruvian league tickers are discovered correctly."""
        mock_fetch.return_value = [
            {
                "ticker": "KXPERLIGA1GAME-26SEP02CAGMEL-CAG",
                "event_ticker": "KXPERLIGA1GAME-26SEP02CAGMEL",
                "title": "Cajamarca vs Melgar",
                "close_time": "2026-09-02T18:00:00Z",
                "occurrence_datetime": "2026-09-02T14:00:00Z",
                "volume_fp": "100.00",
                "volume_24h_fp": "500.00",
            },
            {
                "ticker": "KXPERLIGA1GAME-26SEP02CAGMEL-MEL",
                "event_ticker": "KXPERLIGA1GAME-26SEP02CAGMEL",
                "title": "Cajamarca vs Melgar",
                "close_time": "2026-09-02T18:00:00Z",
                "occurrence_datetime": "2026-09-02T14:00:00Z",
                "volume_fp": "100.00",
                "volume_24h_fp": "500.00",
            },
            {
                "ticker": "KXPERLIGA1TOTAL-26SEP02CAGMEL-1",
                "event_ticker": "KXPERLIGA1TOTAL-26SEP02CAGMEL",
                "title": "Cajamarca vs Melgar O0.5",
                "close_time": "2026-09-02T18:00:00Z",
                "volume_fp": "50.00",
                "volume_24h_fp": "200.00",
                "yes_bid_dollars": "0.91",
                "yes_ask_dollars": "0.93",
            },
            {
                "ticker": "KXPERLIGA1TOTAL-26SEP02CAGMEL-2",
                "event_ticker": "KXPERLIGA1TOTAL-26SEP02CAGMEL",
                "title": "Cajamarca vs Melgar O1.5",
                "close_time": "2026-09-02T18:00:00Z",
                "volume_fp": "50.00",
                "volume_24h_fp": "200.00",
                "yes_bid_dollars": "0.48",
                "yes_ask_dollars": "0.50",
            },
            {
                "ticker": "KXPERLIGA1TOTAL-26SEP02CAGMEL-3",
                "event_ticker": "KXPERLIGA1TOTAL-26SEP02CAGMEL",
                "volume_fp": "40.00",
                "volume_24h_fp": "180.00",
                "yes_bid_dollars": "0.28",
                "yes_ask_dollars": "0.30",
            },
        ]

        result = discover_soccer_games(now=datetime(2026, 9, 2, 15, 30, tzinfo=timezone.utc))

        assert len(result.games) == 1
        game = result.games[0]
        assert "KXPERLIGA1" in game.home_ml_ticker
        assert game.total_atm_ticker == "KXPERLIGA1TOTAL-26SEP02CAGMEL-2"
        assert game.total_up_ticker == "KXPERLIGA1TOTAL-26SEP02CAGMEL-3"

    @patch("suspension_lab.soccer_discovery.fetch_open_soccer_markets")
    def test_brasileirao_tickers(self, mock_fetch):
        """Test that Brasileirão (Brazil Série A) tickers are discovered correctly."""
        mock_fetch.return_value = [
            {
                "ticker": "KXBRASILEIROGAME-26SEP02FLAMIR-FLA",
                "event_ticker": "KXBRASILEIROGAME-26SEP02FLAMIR",
                "title": "Flamengo vs Mirassol",
                "close_time": "2026-09-02T23:00:00Z",
                "occurrence_datetime": "2026-09-02T14:00:00Z",
                "volume_fp": "200.00",
                "volume_24h_fp": "800.00",
            },
            {
                "ticker": "KXBRASILEIROGAME-26SEP02FLAMIR-MIR",
                "event_ticker": "KXBRASILEIROGAME-26SEP02FLAMIR",
                "title": "Flamengo vs Mirassol",
                "close_time": "2026-09-02T23:00:00Z",
                "occurrence_datetime": "2026-09-02T14:00:00Z",
                "volume_fp": "150.00",
                "volume_24h_fp": "600.00",
            },
            {
                "ticker": "KXBRASILEIROTOTAL-26SEP02FLAMIR-1",
                "event_ticker": "KXBRASILEIROTOTAL-26SEP02FLAMIR",
                "title": "Flamengo vs Mirassol O0.5",
                "close_time": "2026-09-02T23:00:00Z",
                "volume_fp": "100.00",
                "volume_24h_fp": "400.00",
                "yes_bid_dollars": "0.95",
                "yes_ask_dollars": "0.97",
            },
            {
                "ticker": "KXBRASILEIROTOTAL-26SEP02FLAMIR-2",
                "event_ticker": "KXBRASILEIROTOTAL-26SEP02FLAMIR",
                "title": "Flamengo vs Mirassol O1.5",
                "close_time": "2026-09-02T23:00:00Z",
                "volume_fp": "80.00",
                "volume_24h_fp": "350.00",
                "yes_bid_dollars": "0.82",
                "yes_ask_dollars": "0.84",
            },
            {
                "ticker": "KXBRASILEIROTOTAL-26SEP02FLAMIR-4",
                "event_ticker": "KXBRASILEIROTOTAL-26SEP02FLAMIR",
                "volume_fp": "90.00",
                "volume_24h_fp": "300.00",
                "yes_bid_dollars": "0.49",
                "yes_ask_dollars": "0.51",
            },
            {
                "ticker": "KXBRASILEIROTOTAL-26SEP02FLAMIR-5",
                "event_ticker": "KXBRASILEIROTOTAL-26SEP02FLAMIR",
                "volume_fp": "70.00",
                "volume_24h_fp": "220.00",
                "yes_bid_dollars": "0.31",
                "yes_ask_dollars": "0.33",
            },
        ]

        result = discover_soccer_games(now=datetime(2026, 9, 2, 15, 30, tzinfo=timezone.utc))

        assert len(result.games) == 1
        game = result.games[0]
        assert game.home_ml_ticker == "KXBRASILEIROGAME-26SEP02FLAMIR-FLA"
        assert game.away_ml_ticker == "KXBRASILEIROGAME-26SEP02FLAMIR-MIR"
        assert game.total_atm_label == "O3.5"
        assert game.total_up_label == "O4.5"
        assert game.total_atm_ticker == "KXBRASILEIROTOTAL-26SEP02FLAMIR-4"
        assert "KXBRASILEIROTOTAL-26SEP02FLAMIR-1" not in game.get_tickers()

    @patch("suspension_lab.soccer_discovery.fetch_open_soccer_markets")
    def test_liga_mx_tickers(self, mock_fetch):
        """Test that Liga MX tickers are discovered correctly."""
        mock_fetch.return_value = [
            {
                "ticker": "KXLIGAMXGAME-26SEP06CRASLA-CRA",
                "event_ticker": "KXLIGAMXGAME-26SEP06CRASLA",
                "title": "Cruz Azul vs Santos Laguna",
                "close_time": "2026-09-06T02:00:00Z",
                "occurrence_datetime": "2026-09-06T00:30:00Z",
                "volume_fp": "500.00",
                "volume_24h_fp": "1200.00",
            },
            {
                "ticker": "KXLIGAMXGAME-26SEP06CRASLA-SLA",
                "event_ticker": "KXLIGAMXGAME-26SEP06CRASLA",
                "title": "Cruz Azul vs Santos Laguna",
                "close_time": "2026-09-06T02:00:00Z",
                "occurrence_datetime": "2026-09-06T00:30:00Z",
                "volume_fp": "450.00",
                "volume_24h_fp": "1100.00",
            },
            {
                "ticker": "KXLIGAMXTOTAL-26SEP06CRASLA-1",
                "event_ticker": "KXLIGAMXTOTAL-26SEP06CRASLA",
                "title": "Cruz Azul vs Santos Laguna O0.5",
                "close_time": "2026-09-06T02:00:00Z",
                "volume_fp": "50.00",
                "volume_24h_fp": "200.00",
                "yes_bid_dollars": "0.90",
                "yes_ask_dollars": "0.92",
            },
            {
                "ticker": "KXLIGAMXTOTAL-26SEP06CRASLA-2",
                "event_ticker": "KXLIGAMXTOTAL-26SEP06CRASLA",
                "title": "Cruz Azul vs Santos Laguna O1.5",
                "close_time": "2026-09-06T02:00:00Z",
                "volume_fp": "40.00",
                "volume_24h_fp": "180.00",
                "yes_bid_dollars": "0.47",
                "yes_ask_dollars": "0.49",
            },
        ]

        result = discover_soccer_games(now=datetime(2026, 9, 6, 1, 0, tzinfo=timezone.utc))

        assert len(result.games) == 1
        game = result.games[0]
        assert game.home_ml_ticker == "KXLIGAMXGAME-26SEP06CRASLA-CRA"
        assert game.away_ml_ticker == "KXLIGAMXGAME-26SEP06CRASLA-SLA"
        assert game.total_atm_ticker == "KXLIGAMXTOTAL-26SEP06CRASLA-2"
        assert game.total_up_ticker is None
        assert "KXLIGAMXTOTAL-26SEP06CRASLA-1" not in game.get_tickers()


def _tb(strike: int, yes: float | None, *, vol24: float = 200, liquid: bool = True) -> TotalBook:
    return TotalBook(
        strike=strike,
        ticker=f"KXTOTAL-GAME-{strike}",
        yes_price=yes,
        volume=vol24,
        volume_24h=vol24,
        liquid=liquid,
    )


class TestNearestFiftyTotals:
    """Totals = YES nearest 50¢ plus next strike up if liquid. No O0.5 default."""

    def test_strike_label(self):
        assert strike_to_over_label(1) == "O0.5"
        assert strike_to_over_label(3) == "O2.5"
        assert strike_to_over_label(4) == "O3.5"

    def test_skips_bonded_o05_picks_nearest_fifty(self):
        atm, up = select_scalp_totals([
            _tb(1, 0.91),
            _tb(2, 0.72),
            _tb(3, 0.48),
            _tb(4, 0.28),
        ])
        assert atm is not None and atm.strike == 3 and atm.label == "O2.5"
        assert up is not None and up.strike == 4 and up.label == "O3.5"

    def test_no_prices_does_not_default_o05_o15(self):
        atm, up = select_scalp_totals([
            _tb(1, None),
            _tb(2, None),
        ])
        assert atm is None
        assert up is None

    def test_all_bonds_funds_no_totals(self):
        atm, up = select_scalp_totals([_tb(1, 0.93), _tb(2, 0.89)])
        assert atm is None
        assert up is None

    def test_next_strike_skipped_if_illiquid(self):
        atm, up = select_scalp_totals([
            _tb(3, 0.51),
            _tb(4, 0.30, liquid=False, vol24=0),
        ])
        assert atm is not None and atm.strike == 3
        assert up is None

    def test_equal_distance_prefers_higher_volume(self):
        atm, _up = select_scalp_totals([
            _tb(2, 0.40, vol24=50),
            _tb(3, 0.60, vol24=800),
        ])
        assert atm is not None and atm.strike == 3

    def test_build_game_no_default_without_prices(self):
        markets = [
            {"ticker": "KXEPLGAME-X-ARS", "volume_fp": "100", "volume_24h_fp": "100"},
            {"ticker": "KXEPLGAME-X-CHE", "volume_fp": "100", "volume_24h_fp": "100"},
            {"ticker": "KXEPLTOTAL-X-1", "volume_fp": "100", "volume_24h_fp": "100"},
            {"ticker": "KXEPLTOTAL-X-2", "volume_fp": "100", "volume_24h_fp": "100"},
        ]
        game = build_soccer_game("X", markets)
        assert game is not None
        assert game.total_atm_ticker is None
        assert game.total_up_ticker is None
        assert game.get_tickers() == ["KXEPLGAME-X-ARS", "KXEPLGAME-X-CHE"]


class TestInGameTotalsRepick:
    """In-game totals come from live YES, not a frozen pregame O2.5."""

    def test_score_11_funds_o35_o45_not_pregame_o25(self):
        # Pregame ATM was O2.5 (~50¢). After 1-1 that book is 85¢.
        books = [
            _tb(1, 0.99),
            _tb(2, 0.99),
            _tb(3, 0.85),
            _tb(4, 0.52),
            _tb(5, 0.25),
        ]
        atm, up = select_ingame_totals(books, drop_far_wing=False)
        assert atm is not None and atm.strike == 4 and atm.label == "O3.5"
        assert up is not None and up.strike == 5 and up.label == "O4.5"

    def test_does_not_freeze_pregame_o25_when_reapplying(self):
        game = SoccerGame(
            event_ticker="KXCOPPAITALIAGAME-26SEP02SASFRO",
            title="Sassuolo vs Frosinone",
            home_team="Sassuolo",
            away_team="Frosinone",
            close_time="2026-09-02T18:00:00Z",
            total_atm_ticker="KXCOPPAITALIATOTAL-26SEP02SASFRO-3",
            total_atm_label="O2.5",
            total_atm_price=0.49,
            over_05_ticker="KXCOPPAITALIATOTAL-26SEP02SASFRO-3",
        )
        live = [
            TotalBook(1, "KXCOPPAITALIATOTAL-26SEP02SASFRO-1", 0.99, 100, 100, True),
            TotalBook(2, "KXCOPPAITALIATOTAL-26SEP02SASFRO-2", 0.99, 100, 100, True),
            TotalBook(3, "KXCOPPAITALIATOTAL-26SEP02SASFRO-3", 0.85, 100, 100, True),
            TotalBook(4, "KXCOPPAITALIATOTAL-26SEP02SASFRO-4", 0.51, 100, 100, True),
            TotalBook(5, "KXCOPPAITALIATOTAL-26SEP02SASFRO-5", 0.26, 100, 100, True),
        ]
        apply_live_totals(game, live, drop_far_wing=False)
        assert game.total_atm_label == "O3.5"
        assert game.total_up_label == "O4.5"
        assert game.total_atm_ticker.endswith("-4")
        assert game.in_play_hint is True
        assert "O2.5" not in (game.total_atm_label, game.total_up_label)

    def test_grind_drops_far_o45_to_o25_cheap_side(self):
        books = [
            _tb(1, 0.99),
            _tb(2, 0.99),
            _tb(3, 0.78),
            _tb(4, 0.48),
            _tb(5, 0.12),
        ]
        atm, wing = select_ingame_totals(books, drop_far_wing=True)
        assert atm is not None and atm.strike == 4
        assert wing is not None and wing.strike == 3 and wing.label == "O2.5"

    def test_grind_keeps_o45_when_still_near_fifty(self):
        books = [
            _tb(3, 0.80),
            _tb(4, 0.50),
            _tb(5, 0.36),
        ]
        atm, wing = select_ingame_totals(books, drop_far_wing=True)
        assert atm is not None and atm.strike == 4
        assert wing is not None and wing.strike == 5

    def test_does_not_drop_to_bonded_o25(self):
        books = [_tb(3, 0.91), _tb(4, 0.50), _tb(5, 0.10)]
        atm, wing = select_ingame_totals(books, drop_far_wing=True)
        assert atm is not None and atm.strike == 4
        assert wing is None or wing.strike == 5

    def test_skips_wide_mid_fifty_longshot(self):
        books = [
            TotalBook(3, "T-3", 0.73, 50, 50, True, spread=0.26),
            TotalBook(4, "T-4", 0.555, 50, 50, True, spread=0.13),
            TotalBook(5, "T-5", 0.335, 50, 50, True, spread=0.31),
            TotalBook(7, "T-7", 0.515, 50, 50, True, spread=0.87),
        ]
        atm, up = select_ingame_totals(books, drop_far_wing=False)
        assert atm is not None and atm.strike == 4
        assert up is not None and up.strike == 5

    def test_el_gouna_o15_at_fifty_not_junk_o35(self):
        """0-1 / 1-0 grind: O1.5 ~47/53 is ATM. O3.5 at 5¢ is junk — do not pin 3.5/4.5."""
        books = [
            _tb(1, 0.91),
            _tb(2, 0.50),
            _tb(3, 0.28),
            _tb(4, 0.05),
            _tb(5, 0.03),
        ]
        atm, up = select_ingame_totals(books, drop_far_wing=False)
        assert atm is not None and atm.strike == 2 and atm.label == "O1.5"
        assert up is not None and up.strike == 3 and up.label == "O2.5"
        assert atm.strike != 4
        assert up.strike not in {4, 5}

    def test_el_gouna_dead_o35_not_next_up(self):
        books = [
            _tb(2, 0.50),
            _tb(3, 0.05, liquid=True),
            _tb(4, 0.02),
        ]
        atm, up = select_scalp_totals(books)
        assert atm is not None and atm.strike == 2
        assert up is None

    def test_dead_wing_untradeable_and_missing_bid(self):
        dead = TotalBook(4, "T-4", 0.05, 80, 80, True, yes_bid=None, untradeable=True)
        junk = TotalBook(5, "T-5", 0.07, 80, 80, True, yes_bid=0.04)
        live = TotalBook(2, "T-2", 0.50, 80, 80, True, yes_bid=0.47)
        assert is_dead_wing(dead)
        assert is_dead_wing(junk)
        assert not is_dead_wing(live)
        atm, up = select_scalp_totals([live, dead, junk])
        assert atm is not None and atm.strike == 2
        assert up is None

    def test_o45_dead_swaps_to_o15_when_o25_also_junk(self):
        books = [
            _tb(1, 0.90),
            _tb(2, 0.48),
            _tb(3, 0.08),
            _tb(4, 0.51),
            _tb(5, 0.04),
        ]
        atm, wing = select_ingame_totals(books, drop_far_wing=False)
        assert atm is not None and atm.strike == 4
        assert wing is not None and wing.strike == 2 and wing.label == "O1.5"

    def test_score_11_is_atm_not_a_hard_pin(self):
        """When 4.5 is still the 50¢ tape after 1-1, fund 3.5/4.5 — that is ATM."""
        books = [
            _tb(1, 0.99),
            _tb(2, 0.99),
            _tb(3, 0.85),
            _tb(4, 0.52),
            _tb(5, 0.25),
        ]
        atm, up = select_ingame_totals(books, drop_far_wing=False)
        assert atm is not None and atm.strike == 4
        assert up is not None and up.strike == 5

    def test_build_game_live_11_sassuolo(self):
        markets = [
            {
                "ticker": "KXCOPPAITALIAGAME-26SEP02SASFRO-SAS",
                "volume_fp": "100",
                "volume_24h_fp": "100",
                "rules_primary": "If Sassuolo wins the Sassuolo vs Frosinone professional Coppa Italia soccer game",
            },
            {
                "ticker": "KXCOPPAITALIAGAME-26SEP02SASFRO-FRO",
                "volume_fp": "100",
                "volume_24h_fp": "100",
            },
            {
                "ticker": "KXCOPPAITALIATOTAL-26SEP02SASFRO-3",
                "volume_fp": "80",
                "volume_24h_fp": "80",
                "yes_bid_dollars": "0.82",
                "yes_ask_dollars": "0.88",
            },
            {
                "ticker": "KXCOPPAITALIATOTAL-26SEP02SASFRO-4",
                "volume_fp": "90",
                "volume_24h_fp": "90",
                "yes_bid_dollars": "0.50",
                "yes_ask_dollars": "0.55",
            },
            {
                "ticker": "KXCOPPAITALIATOTAL-26SEP02SASFRO-5",
                "volume_fp": "70",
                "volume_24h_fp": "70",
                "yes_bid_dollars": "0.23",
                "yes_ask_dollars": "0.28",
            },
        ]
        game = build_soccer_game("26SEP02SASFRO", markets)
        assert game is not None
        assert game.total_atm_label == "O3.5"
        assert game.total_up_label == "O4.5"
        assert "KXCOPPAITALIATOTAL-26SEP02SASFRO-3" not in game.get_tickers()


class TestElGounaSlateFundsO15:
    """Live El Gouna-like tape: O1.5 is the 50¢ book. Do not fund junk O3.5."""

    def _markets(self) -> list[dict]:
        return [
            {
                "ticker": "KXEGYPLGAME-26SEP02GOUMOK-GOU",
                "event_ticker": "KXEGYPLGAME-26SEP02GOUMOK",
                "title": "El Gouna vs Al Mokawloon",
                "close_time": "2026-09-02T20:00:00Z",
                "occurrence_datetime": "2026-09-02T15:00:00Z",
                "status": "open",
                "volume_fp": "4000",
                "volume_24h_fp": "8000",
                "rules_primary": "If El Gouna wins the El Gouna vs Al Mokawloon professional soccer game",
                "yes_bid_dollars": "0.40",
                "yes_ask_dollars": "0.42",
            },
            {
                "ticker": "KXEGYPLGAME-26SEP02GOUMOK-MOK",
                "event_ticker": "KXEGYPLGAME-26SEP02GOUMOK",
                "occurrence_datetime": "2026-09-02T15:00:00Z",
                "volume_fp": "3500",
                "volume_24h_fp": "7000",
                "yes_bid_dollars": "0.30",
                "yes_ask_dollars": "0.32",
            },
            {
                "ticker": "KXEGYPLTOTAL-26SEP02GOUMOK-1",
                "event_ticker": "KXEGYPLTOTAL-26SEP02GOUMOK",
                "occurrence_datetime": "2026-09-02T15:00:00Z",
                "volume_fp": "900",
                "volume_24h_fp": "1800",
                "yes_bid_dollars": "0.90",
                "yes_ask_dollars": "0.93",
            },
            {
                "ticker": "KXEGYPLTOTAL-26SEP02GOUMOK-2",
                "event_ticker": "KXEGYPLTOTAL-26SEP02GOUMOK",
                "occurrence_datetime": "2026-09-02T15:00:00Z",
                "volume_fp": "2200",
                "volume_24h_fp": "4400",
                "yes_bid_dollars": "0.47",
                "yes_ask_dollars": "0.53",
            },
            {
                "ticker": "KXEGYPLTOTAL-26SEP02GOUMOK-3",
                "event_ticker": "KXEGYPLTOTAL-26SEP02GOUMOK",
                "occurrence_datetime": "2026-09-02T15:00:00Z",
                "volume_fp": "1500",
                "volume_24h_fp": "3000",
                "yes_bid_dollars": "0.22",
                "yes_ask_dollars": "0.26",
            },
            {
                "ticker": "KXEGYPLTOTAL-26SEP02GOUMOK-4",
                "event_ticker": "KXEGYPLTOTAL-26SEP02GOUMOK",
                "occurrence_datetime": "2026-09-02T15:00:00Z",
                "volume_fp": "800",
                "volume_24h_fp": "1600",
                "yes_bid_dollars": "0.04",
                "yes_ask_dollars": "0.07",
            },
            {
                "ticker": "KXEGYPLTOTAL-26SEP02GOUMOK-5",
                "event_ticker": "KXEGYPLTOTAL-26SEP02GOUMOK",
                "occurrence_datetime": "2026-09-02T15:00:00Z",
                "volume_fp": "400",
                "volume_24h_fp": "700",
                "yes_bid_dollars": "0.01",
                "yes_ask_dollars": "0.03",
            },
        ]

    def test_build_funds_o15_not_o35(self):
        game = build_soccer_game("26SEP02GOUMOK", self._markets())
        assert game is not None
        assert game.total_atm_label == "O1.5"
        assert game.total_atm_ticker.endswith("-2")
        assert game.total_up_label == "O2.5"
        tickers = game.get_tickers()
        assert "KXEGYPLTOTAL-26SEP02GOUMOK-2" in tickers
        assert "KXEGYPLTOTAL-26SEP02GOUMOK-4" not in tickers
        assert "KXEGYPLTOTAL-26SEP02GOUMOK-5" not in tickers

    @patch("suspension_lab.soccer_discovery.fetch_open_soccer_markets")
    def test_discover_el_gouna_slate(self, mock_fetch):
        mock_fetch.return_value = self._markets()
        now = datetime(2026, 9, 2, 15, 40, tzinfo=timezone.utc)
        result = discover_soccer_games(max_games=5, now=now)
        assert len(result.games) == 1
        game = result.games[0]
        assert game.total_atm_label == "O1.5"
        assert "KXEGYPLTOTAL-26SEP02GOUMOK-2" in result.tickers
        assert "KXEGYPLTOTAL-26SEP02GOUMOK-4" not in result.tickers
        assert "KXEGYPLTOTAL-26SEP02GOUMOK-5" not in result.tickers


class TestRepickDropsDeadWings:
    def test_unfunded_tickers_are_the_diff(self):
        assert unfunded_tickers(["ML-H", "T-4", "T-5"], ["ML-H", "T-2", "T-3"]) == ["T-4", "T-5"]

    def test_session_repick_drops_o35_when_o15_is_atm(self):
        stuck = SoccerGame(
            event_ticker="KXEGYPLGAME-26SEP02GOUMOK",
            title="El Gouna vs Al Mokawloon",
            home_team="El Gouna",
            away_team="Al Mokawloon",
            close_time="2026-09-02T20:00:00Z",
            occurrence_time="2026-09-02T15:00:00Z",
            home_ml_ticker="KXEGYPLGAME-26SEP02GOUMOK-GOU",
            away_ml_ticker="KXEGYPLGAME-26SEP02GOUMOK-MOK",
            total_atm_ticker="KXEGYPLTOTAL-26SEP02GOUMOK-4",
            total_atm_label="O3.5",
            total_atm_price=0.52,
            total_up_ticker="KXEGYPLTOTAL-26SEP02GOUMOK-5",
            total_up_label="O4.5",
            total_up_price=0.25,
            over_05_ticker="KXEGYPLTOTAL-26SEP02GOUMOK-4",
            over_15_ticker="KXEGYPLTOTAL-26SEP02GOUMOK-5",
        )
        live = SoccerGame(
            event_ticker="KXEGYPLGAME-26SEP02GOUMOK",
            title="El Gouna vs Al Mokawloon",
            home_team="El Gouna",
            away_team="Al Mokawloon",
            close_time="2026-09-02T20:00:00Z",
            occurrence_time="2026-09-02T15:00:00Z",
            home_ml_ticker="KXEGYPLGAME-26SEP02GOUMOK-GOU",
            away_ml_ticker="KXEGYPLGAME-26SEP02GOUMOK-MOK",
            total_books=[
                TotalBook(1, "KXEGYPLTOTAL-26SEP02GOUMOK-1", 0.91, 100, 100, True),
                TotalBook(2, "KXEGYPLTOTAL-26SEP02GOUMOK-2", 0.50, 200, 200, True, yes_bid=0.47),
                TotalBook(3, "KXEGYPLTOTAL-26SEP02GOUMOK-3", 0.24, 150, 150, True),
                TotalBook(4, "KXEGYPLTOTAL-26SEP02GOUMOK-4", 0.05, 80, 80, True, yes_bid=0.04, untradeable=False),
                TotalBook(5, "KXEGYPLTOTAL-26SEP02GOUMOK-5", 0.02, 40, 40, True, yes_bid=None, untradeable=True),
            ],
        )
        now = datetime(2026, 9, 2, 15, 45, tzinfo=timezone.utc)
        kept, fund, drop = repick_session_totals([stuck], [live], drop_far_wing=False, now=now)
        assert len(kept) == 1
        assert kept[0].total_atm_label == "O1.5"
        assert "KXEGYPLTOTAL-26SEP02GOUMOK-2" in fund
        assert "KXEGYPLTOTAL-26SEP02GOUMOK-4" in drop
        assert "KXEGYPLTOTAL-26SEP02GOUMOK-5" in drop
        assert "KXEGYPLTOTAL-26SEP02GOUMOK-4" not in fund
        assert "KXEGYPLGAME-26SEP02GOUMOK-GOU" in fund


class TestGreekPrefixesNoTeamBias:
    def test_greek_and_egypt_tff_prefixes_are_boost_only(self):
        for series in (
            "KXSLGREECEGAME",
            "KXSLGREECETOTAL",
            "KXGRECUPGAME",
            "KXGRECUPTOTAL",
            "KXEGYPLGAME",
            "KXEGYPLTOTAL",
            "KXTFF1LIGGAME",
            "KXTFF1LIGTOTAL",
        ):
            assert series in SOCCER_SERIES_PREFIXES
        assert "KXSLGREECEGAME" in SERIES_WITH_GAMES
        assert "KXGRECUPTOTAL" in SERIES_WITH_TOTALS
        assert "KXEGYPLGAME" in SERIES_WITH_GAMES
        assert "KXTFF1LIGTOTAL" in SERIES_WITH_TOTALS

    @patch("suspension_lab.soccer_discovery.fetch_open_soccer_markets")
    def test_low_volume_aek_is_not_force_funded(self, mock_fetch):
        markets = []
        now_occ = "2026-09-02T14:00:00Z"
        for i in range(5):
            markets.extend(
                [
                    {
                        "ticker": f"KXEPLGAME-26SEP02VOL{i}-HOM",
                        "event_ticker": f"KXEPLGAME-26SEP02VOL{i}",
                        "title": f"Volume Club {i} vs Other",
                        "close_time": "2026-09-05T01:00:00Z",
                        "occurrence_datetime": now_occ,
                        "volume_fp": "90000",
                        "volume_24h_fp": str(200000 - i),
                    },
                    {
                        "ticker": f"KXEPLGAME-26SEP02VOL{i}-AWY",
                        "event_ticker": f"KXEPLGAME-26SEP02VOL{i}",
                        "title": f"Volume Club {i} vs Other",
                        "occurrence_datetime": now_occ,
                        "volume_fp": "90000",
                        "volume_24h_fp": str(200000 - i),
                    },
                ]
            )
        markets.extend(
            [
                {
                    "ticker": "KXGRECUPGAME-26SEP02NCHAEK-AEK",
                    "event_ticker": "KXGRECUPGAME-26SEP02NCHAEK",
                    "title": "Chrysoupoli vs AEK Athens",
                    "close_time": "2026-09-05T01:00:00Z",
                    "occurrence_datetime": now_occ,
                    "volume_fp": "20",
                    "volume_24h_fp": "30",
                    "rules_primary": "If AEK Athens wins the Chrysoupoli vs AEK Athens professional soccer game",
                },
                {
                    "ticker": "KXGRECUPGAME-26SEP02NCHAEK-NCH",
                    "event_ticker": "KXGRECUPGAME-26SEP02NCHAEK",
                    "title": "Chrysoupoli vs AEK Athens",
                    "occurrence_datetime": now_occ,
                    "volume_fp": "10",
                    "volume_24h_fp": "20",
                },
            ]
        )
        mock_fetch.return_value = markets
        now = datetime(2026, 9, 2, 14, 10, tzinfo=timezone.utc)
        result = discover_soccer_games(max_games=5, now=now, min_volume=50, min_24h_volume=100)
        titles = " ".join(g.title for g in result.games)
        assert "AEK" not in titles
        assert not any("NCHAEK" in t for t in result.tickers)
        assert len(result.games) == 5

    @patch("suspension_lab.soccer_discovery.fetch_open_soccer_markets")
    def test_does_not_pin_next_week_sassuolo(self, mock_fetch):
        mock_fetch.return_value = [
            {
                "ticker": "KXSERIEAGAME-26SEP06BFCSAS-SAS",
                "event_ticker": "KXSERIEAGAME-26SEP06BFCSAS",
                "title": "Bologna vs Sassuolo",
                "close_time": "2026-09-09T01:00:00Z",
                "occurrence_datetime": "2026-09-06T19:00:00Z",
                "volume_fp": "100",
                "volume_24h_fp": "100",
                "yes_bid_dollars": "0.24",
                "yes_ask_dollars": "0.25",
            },
            {
                "ticker": "KXSERIEAGAME-26SEP06BFCSAS-BFC",
                "event_ticker": "KXSERIEAGAME-26SEP06BFCSAS",
                "title": "Bologna vs Sassuolo",
                "occurrence_datetime": "2026-09-06T19:00:00Z",
                "volume_fp": "100",
                "volume_24h_fp": "100",
            },
            {
                "ticker": "KXSERIEATOTAL-26SEP06BFCSAS-1",
                "event_ticker": "KXSERIEATOTAL-26SEP06BFCSAS",
                "occurrence_datetime": "2026-09-06T19:00:00Z",
                "volume_fp": "50",
                "volume_24h_fp": "50",
                "yes_bid_dollars": "0.92",
                "yes_ask_dollars": "0.93",
            },
        ]
        now = datetime(2026, 9, 2, 14, 10, tzinfo=timezone.utc)
        result = discover_soccer_games(max_games=5, now=now)
        assert result.games == []
        assert result.tickers == []


class TestStaleEnvAndFingerprint:
    """Stale .env pins, Egypt/TFF without prefix, finished Coppa."""

    def test_stale_melgar_env_needs_auto_discover(self):
        now = datetime(2026, 9, 2, 15, 0, tzinfo=timezone.utc)
        melgar = "KXPERLIGA1GAME-26AUG31CAGMEL-MEL"
        assert is_stale_lab_ticker(melgar, now=now)
        assert needs_auto_discover([melgar], now=now)
        assert needs_auto_discover(
            [melgar, "KXPERLIGA1GAME-26AUG31CAGMEL-CAG", "KXPERLIGA1TOTAL-26AUG31CAGMEL-4"],
            now=now,
        )
        assert parse_cli_tickers("") == []
        assert parse_cli_tickers("auto") == []

    def test_today_explicit_kx_can_pin(self):
        now = datetime(2026, 9, 2, 15, 0, tzinfo=timezone.utc)
        assert not needs_auto_discover(["KXEGYPLGAME-26SEP02GOUMOK-GOU"], now=now)

    def test_egypt_tff_fingerprint_without_prefix(self, monkeypatch):
        from suspension_lab import soccer_discovery as sd

        monkeypatch.setattr(
            sd,
            "SOCCER_SERIES_PREFIXES",
            tuple(p for p in sd.SOCCER_SERIES_PREFIXES if "EGYPL" not in p and "TFF" not in p),
        )
        egypt = {
            "ticker": "KXEGYPLGAME-26SEP02GOUMOK-GOU",
            "series_ticker": "KXEGYPLGAME",
            "title": "El Gouna vs Al Mokawloon",
            "yes_sub_title": "El Gouna wins",
            "rules_primary": "If El Gouna wins the El Gouna vs Al Mokawloon professional soccer game",
        }
        turkey = {
            "ticker": "KXTFF1LIGGAME-26SEP02VASBAT-VAS",
            "series_ticker": "KXTFF1LIGGAME",
            "title": "Van Spor vs Batman Petrolspor",
            "subtitle": "goals scored",
        }
        nfl = {
            "ticker": "KXNFLGAME-26SEP02SH-KC",
            "series_ticker": "KXNFLGAME",
            "title": "Chiefs vs Bills",
            "subtitle": "NFL moneyline",
        }
        assert is_soccer_series_ticker("KXEGYPLGAME")
        assert is_soccer_series_ticker("KXTFF1LIGTOTAL")
        assert not is_soccer_series_ticker("KXNFLGAME")
        assert looks_like_soccer_market(egypt)
        assert looks_like_soccer_market(turkey)
        assert not looks_like_soccer_market(nfl)
        kept = {m["ticker"] for m in filter_soccer_markets([egypt, turkey, nfl])}
        assert "KXEGYPLGAME-26SEP02GOUMOK-GOU" in kept
        assert "KXTFF1LIGGAME-26SEP02VASBAT-VAS" in kept
        assert "KXNFLGAME-26SEP02SH-KC" not in kept

    def test_catalog_soccer_tag_includes_egypt_tff(self):
        rows = [
            {"ticker": "KXEGYPLGAME", "title": "Egyptian Premier League", "tags": ["Soccer"]},
            {"ticker": "KXTFF1LIGTOTAL", "title": "TFF 1. Lig totals", "tags": ["Soccer"]},
            {"ticker": "KXNFLGAME", "title": "NFL", "tags": ["Football"]},
            {"ticker": "KXEGYPLGAME", "title": "delete me", "tags": ["Soccer"]},
        ]
        got = soccer_series_tickers_from_catalog(rows)
        assert "KXEGYPLGAME" in got
        assert "KXTFF1LIGTOTAL" in got
        assert "KXNFLGAME" not in got

    @patch("suspension_lab.soccer_discovery.fetch_open_soccer_markets")
    def test_egypt_and_tff_discovered_if_live(self, mock_fetch):
        mock_fetch.return_value = [
            {
                "ticker": "KXEGYPLGAME-26SEP02GOUMOK-GOU",
                "event_ticker": "KXEGYPLGAME-26SEP02GOUMOK",
                "title": "El Gouna vs Al Mokawloon",
                "close_time": "2026-09-02T20:00:00Z",
                "occurrence_datetime": "2026-09-02T15:00:00Z",
                "status": "open",
                "volume_fp": "4000",
                "volume_24h_fp": "8000",
                "rules_primary": "If El Gouna wins the El Gouna vs Al Mokawloon professional soccer game",
                "yes_bid_dollars": "0.40",
                "yes_ask_dollars": "0.42",
            },
            {
                "ticker": "KXEGYPLGAME-26SEP02GOUMOK-MOK",
                "event_ticker": "KXEGYPLGAME-26SEP02GOUMOK",
                "occurrence_datetime": "2026-09-02T15:00:00Z",
                "volume_fp": "3500",
                "volume_24h_fp": "7000",
            },
            {
                "ticker": "KXEGYPLTOTAL-26SEP02GOUMOK-3",
                "event_ticker": "KXEGYPLTOTAL-26SEP02GOUMOK",
                "occurrence_datetime": "2026-09-02T15:00:00Z",
                "volume_fp": "2000",
                "volume_24h_fp": "4000",
                "yes_bid_dollars": "0.49",
                "yes_ask_dollars": "0.51",
            },
            {
                "ticker": "KXEGYPLTOTAL-26SEP02GOUMOK-4",
                "event_ticker": "KXEGYPLTOTAL-26SEP02GOUMOK",
                "occurrence_datetime": "2026-09-02T15:00:00Z",
                "volume_fp": "1800",
                "volume_24h_fp": "3600",
                "yes_bid_dollars": "0.31",
                "yes_ask_dollars": "0.33",
            },
            {
                "ticker": "KXTFF1LIGGAME-26SEP02VASBAT-VAS",
                "event_ticker": "KXTFF1LIGGAME-26SEP02VASBAT",
                "title": "Van vs Batman",
                "occurrence_datetime": "2026-09-02T14:30:00Z",
                "status": "open",
                "volume_fp": "3000",
                "volume_24h_fp": "6000",
                "rules_primary": "If Van wins the Van vs Batman professional soccer game",
            },
            {
                "ticker": "KXTFF1LIGGAME-26SEP02VASBAT-BAT",
                "event_ticker": "KXTFF1LIGGAME-26SEP02VASBAT",
                "occurrence_datetime": "2026-09-02T14:30:00Z",
                "volume_fp": "2800",
                "volume_24h_fp": "5500",
            },
            {
                "ticker": "KXTFF1LIGTOTAL-26SEP02VASBAT-3",
                "event_ticker": "KXTFF1LIGTOTAL-26SEP02VASBAT",
                "occurrence_datetime": "2026-09-02T14:30:00Z",
                "volume_fp": "1500",
                "volume_24h_fp": "3000",
                "yes_bid_dollars": "0.50",
                "yes_ask_dollars": "0.52",
            },
            {
                "ticker": "KXTFF1LIGTOTAL-26SEP02VASBAT-4",
                "event_ticker": "KXTFF1LIGTOTAL-26SEP02VASBAT",
                "occurrence_datetime": "2026-09-02T14:30:00Z",
                "volume_fp": "1400",
                "volume_24h_fp": "2800",
                "yes_bid_dollars": "0.32",
                "yes_ask_dollars": "0.34",
            },
        ]
        now = datetime(2026, 9, 2, 15, 20, tzinfo=timezone.utc)
        result = discover_soccer_games(max_games=5, now=now)
        titles = " ".join(g.title for g in result.games)
        assert "Gouna" in titles or "Mokawloon" in titles
        assert "Van" in titles or "Batman" in titles
        assert any("GOUMOK" in t for t in result.tickers)
        assert any("VASBAT" in t for t in result.tickers)
        assert any(t.endswith("-3") and "GOUMOK" in t for t in result.tickers)
        assert any(t.endswith("-4") and "GOUMOK" in t for t in result.tickers)

    @patch("suspension_lab.soccer_discovery.fetch_open_soccer_markets")
    def test_finished_coppa_sasfro_not_selected(self, mock_fetch):
        mock_fetch.return_value = [
            {
                "ticker": "KXCOPPAITALIAGAME-26SEP02SASFRO-SAS",
                "event_ticker": "KXCOPPAITALIAGAME-26SEP02SASFRO",
                "title": "Sassuolo vs Frosinone",
                "close_time": "2026-09-05T01:00:00Z",
                "occurrence_datetime": "2026-09-02T16:00:00Z",
                "status": "closed",
                "volume_fp": "90000",
                "volume_24h_fp": "200000",
                "rules_primary": "If Sassuolo wins the Sassuolo vs Frosinone professional Coppa Italia soccer game",
            },
            {
                "ticker": "KXCOPPAITALIAGAME-26SEP02SASFRO-FRO",
                "event_ticker": "KXCOPPAITALIAGAME-26SEP02SASFRO",
                "occurrence_datetime": "2026-09-02T16:00:00Z",
                "status": "closed",
                "volume_fp": "80000",
                "volume_24h_fp": "180000",
            },
            {
                "ticker": "KXEGYPLGAME-26SEP02GOUMOK-GOU",
                "event_ticker": "KXEGYPLGAME-26SEP02GOUMOK",
                "title": "El Gouna vs Al Mokawloon",
                "occurrence_datetime": "2026-09-02T18:00:00Z",
                "status": "open",
                "volume_fp": "4000",
                "volume_24h_fp": "8000",
                "rules_primary": "If El Gouna wins the El Gouna vs Al Mokawloon professional soccer game",
            },
            {
                "ticker": "KXEGYPLGAME-26SEP02GOUMOK-MOK",
                "event_ticker": "KXEGYPLGAME-26SEP02GOUMOK",
                "occurrence_datetime": "2026-09-02T18:00:00Z",
                "status": "open",
                "volume_fp": "3500",
                "volume_24h_fp": "7000",
            },
        ]
        now = datetime(2026, 9, 2, 19, 10, tzinfo=timezone.utc)
        result = discover_soccer_games(max_games=5, now=now)
        titles = " ".join(g.title for g in result.games)
        assert "Sassuolo" not in titles
        assert not any("SASFRO" in t for t in result.tickers)
        assert any("GOUMOK" in t for t in result.tickers)

    @patch("suspension_lab.soccer_discovery.fetch_open_soccer_markets")
    def test_yesterday_grau_melgar_never_selected(self, mock_fetch):
        mock_fetch.return_value = [
            {
                "ticker": "KXPERLIGA1GAME-26AUG31CAGMEL-MEL",
                "event_ticker": "KXPERLIGA1GAME-26AUG31CAGMEL",
                "title": "Carlos A. Mannucci vs Melgar",
                "close_time": "2026-09-01T02:00:00Z",
                "occurrence_datetime": "2026-08-31T20:00:00Z",
                "status": "settled",
                "volume_fp": "999999",
                "volume_24h_fp": "999999",
                "rules_primary": "If Melgar wins the Grau vs Melgar professional soccer game",
            },
            {
                "ticker": "KXPERLIGA1GAME-26AUG31CAGMEL-CAG",
                "event_ticker": "KXPERLIGA1GAME-26AUG31CAGMEL",
                "occurrence_datetime": "2026-08-31T20:00:00Z",
                "status": "settled",
                "volume_fp": "900000",
                "volume_24h_fp": "900000",
            },
        ]
        now = datetime(2026, 9, 2, 15, 0, tzinfo=timezone.utc)
        result = discover_soccer_games(max_games=5, now=now)
        assert result.games == []
        assert result.tickers == []
        assert not any("CAGMEL" in t for t in result.tickers)

    def test_finished_by_kickoff_age_without_in_play_hint(self):
        now = datetime(2026, 9, 2, 19, 0, tzinfo=timezone.utc)
        game = SoccerGame(
            event_ticker="KXCOPPAITALIAGAME-26SEP02SASFRO",
            title="Sassuolo vs Frosinone",
            home_team="Sassuolo",
            away_team="Frosinone",
            close_time="2026-09-05T01:00:00Z",
            occurrence_time="2026-09-02T16:00:00Z",
            status="open",
            in_play_hint=False,
        )
        assert is_finished_game(game, now=now)

    def test_liquid_tie_is_funded(self):
        markets = [
            {
                "ticker": "KXEGYPLGAME-26SEP02GOUMOK-GOU",
                "volume_fp": "100",
                "volume_24h_fp": "100",
                "yes_bid_dollars": "0.40",
                "yes_ask_dollars": "0.42",
            },
            {
                "ticker": "KXEGYPLGAME-26SEP02GOUMOK-MOK",
                "volume_fp": "100",
                "volume_24h_fp": "100",
                "yes_bid_dollars": "0.30",
                "yes_ask_dollars": "0.32",
            },
            {
                "ticker": "KXEGYPLGAME-26SEP02GOUMOK-TIE",
                "volume_fp": "80",
                "volume_24h_fp": "80",
                "yes_bid_dollars": "0.26",
                "yes_ask_dollars": "0.28",
            },
        ]
        game = build_soccer_game("26SEP02GOUMOK", markets)
        assert game is not None
        assert game.tie_ml_ticker == "KXEGYPLGAME-26SEP02GOUMOK-TIE"
        assert "TIE" not in (game.home_ml_ticker or "")
        assert game.tie_ml_ticker in game.get_tickers()


class TestLiveOnlySeats:
    def _game(self, ticker: str, title: str, kick: str, **kwargs) -> SoccerGame:
        return SoccerGame(
            event_ticker=ticker,
            title=title,
            home_team=title.split(" vs ")[0],
            away_team=title.split(" vs ")[-1],
            close_time="",
            occurrence_time=kick,
            home_ml_ticker=f"{ticker}-H",
            away_ml_ticker=f"{ticker}-A",
            **kwargs,
        )

    def test_pregame_not_funded_in_play_coppa_is(self):
        now = datetime(2026, 9, 2, 16, 30, tzinfo=timezone.utc)
        live = self._game(
            "KXCOPPAITALIAGAME-26SEP02UDIVEN",
            "Udinese vs Venezia",
            "2026-09-02T15:00:00Z",
        )
        pre = self._game(
            "KXEPLGAME-26SEP02ARSLIV",
            "Arsenal vs Liverpool",
            "2026-09-02T19:00:00Z",
        )
        done = self._game(
            "KXEPLGAME-26SEP02OLD",
            "Finished vs Match",
            "2026-09-02T10:00:00Z",
        )
        assert is_in_play(live, now=now)
        assert should_fund_live(live, now=now)
        assert is_pregame(pre, now=now)
        assert not should_fund_live(pre, now=now)
        assert is_finished_game(done, now=now)
        assert not should_fund_live(done, now=now)

    def test_repick_drops_pregame_keeps_live_adds_newly_live(self):
        now = datetime(2026, 9, 2, 16, 30, tzinfo=timezone.utc)
        seated_live = self._game(
            "KXCOPPAITALIAGAME-26SEP02UDIVEN",
            "Udinese vs Venezia",
            "2026-09-02T15:00:00Z",
        )
        seated_pre = self._game(
            "KXEPLGAME-26SEP02NEXTEPL",
            "Later vs Kickoff",
            "2026-09-02T19:30:00Z",
        )
        newly_live = self._game(
            "KXCOPPAITALIAGAME-26SEP02NEWCOP",
            "New vs Live",
            "2026-09-02T16:00:00Z",
        )
        kept, fund, drop = repick_session_totals(
            [seated_live, seated_pre],
            [seated_live, newly_live],
            now=now,
        )
        titles = [g.title for g in kept]
        assert any("Udinese" in t for t in titles)
        assert any("New vs Live" in t for t in titles)
        assert not any("Later vs Kickoff" in t for t in titles)
        assert seated_pre.home_ml_ticker in drop
        assert seated_live.home_ml_ticker in fund
        assert newly_live.home_ml_ticker in fund
