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
from datetime import datetime, timedelta, timezone
from typing import Any

import requests

logger = logging.getLogger(__name__)

KALSHI_API_BASE = "https://api.elections.kalshi.com/trade-api/v2"

# GAME + TOTAL pairs. Midweek cups/second divisions are required so tonight's
# tape (Coppa Italia, EFL Championship, Sudamericana-adjacent slates) is not
# skipped in favor of Saturday EPL volume.
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
    "KXARGPREMDIVGAME",
    "KXARGPREMDIVTOTAL",
    "KXWCGAME",
    "KXWCTOTAL",
    "KXBRASILEIROGAME",
    "KXBRASILEIROTOTAL",
    "KXBRASILEIROBGAME",
    "KXBRASILEIROBTOTAL",
    "KXLIGAMXGAME",
    "KXLIGAMXTOTAL",
    "KXCOPPAITALIAGAME",
    "KXCOPPAITALIATOTAL",
    "KXEFLCHAMPIONSHIPGAME",
    "KXEFLCHAMPIONSHIPTOTAL",
    "KXECULPGAME",
    "KXECULPTOTAL",
    "KXCHLLDPGAME",
    "KXCHLLDPTOTAL",
    "KXDIMAYORGAME",
    "KXDIMAYORTOTAL",
    "KXUSLGAME",
    "KXUSLTOTAL",
    "KXVENFUTVEGAME",
    "KXVENFUTVETOTAL",
    "KXCONMEBOLLIBGAME",
    "KXCONMEBOLLIBTOTAL",
    "KXCONMEBOLSUDGAME",
    "KXCONMEBOLSUDTOTAL",
    "KXEREDIVISIEGAME",
    "KXEREDIVISIETOTAL",
    "KXNWSLGAME",
    "KXNWSLTOTAL",
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
    "KXARGPREMDIVGAME",
    "KXWCGAME",
    "KXBRASILEIROGAME",
    "KXBRASILEIROBGAME",
    "KXLIGAMXGAME",
    "KXCOPPAITALIAGAME",
    "KXEFLCHAMPIONSHIPGAME",
    "KXECULPGAME",
    "KXCHLLDPGAME",
    "KXDIMAYORGAME",
    "KXUSLGAME",
    "KXVENFUTVEGAME",
    "KXCONMEBOLLIBGAME",
    "KXCONMEBOLSUDGAME",
    "KXEREDIVISIEGAME",
    "KXNWSLGAME",
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
    "KXARGPREMDIVTOTAL",
    "KXWCTOTAL",
    "KXBRASILEIROTOTAL",
    "KXBRASILEIROBTOTAL",
    "KXLIGAMXTOTAL",
    "KXCOPPAITALIATOTAL",
    "KXEFLCHAMPIONSHIPTOTAL",
    "KXECULPTOTAL",
    "KXCHLLDPTOTAL",
    "KXDIMAYORTOTAL",
    "KXUSLTOTAL",
    "KXVENFUTVETOTAL",
    "KXCONMEBOLLIBTOTAL",
    "KXCONMEBOLSUDTOTAL",
    "KXEREDIVISIETOTAL",
    "KXNWSLTOTAL",
)

MIN_VOLUME_THRESHOLD = 50
MIN_24H_VOLUME_THRESHOLD = 100

# Kickoff window for "today / tonight" tape. close_time is market expiry (often
# +2–3 days) so we rank on occurrence_datetime instead.
LIVE_LOOKBACK_HOURS = 3
SOON_HORIZON_HOURS = 18

SKIP_ML_CODES = {"TIE", "DRAW", "X"}

PLACEHOLDER_TICKER_TOKENS = {
    "auto",
    "discover",
    "run",
    "none",
    "example",
    "ticker_o35",
    "ticker_o45",
    "your_o35_ticker",
    "your_o45_ticker",
}


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
    occurrence_time: str = ""
    series: str = ""

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

    @property
    def kickoff(self) -> datetime | None:
        return _parse_iso(self.occurrence_time) or _parse_iso(self.close_time)


@dataclass
class DiscoveryResult:
    """Result of soccer game discovery."""

    games: list[SoccerGame]
    tickers: list[str]
    log_lines: list[str]
    discovered_at: str = ""
    soon_games: list[SoccerGame] = field(default_factory=list)
    later_games: list[SoccerGame] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.discovered_at:
            self.discovered_at = datetime.now(tz=timezone.utc).isoformat()


def _parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    text = value.strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def is_placeholder_ticker(ticker: str) -> bool:
    """True for .env.example tokens / 'auto' — not a real Kalshi ticker."""
    token = (ticker or "").strip().lower()
    if not token:
        return True
    if token in PLACEHOLDER_TICKER_TOKENS:
        return True
    if token.startswith("ticker_") or token.startswith("your_"):
        return True
    return False


def needs_auto_discover(tickers: list[str] | None) -> bool:
    """Empty or placeholder LAB_TICKERS should auto-discover, not pin fake books."""
    cleaned = [t.strip() for t in (tickers or []) if t and t.strip()]
    if not cleaned:
        return True
    return all(is_placeholder_ticker(t) for t in cleaned)


def is_live_or_soon(
    game: SoccerGame,
    *,
    now: datetime | None = None,
    lookback_hours: float = LIVE_LOOKBACK_HOURS,
    horizon_hours: float = SOON_HORIZON_HOURS,
) -> bool:
    """True if kickoff is in-play or later today/tonight."""
    kickoff = game.kickoff
    if kickoff is None:
        return False
    now_utc = now or datetime.now(tz=timezone.utc)
    start = now_utc - timedelta(hours=lookback_hours)
    end = now_utc + timedelta(hours=horizon_hours)
    return start <= kickoff <= end


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
        r"the\s+([A-Z][A-Za-z0-9'.\s]+?)\s+vs\.?\s+([A-Z][A-Za-z0-9'.\s]+?)\s+professional",
        rules_primary,
    )
    if match:
        return f"{match.group(1).strip()} vs {match.group(2).strip()}"

    match = re.search(
        r"([A-Z][A-Za-z0-9'.\s]+?)\s+vs\.?\s+([A-Z][A-Za-z0-9'.\s]+?)(?:\s+professional|\s+soccer|\s+EPL|\s+La Liga)",
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

    for i, series in enumerate(SOCCER_SERIES_PREFIXES):
        if i and i % 8 == 0:
            time.sleep(0.35)
        url = f"{rest_base}/markets"
        params = {
            "series_ticker": series,
            "status": "open",
            "limit": 200,
        }
        try:
            resp = session.get(url, params=params, timeout=timeout)
            if resp.status_code == 429:
                logger.warning(f"Rate-limited on {series}; retrying once")
                time.sleep(1.5)
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

    occurrence = ""
    series = ""
    for market in markets:
        if not occurrence:
            occurrence = market.get("occurrence_datetime") or market.get("expected_expiration_time") or ""
        ticker = market.get("ticker", "")
        if ticker and not series:
            series = ticker.split("-", 1)[0]

    game = SoccerGame(
        event_ticker=event_ticker,
        title=title,
        home_team=home_team,
        away_team=away_team,
        close_time=close_time,
        occurrence_time=occurrence,
        series=series,
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
            if team_code in SKIP_ML_CODES:
                continue
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
    now: datetime | None = None,
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

    now = now or datetime.now(tz=timezone.utc)
    soon = [g for g in games if is_live_or_soon(g, now=now)]
    later = [g for g in games if g not in soon]
    later.sort(key=lambda g: g.total_24h_volume, reverse=True)

    has_kickoffs = any(g.occurrence_time for g in games)
    if soon:
        soon_with_vol = [
            g for g in soon
            if g.total_volume >= min_volume or g.total_24h_volume >= min_24h_volume
        ]
        soon_with_vol.sort(key=lambda g: g.total_24h_volume, reverse=True)
        selected = list(soon_with_vol[:max_games])
        if len(selected) < max_games:
            rest = [g for g in soon if g not in selected]
            rest.sort(key=lambda g: (g.kickoff or now, -g.total_24h_volume))
            selected.extend(rest[: max_games - len(selected)])
        log_lines.append(
            f"Live/soon games (kickoff -{LIVE_LOOKBACK_HOURS:.0f}h..+{SOON_HORIZON_HOURS:.0f}h): {len(soon)}"
        )
        log_lines.append(f"Auto-selected {len(selected)} for the paper logger")
    elif has_kickoffs:
        selected = []
        log_lines.append("No soccer live or later today/tonight (kickoffs known). Auto-discover is ready for the next slate.")
    else:
        # Unit fixtures often omit occurrence_datetime — keep volume ranking.
        selected = [
            g for g in games
            if g.total_volume >= min_volume or g.total_24h_volume >= min_24h_volume
        ]
        selected.sort(key=lambda g: g.total_24h_volume, reverse=True)
        selected = selected[:max_games]
        log_lines.append(
            f"Games with volume (>={min_volume} total or >={min_24h_volume} 24h): {len(selected)}"
        )

    all_tickers: list[str] = []
    for game in selected:
        tickers = game.get_tickers()
        all_tickers.extend(tickers)
        ticker_summary = ", ".join(t.split("-")[-1] for t in tickers)
        kick = game.occurrence_time or game.close_time or "?"
        log_lines.append(
            f"  {game.title[:50]}: kick={kick} vol={game.total_volume:.0f}, "
            f"24h={game.total_24h_volume:.0f}, tickers=[{ticker_summary}]"
        )

    if not all_tickers:
        log_lines.append("No tickers auto-funded (no today/tonight soccer, or no volume on fixtures)")

    return DiscoveryResult(
        games=selected,
        tickers=all_tickers,
        log_lines=log_lines,
        soon_games=soon,
        later_games=later[:12],
    )


def format_discovery_log(result: DiscoveryResult) -> str:
    """Format discovery result as a multi-line log string."""
    return "\n".join(result.log_lines)


def format_slate_digest(result: DiscoveryResult) -> str:
    """Short markdown digest of live/soon books vs what the paper logger funds."""
    lines = [
        "# Soccer slate digest (paper logger)",
        "",
        f"Discovered at `{result.discovered_at}` (UTC).",
        "",
        "Paper only — no live orders. Fills are **not** invented; would-have "
        "scalps appear only after a book-detected GOAL and a fill check on tape.",
        "",
        "## Auto-funded (logger will watch)",
        "",
    ]
    if not result.games:
        lines.append("None. No today/tonight soccer tape selected.")
        lines.append("")
    else:
        lines.append("| Kickoff (UTC) | Match | 24h vol | Tickers |")
        lines.append("|---|---|---:|---|")
        for game in result.games:
            tickers = ", ".join(t.rsplit("-", 1)[-1] for t in game.get_tickers())
            lines.append(
                f"| {game.occurrence_time or game.close_time or '?'} | "
                f"{game.title[:48]} | {game.total_24h_volume:.0f} | `{tickers}` |"
            )
        lines.append("")

    if result.soon_games and len(result.soon_games) > len(result.games):
        extra = [g for g in result.soon_games if g not in result.games]
        lines.append("## Also live/soon (not in top-N)")
        lines.append("")
        for game in extra[:8]:
            lines.append(
                f"- {game.occurrence_time or '?'} {game.title[:48]} "
                f"(24h {game.total_24h_volume:.0f})"
            )
        lines.append("")

    if result.later_games:
        lines.append("## Later (not today/tonight — not auto-funded)")
        lines.append("")
        for game in result.later_games[:8]:
            lines.append(
                f"- {game.occurrence_time or game.close_time or '?'} "
                f"{game.title[:48]} (24h {game.total_24h_volume:.0f})"
            )
        lines.append("")

    if not result.tickers:
        lines.append(
            "Auto-discover is ready for the next slate. "
            "Launch without `LAB_TICKERS` and it will fund when games appear."
        )
    else:
        lines.append(
            f"Paper logger would capture **{len(result.tickers)}** books "
            f"(`books_long.csv` at 200ms) with spoof filter + fill-would-have. "
            f"No fills until a GOAL prints on the tape."
        )
    return "\n".join(lines)


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
