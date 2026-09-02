"""Auto-discover live/imminent soccer events from Kalshi API and map to 4 tickers per game.

This module queries Kalshi's public API to find active soccer markets,
identifies games with volume, and maps each game to the 4 key tickers:
- Home ML (moneyline)
- Away ML (moneyline)
- O0.5 goals (totals)
- O1.5 goals (totals)

No scraping - uses official REST API endpoints.
"""

from __future__ import annotations

import logging
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

import requests

logger = logging.getLogger(__name__)

KALSHI_API_BASE = "https://api.elections.kalshi.com/trade-api/v2"

SOCCER_SERIES_PREFIXES = (
    "KXEPLGAME",
    "KXEPLTOTAL",
    "KXLALIGAGAME",
    "KXLALIGATOTAL",
    "KXBUNDESLIGAGAME",
    "KXBUNDESLIGATOTAL",
    "KXSERIEAGAME",
    "KXSERIEATOTAL",
    "KXLIGUE1GAME",
    "KXLIGUE1TOTAL",
    "KXUCLGAME",
    "KXUCLTOTAL",
    "KXUEFAGAME",
    "KXUELGAME",
    "KXUELTOTAL",
    "KXUECLGAME",
    "KXUECLTOTAL",
    "KXMLSGAME",
    "KXMLSTOTAL",
    "KXPERLIGA1GAME",
    "KXPERLIGA1TOTAL",
    "KXARGLIGA1GAME",
    "KXARGLIGA1TOTAL",
    "KXWCGAME",
    "KXWCTOTAL",
)

SERIES_WITH_GAMES = (
    "KXEPLGAME",
    "KXLALIGAGAME",
    "KXBUNDESLIGAGAME",
    "KXSERIEAGAME",
    "KXLIGUE1GAME",
    "KXUCLGAME",
    "KXUEFAGAME",
    "KXUELGAME",
    "KXUECLGAME",
    "KXMLSGAME",
    "KXPERLIGA1GAME",
    "KXARGLIGA1GAME",
    "KXWCGAME",
)

SERIES_WITH_TOTALS = (
    "KXEPLTOTAL",
    "KXLALIGATOTAL",
    "KXBUNDESLIGATOTAL",
    "KXSERIEATOTAL",
    "KXLIGUE1TOTAL",
    "KXUCLTOTAL",
    "KXUELTOTAL",
    "KXUECLTOTAL",
    "KXMLSTOTAL",
    "KXPERLIGA1TOTAL",
    "KXARGLIGA1TOTAL",
    "KXWCTOTAL",
)

MIN_VOLUME_THRESHOLD = 50
MIN_24H_VOLUME_THRESHOLD = 100


@dataclass
class SoccerGame:
    """Represents a discovered soccer game with its associated markets."""

    event_ticker: str
    title: str
    home_team: str
    away_team: str
    close_time: str
    home_ml_ticker: str | None = None
    away_ml_ticker: str | None = None
    over_05_ticker: str | None = None
    over_15_ticker: str | None = None
    total_volume: float = 0.0
    total_24h_volume: float = 0.0
    market_count: int = 0
    reasons: list[str] = field(default_factory=list)

    def get_tickers(self) -> list[str]:
        """Return the list of non-None tickers for this game."""
        tickers = []
        if self.home_ml_ticker:
            tickers.append(self.home_ml_ticker)
        if self.away_ml_ticker:
            tickers.append(self.away_ml_ticker)
        if self.over_05_ticker:
            tickers.append(self.over_05_ticker)
        if self.over_15_ticker:
            tickers.append(self.over_15_ticker)
        return tickers

    @property
    def has_volume(self) -> bool:
        return (
            self.total_volume >= MIN_VOLUME_THRESHOLD
            or self.total_24h_volume >= MIN_24H_VOLUME_THRESHOLD
        )


@dataclass
class DiscoveryResult:
    """Result of soccer game discovery."""

    games: list[SoccerGame]
    tickers: list[str]
    log_lines: list[str]
    discovered_at: str = ""

    def __post_init__(self) -> None:
        if not self.discovered_at:
            self.discovered_at = datetime.now(tz=timezone.utc).isoformat()


def _parse_volume(market: dict) -> tuple[float, float]:
    """Parse volume and 24h volume from market data."""
    vol_str = market.get("volume_fp", "0") or "0"
    vol_24h_str = market.get("volume_24h_fp", "0") or "0"
    try:
        vol = float(vol_str)
    except (ValueError, TypeError):
        vol = 0.0
    try:
        vol_24h = float(vol_24h_str)
    except (ValueError, TypeError):
        vol_24h = 0.0
    return vol, vol_24h


def _extract_teams_from_title(title: str) -> tuple[str, str]:
    """Extract home and away team names from event/market title.

    Common formats:
    - "Arsenal vs Chelsea - Aug 31, 2026"
    - "Arsenal - Chelsea"
    - "Barcelona vs Real Madrid"
    - "Liverpool vs. Man City"
    """
    title_clean = re.sub(r"\s*-\s*[A-Z][a-z]{2}\s+\d{1,2},?\s*\d{4}.*$", "", title)
    title_clean = re.sub(r"\s*-\s*\d{1,2}/\d{1,2}/\d{2,4}.*$", "", title_clean)

    vs_match = re.split(r"\s+vs\.?\s+", title_clean, flags=re.IGNORECASE)
    if len(vs_match) >= 2:
        return vs_match[0].strip(), vs_match[1].strip()

    if " - " in title_clean:
        parts = title_clean.split(" - ", 1)
        if len(parts) >= 2:
            return parts[0].strip(), parts[1].strip()

    return title_clean, ""


def _extract_game_from_rules(rules_primary: str) -> str | None:
    """Extract game title from rules_primary field.

    Example: "If Tie is the result of the Leeds United vs Newcastle professional EPL soccer game..."
    Returns: "Leeds United vs Newcastle"
    """
    match = re.search(
        r"the\s+([A-Z][A-Za-z\s]+?)\s+vs\.?\s+([A-Z][A-Za-z\s]+?)\s+professional",
        rules_primary,
    )
    if match:
        return f"{match.group(1).strip()} vs {match.group(2).strip()}"

    match = re.search(
        r"([A-Z][A-Za-z\s]+?)\s+vs\.?\s+([A-Z][A-Za-z\s]+?)(?:\s+professional|\s+soccer|\s+EPL|\s+La Liga)",
        rules_primary,
    )
    if match:
        return f"{match.group(1).strip()} vs {match.group(2).strip()}"

    return None


def _match_game_ticker(ticker: str) -> re.Match | None:
    """Match a GAME ticker and extract team code.

    Examples:
    - KXEPLGAME-26AUG31ARSCHE-ARS -> home team ARS
    - KXEPLGAME-26AUG31ARSCHE-CHE -> away team CHE
    """
    return re.match(r"^(KX[A-Z0-9]+GAME)-([A-Z0-9]+)-([A-Z]+)$", ticker)


def _match_total_ticker(ticker: str) -> re.Match | None:
    """Match a TOTAL ticker and extract strike number.

    Examples:
    - KXEPLTOTAL-26AUG31ARSCHE-1 -> O0.5 (strike 1)
    - KXEPLTOTAL-26AUG31ARSCHE-2 -> O1.5 (strike 2)
    """
    return re.match(r"^(KX[A-Z0-9]+TOTAL)-([A-Z0-9]+)-(\d+)$", ticker)


def _get_event_identifier(ticker: str) -> str | None:
    """Extract the event identifier from a market ticker.

    Both GAME and TOTAL tickers for the same match share an identifier.
    Examples:
    - KXEPLGAME-26AUG31ARSCHE-ARS -> 26AUG31ARSCHE
    - KXEPLTOTAL-26AUG31ARSCHE-1 -> 26AUG31ARSCHE
    """
    game_match = _match_game_ticker(ticker)
    if game_match:
        return game_match.group(2)

    total_match = _match_total_ticker(ticker)
    if total_match:
        return total_match.group(2)

    parts = ticker.split("-")
    if len(parts) >= 2:
        return parts[1]
    return None


def fetch_open_soccer_markets(
    rest_base: str = KALSHI_API_BASE,
    timeout: float = 15.0,
) -> list[dict]:
    """Fetch all open soccer markets from Kalshi API.

    Returns list of market dicts for all soccer-related series with status=open.
    """
    session = requests.Session()
    session.headers.update({"User-Agent": "suspension-lab/0.1"})

    all_markets: list[dict] = []

    for series in SOCCER_SERIES_PREFIXES:
        url = f"{rest_base}/markets"
        params = {
            "series_ticker": series,
            "status": "open",
            "limit": 200,
        }
        try:
            resp = session.get(url, params=params, timeout=timeout)
            if resp.status_code == 200:
                data = resp.json()
                markets = data.get("markets", [])
                all_markets.extend(markets)
                logger.debug(f"Fetched {len(markets)} markets from {series}")
        except requests.RequestException as e:
            logger.warning(f"Failed to fetch {series}: {e}")
            continue

    return all_markets


def group_markets_by_event(markets: list[dict]) -> dict[str, list[dict]]:
    """Group markets by their event identifier (game match)."""
    groups: dict[str, list[dict]] = {}
    for market in markets:
        ticker = market.get("ticker", "")
        event_id = _get_event_identifier(ticker)
        if event_id:
            groups.setdefault(event_id, []).append(market)
    return groups


def build_soccer_game(event_id: str, markets: list[dict]) -> SoccerGame | None:
    """Build a SoccerGame from a group of related markets.

    Maps markets to:
    - home_ml_ticker, away_ml_ticker (from GAME series)
    - over_05_ticker (TOTAL strike 1)
    - over_15_ticker (TOTAL strike 2)
    """
    if not markets:
        return None

    first = markets[0]
    event_ticker = first.get("event_ticker", "")
    close_time = first.get("close_time", "")

    title = None
    for market in markets:
        rules = market.get("rules_primary", "")
        if rules:
            extracted = _extract_game_from_rules(rules)
            if extracted:
                title = extracted
                break

    if not title:
        title = first.get("title", "") or first.get("yes_sub_title", "") or event_id

    home_team, away_team = _extract_teams_from_title(title)

    game = SoccerGame(
        event_ticker=event_ticker,
        title=title,
        home_team=home_team,
        away_team=away_team,
        close_time=close_time,
    )

    game_tickers: list[tuple[str, str]] = []
    total_tickers: dict[int, str] = {}

    for market in markets:
        ticker = market.get("ticker", "")
        vol, vol_24h = _parse_volume(market)
        game.total_volume += vol
        game.total_24h_volume += vol_24h
        game.market_count += 1

        gm = _match_game_ticker(ticker)
        if gm:
            team_code = gm.group(3)
            game_tickers.append((ticker, team_code))
            continue

        tm = _match_total_ticker(ticker)
        if tm:
            strike = int(tm.group(3))
            total_tickers[strike] = ticker
            continue

    if len(game_tickers) >= 2:
        game_tickers.sort(key=lambda x: x[1])
        game.home_ml_ticker = game_tickers[0][0]
        game.away_ml_ticker = game_tickers[1][0]
        game.reasons.append(f"ML: {game_tickers[0][1]} vs {game_tickers[1][1]}")
    elif len(game_tickers) == 1:
        game.home_ml_ticker = game_tickers[0][0]
        game.reasons.append(f"ML: only {game_tickers[0][1]} found")

    if 1 in total_tickers:
        game.over_05_ticker = total_tickers[1]
        game.reasons.append("O0.5 found")
    if 2 in total_tickers:
        game.over_15_ticker = total_tickers[2]
        game.reasons.append("O1.5 found")

    return game


def discover_soccer_games(
    rest_base: str = KALSHI_API_BASE,
    min_volume: float = MIN_VOLUME_THRESHOLD,
    min_24h_volume: float = MIN_24H_VOLUME_THRESHOLD,
    max_games: int = 5,
) -> DiscoveryResult:
    """Discover live/imminent soccer games with volume and return discovery result.

    Args:
        rest_base: Kalshi API base URL
        min_volume: Minimum total volume to include a game
        min_24h_volume: Minimum 24h volume to include a game
        max_games: Maximum number of games to return

    Returns:
        DiscoveryResult with games, tickers, and log lines
    """
    log_lines: list[str] = []
    log_lines.append(f"[{datetime.now(tz=timezone.utc).isoformat()}] Starting soccer discovery...")

    markets = fetch_open_soccer_markets(rest_base)
    log_lines.append(f"Fetched {len(markets)} open soccer markets")

    if not markets:
        log_lines.append("No open soccer markets found")
        return DiscoveryResult(games=[], tickers=[], log_lines=log_lines)

    groups = group_markets_by_event(markets)
    log_lines.append(f"Found {len(groups)} unique events")

    games: list[SoccerGame] = []
    for event_id, event_markets in groups.items():
        game = build_soccer_game(event_id, event_markets)
        if game and game.get_tickers():
            games.append(game)

    games_with_volume = [
        g for g in games
        if g.total_volume >= min_volume or g.total_24h_volume >= min_24h_volume
    ]

    games_with_volume.sort(key=lambda g: g.total_24h_volume, reverse=True)
    games_with_volume = games_with_volume[:max_games]

    log_lines.append(f"Games with volume (>={min_volume} total or >={min_24h_volume} 24h): {len(games_with_volume)}")

    all_tickers: list[str] = []
    for game in games_with_volume:
        tickers = game.get_tickers()
        all_tickers.extend(tickers)
        ticker_summary = ", ".join(t.split("-")[-1] for t in tickers)
        log_lines.append(
            f"  {game.title[:50]}: vol={game.total_volume:.0f}, 24h={game.total_24h_volume:.0f}, "
            f"tickers=[{ticker_summary}]"
        )

    if not all_tickers:
        log_lines.append("No tickers discovered (no games with sufficient volume)")

    return DiscoveryResult(
        games=games_with_volume,
        tickers=all_tickers,
        log_lines=log_lines,
    )


def format_discovery_log(result: DiscoveryResult) -> str:
    """Format discovery result as a multi-line log string."""
    return "\n".join(result.log_lines)


def discover_tickers_for_lab(
    rest_base: str = KALSHI_API_BASE,
    min_volume: float = MIN_VOLUME_THRESHOLD,
    min_24h_volume: float = MIN_24H_VOLUME_THRESHOLD,
    max_games: int = 5,
) -> tuple[list[str], str, list[SoccerGame]]:
    """Convenience function for CLI integration.

    Returns:
        Tuple of (ticker_list, log_message, games)
    """
    result = discover_soccer_games(
        rest_base=rest_base,
        min_volume=min_volume,
        min_24h_volume=min_24h_volume,
        max_games=max_games,
    )
    log_msg = format_discovery_log(result)
    return result.tickers, log_msg, result.games


if __name__ == "__main__":
    import sys

    logging.basicConfig(level=logging.DEBUG)
    tickers, log_msg, games = discover_tickers_for_lab()
    print(log_msg)
    print()
    print(f"Discovered {len(tickers)} tickers:")
    for t in tickers:
        print(f"  {t}")
