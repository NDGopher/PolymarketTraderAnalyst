"""Tests for soccer auto-discovery from Kalshi API."""

import pytest
from unittest.mock import patch, MagicMock

from suspension_lab.soccer_discovery import (
    SoccerGame,
    DiscoveryResult,
    TotalBook,
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
                "yes_bid_dollars": "0.91",
                "yes_ask_dollars": "0.93",
            },
            {
                "ticker": "KXEPLTOTAL-26AUG31ARSCHE-2",
                "event_ticker": "KXEPLTOTAL-26AUG31ARSCHE",
                "title": "Arsenal vs Chelsea O1.5",
                "close_time": "2026-08-31T18:00:00Z",
                "volume_fp": "50.00",
                "volume_24h_fp": "200.00",
                "yes_bid_dollars": "0.70",
                "yes_ask_dollars": "0.72",
            },
            {
                "ticker": "KXEPLTOTAL-26AUG31ARSCHE-3",
                "event_ticker": "KXEPLTOTAL-26AUG31ARSCHE",
                "volume_fp": "80.00",
                "volume_24h_fp": "250.00",
                "yes_bid_dollars": "0.48",
                "yes_ask_dollars": "0.50",
            },
        ]

        result = discover_soccer_games(min_volume=50, min_24h_volume=100)

        assert len(result.games) == 1
        assert "KXEPLGAME-26AUG31ARSCHE-ARS" in result.tickers
        assert "KXEPLGAME-26AUG31ARSCHE-CHE" in result.tickers
        assert "KXEPLTOTAL-26AUG31ARSCHE-1" not in result.tickers
        assert "KXEPLTOTAL-26AUG31ARSCHE-3" in result.tickers

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
                "yes_bid_dollars": "0.91",
                "yes_ask_dollars": "0.93",
            },
            {
                "ticker": "KXPERLIGA1TOTAL-26AUG31CAGMEL-2",
                "event_ticker": "KXPERLIGA1TOTAL-26AUG31CAGMEL",
                "title": "Cajamarca vs Melgar O1.5",
                "close_time": "2026-08-31T18:00:00Z",
                "volume_fp": "50.00",
                "volume_24h_fp": "200.00",
                "yes_bid_dollars": "0.48",
                "yes_ask_dollars": "0.50",
            },
            {
                "ticker": "KXPERLIGA1TOTAL-26AUG31CAGMEL-3",
                "event_ticker": "KXPERLIGA1TOTAL-26AUG31CAGMEL",
                "volume_fp": "40.00",
                "volume_24h_fp": "180.00",
                "yes_bid_dollars": "0.28",
                "yes_ask_dollars": "0.30",
            },
        ]

        result = discover_soccer_games()

        assert len(result.games) == 1
        game = result.games[0]
        assert "KXPERLIGA1" in game.home_ml_ticker
        assert game.total_atm_ticker == "KXPERLIGA1TOTAL-26AUG31CAGMEL-2"
        assert game.total_up_ticker == "KXPERLIGA1TOTAL-26AUG31CAGMEL-3"

    @patch("suspension_lab.soccer_discovery.fetch_open_soccer_markets")
    def test_brasileirao_tickers(self, mock_fetch):
        """Test that Brasileirão (Brazil Série A) tickers are discovered correctly."""
        mock_fetch.return_value = [
            {
                "ticker": "KXBRASILEIROGAME-26SEP02FLAMIR-FLA",
                "event_ticker": "KXBRASILEIROGAME-26SEP02FLAMIR",
                "title": "Flamengo vs Mirassol",
                "close_time": "2026-09-02T23:00:00Z",
                "volume_fp": "200.00",
                "volume_24h_fp": "800.00",
            },
            {
                "ticker": "KXBRASILEIROGAME-26SEP02FLAMIR-MIR",
                "event_ticker": "KXBRASILEIROGAME-26SEP02FLAMIR",
                "title": "Flamengo vs Mirassol",
                "close_time": "2026-09-02T23:00:00Z",
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

        result = discover_soccer_games()

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
                "volume_fp": "500.00",
                "volume_24h_fp": "1200.00",
            },
            {
                "ticker": "KXLIGAMXGAME-26SEP06CRASLA-SLA",
                "event_ticker": "KXLIGAMXGAME-26SEP06CRASLA",
                "title": "Cruz Azul vs Santos Laguna",
                "close_time": "2026-09-06T02:00:00Z",
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

        result = discover_soccer_games()

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
