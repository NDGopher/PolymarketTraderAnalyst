"""Auto-discover live/imminent soccer events from Kalshi API and map to 4 tickers per game.

This module queries Kalshi's public API to find active soccer markets,
identifies games with volume, and maps each game to:
- Home ML (moneyline)
- Away ML (moneyline)
- The total whose YES is nearest 50¢ (not a default O0.5/O1.5)
- The next strike up, if that book is liquid

O0.5 is usually a ~90¢ bond pregame and is not auto-funded as a scalp.

No scraping - uses official REST API endpoints.
"""

from __future__ import annotations

import logging
import os
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
    "KXSLGREECEGAME",
    "KXSLGREECETOTAL",
    "KXGRECUPGAME",
    "KXGRECUPTOTAL",
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
    "KXSLGREECEGAME",
    "KXGRECUPGAME",
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
    "KXSLGREECETOTAL",
    "KXGRECUPTOTAL",
)

MIN_VOLUME_THRESHOLD = 50
MIN_24H_VOLUME_THRESHOLD = 100
TOTAL_ATM_TARGET = 0.50
TOTAL_BOND_YES = 0.88  # skip ~90¢ O0.5 bonds when picking the scalp total
# Next-up farther than this from 50¢ during a no-goal grind → swap to the
# cheaper adjacent strike (e.g. O4.5 at 12¢ → O2.5 while ATM is O3.5).
TOTAL_WING_DRIFT = 0.22
# Ignore 80¢-wide longshot books whose mid luckily prints ~50¢ (e.g. O6.5 8¢/95¢).
TOTAL_MAX_SPREAD = 0.25
DEFAULT_PRIORITY_TEAMS = "sassuolo,frosinone,aek"

# Kickoff window for "today / tonight" tape. close_time is market expiry (often
# +2–3 days) so we rank on occurrence_datetime instead.
LIVE_LOOKBACK_HOURS = 4
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
    total_atm_ticker: str | None = None
    total_atm_label: str = ""
    total_atm_price: float | None = None
    total_up_ticker: str | None = None
    total_up_label: str = ""
    total_up_price: float | None = None
    # Compat aliases — ATM / next-up slots (not necessarily O0.5 / O1.5).
    over_05_ticker: str | None = None
    over_15_ticker: str | None = None
    total_volume: float = 0.0
    total_24h_volume: float = 0.0
    market_count: int = 0
    reasons: list[str] = field(default_factory=list)
    occurrence_time: str = ""
    series: str = ""
    in_play_hint: bool = False
    totals_repick: str = ""
    total_books: list[TotalBook] = field(default_factory=list)

    def get_tickers(self) -> list[str]:
        """Return the list of non-None tickers for this game."""
        tickers = []
        if self.home_ml_ticker:
            tickers.append(self.home_ml_ticker)
        if self.away_ml_ticker:
            tickers.append(self.away_ml_ticker)
        atm = self.total_atm_ticker or self.over_05_ticker
        up = self.total_up_ticker or self.over_15_ticker
        if atm:
            tickers.append(atm)
        if up:
            tickers.append(up)
        return tickers

    def totals_summary(self) -> str:
        parts = []
        if self.total_atm_ticker:
            px = f" {self.total_atm_price:.2f}" if self.total_atm_price is not None else ""
            parts.append(f"{self.total_atm_label or 'ATM'}{px}")
        if self.total_up_ticker:
            px = f" {self.total_up_price:.2f}" if self.total_up_price is not None else ""
            parts.append(f"{self.total_up_label or 'ATM+1'}{px}")
        return ", ".join(parts) if parts else "no liquid 50/50 total"

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


@dataclass(frozen=True)
class TotalBook:
    """One totals strike for a match."""

    strike: int
    ticker: str
    yes_price: float | None
    volume: float
    volume_24h: float
    liquid: bool
    spread: float | None = None

    @property
    def label(self) -> str:
        return strike_to_over_label(self.strike)

    @property
    def tight_enough(self) -> bool:
        if self.spread is None:
            return True
        return self.spread <= TOTAL_MAX_SPREAD


def strike_to_over_label(strike: int) -> str:
    """Kalshi TOTAL-N is Over (N-1).5 — strike 1=O0.5, 3=O2.5."""
    return f"O{strike - 1}.5"


def _parse_dollar_price(raw: Any) -> float | None:
    if raw is None or raw == "":
        return None
    try:
        val = float(raw)
    except (TypeError, ValueError):
        return None
    if val > 1.5:
        val = val / 100.0
    if val < 0 or val > 1:
        return None
    return val


def yes_price_from_market(market: dict) -> float | None:
    """YES mid if two-sided, else last, else bid. Dollars (0–1)."""
    bid = _parse_dollar_price(market.get("yes_bid_dollars") or market.get("yes_bid"))
    ask = _parse_dollar_price(market.get("yes_ask_dollars") or market.get("yes_ask"))
    last = _parse_dollar_price(market.get("last_price_dollars") or market.get("last_price"))
    if bid is not None and ask is not None:
        return (bid + ask) / 2.0
    if last is not None:
        return last
    return bid if bid is not None else ask


def is_bond_yes(price: float | None, *, bond: float = TOTAL_BOND_YES) -> bool:
    if price is None:
        return False
    return price >= bond or price <= (1.0 - bond)


def market_is_liquid(market: dict, volume: float, volume_24h: float) -> bool:
    if volume >= MIN_VOLUME_THRESHOLD or volume_24h >= MIN_24H_VOLUME_THRESHOLD:
        return True
    bid = _parse_dollar_price(market.get("yes_bid_dollars") or market.get("yes_bid"))
    ask = _parse_dollar_price(market.get("yes_ask_dollars") or market.get("yes_ask"))
    return bid is not None and ask is not None


def select_scalp_totals(books: list[TotalBook]) -> tuple[TotalBook | None, TotalBook | None]:
    """ATM = YES nearest 50¢ among non-bond books. Up = next strike if liquid.

    Does not default to O0.5/O1.5. Bonded O0.5 (~90¢) is not a scalp.
    Live YES only — never reuse a pregame snapshot.
    """
    priced = [
        b
        for b in books
        if b.yes_price is not None and not is_bond_yes(b.yes_price) and b.tight_enough
    ]
    if not priced:
        return None, None
    atm = min(
        priced,
        key=lambda b: (abs((b.yes_price or 0.0) - TOTAL_ATM_TARGET), -b.volume_24h, -b.volume, b.strike),
    )
    by_strike = {b.strike: b for b in books}
    up = by_strike.get(atm.strike + 1)
    if up is None or not up.liquid:
        return atm, None
    return atm, up


def select_ingame_totals(
    books: list[TotalBook],
    *,
    drop_far_wing: bool = False,
    drift: float = TOTAL_WING_DRIFT,
) -> tuple[TotalBook | None, TotalBook | None]:
    """Re-pick totals from *current* live YES prices given the score.

    At 1-1, O2.5 is usually 70–85¢ (not 50/50). ATM becomes O3.5 and the
    next strike is O4.5. Do not freeze a pregame O2.5 snapshot.

    If the next-up wing has drifted far from 50¢ *and* there has been no
    goal for a while (`drop_far_wing`), swap that wing for the cheaper
    adjacent strike below ATM (O2.5 when ATM is O3.5), unless that book
    is a bond.
    """
    atm, up = select_scalp_totals(books)
    if atm is None:
        return None, None
    if not drop_far_wing:
        return atm, up
    by_strike = {b.strike: b for b in books}
    up_far = (
        up is None
        or up.yes_price is None
        or abs(up.yes_price - TOTAL_ATM_TARGET) > drift
    )
    if not up_far:
        return atm, up
    down = by_strike.get(atm.strike - 1)
    if (
        down is not None
        and down.liquid
        and down.yes_price is not None
        and not is_bond_yes(down.yes_price)
    ):
        return atm, down
    return atm, up


def apply_live_totals(
    game: SoccerGame,
    books: list[TotalBook],
    *,
    drop_far_wing: bool = False,
) -> SoccerGame:
    """Overwrite ATM / next-up from live YES books (in-game re-pick)."""
    atm, wing = select_ingame_totals(books, drop_far_wing=drop_far_wing)
    game.total_atm_ticker = atm.ticker if atm else None
    game.total_atm_label = atm.label if atm else ""
    game.total_atm_price = atm.yes_price if atm else None
    game.total_up_ticker = wing.ticker if wing else None
    game.total_up_label = wing.label if wing else ""
    game.total_up_price = wing.yes_price if wing else None
    game.over_05_ticker = game.total_atm_ticker
    game.over_15_ticker = game.total_up_ticker
    # O0.5 is often a 90¢ *pregame* bond. O1.5 bonded (~99¢) means 2+ goals
    # already — the match is in-play even if Kalshi's kickoff clock is late.
    game.in_play_hint = any(
        b.strike == 2 and b.yes_price is not None and is_bond_yes(b.yes_price) for b in books
    )
    if atm and wing:
        mode = "grind-cheap-side" if drop_far_wing and wing.strike < atm.strike else "live-atm+up"
        game.totals_repick = f"{mode} {atm.label}/{wing.label}"
    elif atm:
        game.totals_repick = f"live-atm {atm.label}"
    else:
        game.totals_repick = "no liquid live total"
    return game


def priority_title_tokens() -> tuple[str, ...]:
    raw = os.environ.get("LAB_PRIORITY_TEAMS", DEFAULT_PRIORITY_TEAMS)
    return tuple(t.strip().lower() for t in raw.split(",") if t.strip())


def is_priority_game(game: SoccerGame, tokens: tuple[str, ...] | None = None) -> bool:
    needles = tokens if tokens is not None else priority_title_tokens()
    blob = " ".join(
        (
            game.title,
            game.home_team,
            game.away_team,
            game.event_ticker,
            game.series,
        )
    ).lower()
    return any(tok in blob for tok in needles)


def is_in_play(game: SoccerGame, *, now: datetime | None = None) -> bool:
    """Kickoff already happened, or O1.5 is bonded (2+ goals) near listed kickoff."""
    now_utc = now or datetime.now(tz=timezone.utc)
    kickoff = game.kickoff
    if kickoff is not None:
        started = kickoff <= now_utc + timedelta(minutes=10)
        recent = now_utc - kickoff <= timedelta(hours=LIVE_LOOKBACK_HOURS)
        if started and recent:
            return True
        if game.in_play_hint and abs((kickoff - now_utc).total_seconds()) <= 8 * 3600:
            return True
        return False
    return bool(game.in_play_hint)


def is_watchable(
    game: SoccerGame,
    *,
    now: datetime | None = None,
    lookback_hours: float = LIVE_LOOKBACK_HOURS,
    horizon_hours: float = SOON_HORIZON_HOURS,
) -> bool:
    """Live, soon, or already in-play by bonded totals (kickoff clock may lag)."""
    if is_live_or_soon(
        game, now=now, lookback_hours=lookback_hours, horizon_hours=horizon_hours
    ):
        return True
    return is_in_play(game, now=now)


def select_watchlist(
    games: list[SoccerGame],
    *,
    now: datetime,
    max_games: int,
    min_volume: float,
    min_24h_volume: float,
) -> tuple[list[SoccerGame], list[SoccerGame], list[SoccerGame], list[str]]:
    """Priority + in-play first so a 1-1 Coppa / AEK tape is not dropped for volume."""
    notes: list[str] = []
    soon = [g for g in games if is_watchable(g, now=now)]
    later = [g for g in games if g not in soon]
    later.sort(key=lambda g: g.total_24h_volume, reverse=True)

    must: list[SoccerGame] = []
    for game in games:
        if not is_priority_game(game):
            continue
        # Today/tonight only — do not pin next week's Sassuolo/AEK because the
        # team token matches. In-play hint covers a late Kalshi kickoff clock.
        if not (is_live_or_soon(game, now=now) or is_in_play(game, now=now)):
            continue
        if game not in must:
            must.append(game)
            notes.append(f"priority auto-fund: {game.title[:48]}")

    in_play = [g for g in soon if is_in_play(g, now=now) and g not in must]
    in_play.sort(key=lambda g: g.total_24h_volume, reverse=True)
    selected = list(must)
    # In-play is forced even outside top-N, but not every bonded-O0.5 pregame
    # on the catalog. Cap extras so the tape stays on today's live matches.
    in_play_cap = max(max_games, 8)
    for game in in_play:
        if len([g for g in selected if is_in_play(g, now=now)]) >= in_play_cap:
            break
        if game not in selected:
            selected.append(game)
            notes.append(f"in-play auto-fund: {game.title[:48]}")

    rest = [g for g in soon if g not in selected]
    rest_vol = [
        g for g in rest if g.total_volume >= min_volume or g.total_24h_volume >= min_24h_volume
    ]
    rest_vol.sort(key=lambda g: g.total_24h_volume, reverse=True)
    rest_other = [g for g in rest if g not in rest_vol]
    rest_other.sort(key=lambda g: (g.kickoff or now, -g.total_24h_volume))

    for pool in (rest_vol, rest_other):
        for game in pool:
            if len(selected) >= max_games:
                break
            selected.append(game)
        if len(selected) >= max_games:
            break

    # Priority / in-play always stay even if that exceeds max_games.
    return selected, soon, later, notes


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
    - home_ml_ticker, away_ml_ticker (from GAME series; TIE skipped)
    - total nearest 50¢ YES + next strike up if liquid
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
    total_books: list[TotalBook] = []

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
            yes = yes_price_from_market(market)
            bid = _parse_dollar_price(market.get("yes_bid_dollars") or market.get("yes_bid"))
            ask = _parse_dollar_price(market.get("yes_ask_dollars") or market.get("yes_ask"))
            spread = (ask - bid) if bid is not None and ask is not None else None
            total_books.append(
                TotalBook(
                    strike=strike,
                    ticker=ticker,
                    yes_price=yes,
                    volume=vol,
                    volume_24h=vol_24h,
                    liquid=market_is_liquid(market, vol, vol_24h),
                    spread=spread,
                )
            )
            continue

    if len(game_tickers) >= 2:
        game_tickers.sort(key=lambda x: x[1])
        game.home_ml_ticker = game_tickers[0][0]
        game.away_ml_ticker = game_tickers[1][0]
        game.reasons.append(f"ML: {game_tickers[0][1]} vs {game_tickers[1][1]}")
    elif len(game_tickers) == 1:
        game.home_ml_ticker = game_tickers[0][0]
        game.reasons.append(f"ML: only {game_tickers[0][1]} found")

    game.total_books = total_books
    apply_live_totals(game, total_books, drop_far_wing=False)
    atm_t = game.total_atm_ticker
    up_t = game.total_up_ticker
    if game.total_atm_label:
        px = game.total_atm_price
        game.reasons.append(
            f"{game.total_atm_label} nearest 50¢ live ({px:.2f})" if px is not None else game.total_atm_label
        )
    if game.total_up_label:
        game.reasons.append(f"{game.total_up_label} next strike up (live YES)")
    if total_books and not atm_t:
        game.reasons.append("no non-bond total near 50¢ — skipped O0.5/O1.5 default")
    if game.in_play_hint:
        game.reasons.append("in-play hint: low totals bonded — re-picked from live YES")

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
    has_kickoffs = any(g.occurrence_time for g in games)
    watchable = [g for g in games if is_watchable(g, now=now)]
    soon: list[SoccerGame] = []
    later: list[SoccerGame] = []
    if watchable:
        selected, soon, later, extra_notes = select_watchlist(
            games,
            now=now,
            max_games=max_games,
            min_volume=min_volume,
            min_24h_volume=min_24h_volume,
        )
        log_lines.append(
            f"Live/soon/in-play games (kickoff -{LIVE_LOOKBACK_HOURS:.0f}h..+{SOON_HORIZON_HOURS:.0f}h): {len(soon)}"
        )
        log_lines.append(f"Auto-selected {len(selected)} for the paper logger")
        log_lines.extend(f"  {n}" for n in extra_notes)
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
        ml = ", ".join(t.split("-")[-1] for t in tickers if "TOTAL" not in t)
        kick = game.occurrence_time or game.close_time or "?"
        repick = f" repick={game.totals_repick}" if game.totals_repick else ""
        log_lines.append(
            f"  {game.title[:50]}: kick={kick} vol={game.total_volume:.0f}, "
            f"24h={game.total_24h_volume:.0f}, ML=[{ml}] totals=[{game.totals_summary()}]{repick}"
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
        "In-game totals re-pick from **live YES** (nearest 50¢ given the current "
        "score). A pregame O2.5 is not frozen after the score moves.",
        "",
        "## Auto-funded (logger will watch)",
        "",
    ]
    if not result.games:
        lines.append("None. No today/tonight soccer tape selected.")
        lines.append("")
    else:
        lines.append("| Kickoff (UTC) | Match | 24h vol | Totals (ATM + next) |")
        lines.append("|---|---|---:|---|")
        for game in result.games:
            lines.append(
                f"| {game.occurrence_time or game.close_time or '?'} | "
                f"{game.title[:48]} | {game.total_24h_volume:.0f} | {game.totals_summary()} |"
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
