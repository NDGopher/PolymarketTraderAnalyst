"""Tests for soccer auto-discovery from Kalshi API."""

import pytest
from unittest.mock import patch, MagicMock

from suspension_lab.soccer_discovery import (
    SoccerGame,
    DiscoveryResult,
    _parse_volume,
    _extract_teams_from_title,
    _match_game_ticker,
    _match_total_ticker,
    _get_event_identifier,
    group_markets_by_event,
    build_soccer_game,
    discover_soccer_games,
    discover_tickers_for_lab,
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
            },
            {
                "ticker": "KXEPLTOTAL-26AUG31ARSCHE-2",
                "event_ticker": "KXEPLTOTAL-26AUG31ARSCHE",
                "title": "Arsenal vs Chelsea O1.5 Goals",
                "close_time": "2026-08-31T18:00:00Z",
                "volume_fp": "75.00",
                "volume_24h_fp": "125.00",
            },
        ]
        game = build_soccer_game("26AUG31ARSCHE", markets)

        assert game is not None
        assert game.home_ml_ticker == "KXEPLGAME-26AUG31ARSCHE-ARS"
        assert game.away_ml_ticker == "KXEPLGAME-26AUG31ARSCHE-CHE"
        assert game.over_05_ticker == "KXEPLTOTAL-26AUG31ARSCHE-1"
        assert game.over_15_ticker == "KXEPLTOTAL-26AUG31ARSCHE-2"
        assert game.total_volume == 375.0
        assert game.total_24h_volume == 725.0
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
                "ticker": "KXEPLGAME-26AUG31ARSCHE-ARS",
                "event_ticker": "KXEPLGAME-26AUG31ARSCHE",
                "title": "Arsenal vs Chelsea",
                "close_time": "2026-08-31T18:00:00Z",
                "volume_fp": "100.00",
                "volume_24h_fp": "500.00",
            },
            {
                "ticker": "KXEPLGAME-26AUG31ARSCHE-CHE",
                "event_ticker": "KXEPLGAME-26AUG31ARSCHE",
                "title": "Arsenal vs Chelsea",
                "close_time": "2026-08-31T18:00:00Z",
                "volume_fp": "100.00",
                "volume_24h_fp": "500.00",
            },
            {
                "ticker": "KXEPLTOTAL-26AUG31ARSCHE-1",
                "event_ticker": "KXEPLTOTAL-26AUG31ARSCHE",
                "title": "Arsenal vs Chelsea O0.5",
                "close_time": "2026-08-31T18:00:00Z",
                "volume_fp": "50.00",
                "volume_24h_fp": "200.00",
            },
            {
                "ticker": "KXEPLTOTAL-26AUG31ARSCHE-2",
                "event_ticker": "KXEPLTOTAL-26AUG31ARSCHE",
                "title": "Arsenal vs Chelsea O1.5",
                "close_time": "2026-08-31T18:00:00Z",
                "volume_fp": "50.00",
                "volume_24h_fp": "200.00",
            },
        ]

        result = discover_soccer_games(min_volume=50, min_24h_volume=100)

        assert len(result.games) == 1
        assert len(result.tickers) == 4
        assert "KXEPLGAME-26AUG31ARSCHE-ARS" in result.tickers
        assert "KXEPLGAME-26AUG31ARSCHE-CHE" in result.tickers
        assert "KXEPLTOTAL-26AUG31ARSCHE-1" in result.tickers
        assert "KXEPLTOTAL-26AUG31ARSCHE-2" in result.tickers

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
                    "close_time": "2026-08-31T18:00:00Z",
                    "volume_fp": "100.00",
                    "volume_24h_fp": str(1000 - i * 100),
                },
                {
                    "ticker": f"KXEPLGAME-GAME{i}-AWAY",
                    "event_ticker": f"KXEPLGAME-GAME{i}",
                    "title": f"Home vs Away {i}",
                    "close_time": "2026-08-31T18:00:00Z",
                    "volume_fp": "100.00",
                    "volume_24h_fp": str(1000 - i * 100),
                },
            ])
        mock_fetch.return_value = markets

        result = discover_soccer_games(max_games=3)

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
                "ticker": "KXPERLIGA1GAME-26AUG31CAGMEL-CAG",
                "event_ticker": "KXPERLIGA1GAME-26AUG31CAGMEL",
                "title": "Cajamarca vs Melgar",
                "close_time": "2026-08-31T18:00:00Z",
                "volume_fp": "100.00",
                "volume_24h_fp": "500.00",
            },
            {
                "ticker": "KXPERLIGA1GAME-26AUG31CAGMEL-MEL",
                "event_ticker": "KXPERLIGA1GAME-26AUG31CAGMEL",
                "title": "Cajamarca vs Melgar",
                "close_time": "2026-08-31T18:00:00Z",
                "volume_fp": "100.00",
                "volume_24h_fp": "500.00",
            },
            {
                "ticker": "KXPERLIGA1TOTAL-26AUG31CAGMEL-1",
                "event_ticker": "KXPERLIGA1TOTAL-26AUG31CAGMEL",
                "title": "Cajamarca vs Melgar O0.5",
                "close_time": "2026-08-31T18:00:00Z",
                "volume_fp": "50.00",
                "volume_24h_fp": "200.00",
            },
            {
                "ticker": "KXPERLIGA1TOTAL-26AUG31CAGMEL-2",
                "event_ticker": "KXPERLIGA1TOTAL-26AUG31CAGMEL",
                "title": "Cajamarca vs Melgar O1.5",
                "close_time": "2026-08-31T18:00:00Z",
                "volume_fp": "50.00",
                "volume_24h_fp": "200.00",
            },
        ]

        result = discover_soccer_games()

        assert len(result.games) == 1
        game = result.games[0]
        assert "KXPERLIGA1" in game.home_ml_ticker
        assert game.over_05_ticker == "KXPERLIGA1TOTAL-26AUG31CAGMEL-1"
        assert game.over_15_ticker == "KXPERLIGA1TOTAL-26AUG31CAGMEL-2"
