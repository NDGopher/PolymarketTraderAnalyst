"""Auto-discover live/imminent soccer events from Kalshi API.

Fingerprint (not a Big-5 prefix allowlist):
- title/subtitle contains "goals scored", or
- series looks like soccer KX*GAME / KX*TOTAL and is not NFL/MLB/NBA/NHL/…

Funds home + away ML (and liquid TIE), plus live ATM total + next strike.
ATM is live YES nearest 50¢ — a 0-1 grind with O1.5 at 50¢ funds O1.5,
not leftover O3.5/O4.5. 1-1 → O3.5+O4.5 is that ATM case, not a pin.
O0.5 ~90¢ bonds and dead wings (YES < ~10¢, bid missing) are skipped.
Rediscover on a timer while the session runs. Paper only — no live bets.

`.env LAB_TICKERS` is never a pin list. Empty / placeholder / yesterday
tickers always auto-discover.
"""

from __future__ import annotations

import logging
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from typing import Any, Iterable, Sequence

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
    "KXEGYPLGAME",
    "KXEGYPLTOTAL",
    "KXTFF1LIGGAME",
    "KXTFF1LIGTOTAL",
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
    "KXEGYPLGAME",
    "KXTFF1LIGGAME",
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
    "KXEGYPLTOTAL",
    "KXTFF1LIGTOTAL",
)

MIN_VOLUME_THRESHOLD = 50
MIN_24H_VOLUME_THRESHOLD = 100
TOTAL_ATM_TARGET = 0.50
TOTAL_BOND_YES = 0.88  # skip ~90¢ O0.5 bonds when picking the scalp total
# Next-up farther than this from 50¢ during a no-goal grind → swap to the
# cheaper adjacent strike (e.g. O4.5 at 12¢ → O2.5 while ATM is O3.5).
TOTAL_WING_DRIFT = 0.22
# Drop untradeable / missing-bid / junk longshot wings (El Gouna O3.5 at 5¢).
TOTAL_DEAD_YES = 0.10
# Ignore 80¢-wide longshot books whose mid luckily prints ~50¢ (e.g. O6.5 8¢/95¢).
TOTAL_MAX_SPREAD = 0.25
# Kickoff window for "today / tonight" tape. close_time is market expiry (often
# +2–3 days) so we rank on occurrence_datetime instead.
LIVE_LOOKBACK_HOURS = 4
SOON_HORIZON_HOURS = 18
FINISHED_AFTER_KICKOFF_HOURS = 2.5
FINISHED_HARD_HOURS = 4.0

# Prefix list is a fetch *boost*, never a closed allowlist.
SOCCER_SERIES_RE = re.compile(r"^KX[A-Z0-9]+(GAME|TOTAL)$")
TICKER_DATE_RE = re.compile(
    r"-(\d{2})(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)(\d{2})",
    re.IGNORECASE,
)
_MONTHS = {
    "JAN": 1,
    "FEB": 2,
    "MAR": 3,
    "APR": 4,
    "MAY": 5,
    "JUN": 6,
    "JUL": 7,
    "AUG": 8,
    "SEP": 9,
    "OCT": 10,
    "NOV": 11,
    "DEC": 12,
}
NON_SOCCER_SERIES_HINTS = (
    "NFL",
    "MLB",
    "NBA",
    "NHL",
    "WNBA",
    "NCAAF",
    "NCAAB",
    "ATP",
    "WTA",
    "TENNIS",
    "GOLF",
    "MMA",
    "UFC",
    "NASCAR",
    "FORMULA",
)
NON_SOCCER_TITLE_HINTS = (
    "nfl",
    "mlb",
    "nba",
    "nhl",
    "wnba",
    "ncaaf",
    "ncaab",
    "college football",
    "atp ",
    "wta ",
    "tennis",
    "golf",
    "pga ",
    "mma",
    "ufc",
    "nascar",
)

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
    tie_ml_ticker: str | None = None
    status: str = ""
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
        if self.tie_ml_ticker:
            tickers.append(self.tie_ml_ticker)
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


def ticker_embedded_date(ticker: str) -> date | None:
    """Parse the `-26AUG31-` calendar date Kalshi embeds in soccer tickers."""
    match = TICKER_DATE_RE.search((ticker or "").upper())
    if not match:
        return None
    year = 2000 + int(match.group(1))
    month = _MONTHS.get(match.group(2))
    day = int(match.group(3))
    if month is None:
        return None
    try:
        return date(year, month, day)
    except ValueError:
        return None


def is_stale_lab_ticker(ticker: str, *, now: datetime | None = None) -> bool:
    """Placeholder or yesterday/finished pin — never treat as a live fund list."""
    token = (ticker or "").strip()
    if is_placeholder_ticker(token):
        return True
    now_utc = now or datetime.now(tz=timezone.utc)
    embedded = ticker_embedded_date(token)
    if embedded is not None and embedded < now_utc.date():
        return True
    return False


def is_explicit_kalshi_ticker(ticker: str, *, now: datetime | None = None) -> bool:
    """Real KX… ticker the user typed on the CLI — not a .env leftover."""
    token = (ticker or "").strip()
    if not token.upper().startswith("KX"):
        return False
    if is_stale_lab_ticker(token, now=now):
        return False
    return True


def parse_cli_tickers(cli_tickers: str | None) -> list[str]:
    """Parse `--tickers` only. Never read LAB_TICKERS from the environment."""
    raw = (cli_tickers or "").strip()
    if not raw or raw.lower() in PLACEHOLDER_TICKER_TOKENS:
        return []
    return [t.strip() for t in raw.split(",") if t.strip()]


def needs_auto_discover(
    tickers: list[str] | None,
    *,
    now: datetime | None = None,
) -> bool:
    """Empty, placeholder, or yesterday/finished pins must auto-discover.

    Hardcoded `.env LAB_TICKERS` is not a pin list. A real KX… ticker the
    user typed today on the CLI is the only thing that skips discovery.
    """
    cleaned = [t.strip() for t in (tickers or []) if t and t.strip()]
    if not cleaned:
        return True
    if all(is_placeholder_ticker(t) for t in cleaned):
        return True
    if any(is_stale_lab_ticker(t, now=now) for t in cleaned):
        return True
    if not any(is_explicit_kalshi_ticker(t, now=now) for t in cleaned):
        return True
    return False


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
    yes_bid: float | None = None
    untradeable: bool = False

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


def is_dead_wing(book: TotalBook, *, floor: float = TOTAL_DEAD_YES) -> bool:
    """Untradeable, bid missing, or YES ≤ ~10¢ — never fund as ATM or next-up.

    Constructed unit books with only a mid (yes_bid=None, untradeable=False)
    are not dead just because the bid was omitted.
    """
    if book.untradeable:
        return True
    if not book.liquid:
        return True
    if book.yes_price is not None and book.yes_price <= floor:
        return True
    if book.yes_bid is not None and book.yes_bid <= floor:
        return True
    return False


def market_is_liquid(market: dict, volume: float, volume_24h: float) -> bool:
    if volume >= MIN_VOLUME_THRESHOLD or volume_24h >= MIN_24H_VOLUME_THRESHOLD:
        return True
    bid = _parse_dollar_price(market.get("yes_bid_dollars") or market.get("yes_bid"))
    ask = _parse_dollar_price(market.get("yes_ask_dollars") or market.get("yes_ask"))
    return bid is not None and ask is not None


def _fundable_total(book: TotalBook) -> bool:
    """ATM candidate: live mid, not a 90¢ bond, not a 5¢ junk wing, not a 80¢ hole."""
    if book.yes_price is None:
        return False
    if is_dead_wing(book) or is_bond_yes(book.yes_price) or not book.tight_enough:
        return False
    return True


def _wing_ok(book: TotalBook) -> bool:
    """Next-up / cheap-adjacent: liquid and not dead. Wide-but-alive 30¢ books stay."""
    if is_dead_wing(book):
        return False
    if book.yes_price is not None and is_bond_yes(book.yes_price):
        return False
    return True


def _cheaper_adjacent(
    books: list[TotalBook],
    atm: TotalBook,
) -> TotalBook | None:
    """O2.5 then O1.5 when ATM is O3.5 and the up-wing is dead or drifted."""
    by_strike = {b.strike: b for b in books}
    for delta in (1, 2):
        down = by_strike.get(atm.strike - delta)
        if down is not None and down.yes_price is not None and _wing_ok(down):
            return down
    return None


def select_scalp_totals(books: list[TotalBook]) -> tuple[TotalBook | None, TotalBook | None]:
    """ATM = live YES nearest 50¢. Up = next strike if liquid and not dead.

    1-1 / ≥3 goals → O3.5+O4.5 only when those books *are* the 50¢ tape.
    A 0-1 / 1-0 grind with O1.5 at ~50¢ funds O1.5 (and O2.5 if that is
    the next live strike) — never keep O3.5/O4.5 as a score pin.

    Skips ~90¢ O0.5 bonds and YES≤10¢ junk wings. Live YES only.
    """
    priced = [b for b in books if _fundable_total(b)]
    if not priced:
        return None, None
    atm = min(
        priced,
        key=lambda b: (abs((b.yes_price or 0.0) - TOTAL_ATM_TARGET), -b.volume_24h, -b.volume, b.strike),
    )
    by_strike = {b.strike: b for b in books}
    up = by_strike.get(atm.strike + 1)
    if up is None or not _wing_ok(up):
        return atm, None
    return atm, up


def select_ingame_totals(
    books: list[TotalBook],
    *,
    drop_far_wing: bool = False,
    drift: float = TOTAL_WING_DRIFT,
) -> tuple[TotalBook | None, TotalBook | None]:
    """Re-pick totals from *current* live YES. Score rules are ATM, not pins.

    At 1-1, O2.5 is often 70–85¢ so ATM is O3.5 and next-up is O4.5 — but
    only while those prices sit near 50¢. If the game is 0-1 / 1-0 and
    O1.5 is the 50¢ book, fund O1.5. Dead wings (no bid, untradeable,
    YES < ~10¢) are dropped immediately.

    When the next-up strike exists but is dead, or has drifted far from
    50¢ (`drop_far_wing` grind), swap to the cheaper adjacent (O2.5 or
    O1.5), never keep a junk O3.5/O4.5.
    """
    atm, up = select_scalp_totals(books)
    if atm is None:
        return None, None
    by_strike = {b.strike: b for b in books}
    up_raw = by_strike.get(atm.strike + 1)
    up_dead = up_raw is not None and not _wing_ok(up_raw)
    up_far = (
        up is not None
        and up.yes_price is not None
        and abs(up.yes_price - TOTAL_ATM_TARGET) > drift
    )
    need_cheap = up_dead or (drop_far_wing and (up is None or up_far))
    if not need_cheap:
        return atm, up
    down = _cheaper_adjacent(books, atm)
    if down is not None:
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
        cheap = wing.strike < atm.strike
        mode = "grind-cheap-side" if cheap else "live-atm+up"
        game.totals_repick = f"{mode} {atm.label}/{wing.label}"
    elif atm:
        game.totals_repick = f"live-atm {atm.label}"
    else:
        game.totals_repick = "no liquid live total"
    return game


_TOTALS_COPY_FIELDS = (
    "total_atm_ticker",
    "total_atm_label",
    "total_atm_price",
    "total_up_ticker",
    "total_up_label",
    "total_up_price",
    "over_05_ticker",
    "over_15_ticker",
    "totals_repick",
    "in_play_hint",
    "status",
    "tie_ml_ticker",
    "total_books",
)


def copy_totals_fields(dst: SoccerGame, src: SoccerGame) -> None:
    """Copy live ATM / wing selection onto the session's game object."""
    for attr in _TOTALS_COPY_FIELDS:
        setattr(dst, attr, getattr(src, attr))


def unfunded_tickers(before: Sequence[str], after: Sequence[str]) -> list[str]:
    """Tickers that left the fund list (dead wings, finished books)."""
    keep = {t for t in after if t}
    return [t for t in before if t and t not in keep]


def repick_session_totals(
    current_games: list[SoccerGame],
    fresh_games: list[SoccerGame],
    *,
    drop_far_wing: bool = False,
    now: datetime | None = None,
) -> tuple[list[SoccerGame], list[str], list[str]]:
    """Timer rediscover: live ATM, drop dead wings, drop finished games.

    Returns (kept_games, fund_tickers, drop_tickers). Does not invent fills.
    """
    for game in fresh_games:
        if game.total_books:
            apply_live_totals(game, game.total_books, drop_far_wing=drop_far_wing)

    before: dict[str, list[str]] = {}
    for game in current_games:
        key = game.event_ticker or id(game)
        before[key] = list(game.get_tickers())

    known = {g.event_ticker: g for g in current_games if g.event_ticker}
    kept: list[SoccerGame] = list(current_games)
    live_events = {g.event_ticker for g in fresh_games if g.event_ticker}

    for game in fresh_games:
        old = known.get(game.event_ticker)
        if old is None:
            kept.append(game)
            known[game.event_ticker] = game
        else:
            copy_totals_fields(old, game)

    drop: list[str] = []
    still: list[SoccerGame] = []
    for old in kept:
        fresh = known.get(old.event_ticker) if old.event_ticker else None
        candidate = fresh if fresh is not None else old
        finished = is_finished_game(candidate, now=now) or (
            old.event_ticker
            and old.event_ticker not in live_events
            and is_finished_game(old, now=now)
        )
        if finished:
            drop.extend(old.get_tickers())
            continue
        still.append(old)
        prev = before.get(old.event_ticker or id(old), [])
        drop.extend(unfunded_tickers(prev, old.get_tickers()))

    fund: list[str] = []
    seen: set[str] = set()
    for game in still:
        for ticker in game.get_tickers():
            if ticker in seen:
                continue
            seen.add(ticker)
            fund.append(ticker)

    # Unique drop list, never drop something we still fund.
    drop = [t for t in dict.fromkeys(drop) if t not in seen]
    return still, fund, drop


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


def is_finished_game(game: SoccerGame, *, now: datetime | None = None) -> bool:
    """Settled, yesterday, or kickoff + ~2.5h with no in-play hint — never fund."""
    now_utc = now or datetime.now(tz=timezone.utc)
    status = (game.status or "").strip().lower()
    if status in {"settled", "closed", "finalized", "determined", "inactive", "resolved"}:
        return True

    for raw in (game.event_ticker, game.home_ml_ticker, game.away_ml_ticker, game.series):
        if raw and is_stale_lab_ticker(raw, now=now_utc):
            return True

    kickoff = game.kickoff
    if kickoff is not None:
        age = now_utc - kickoff
        if age >= timedelta(hours=FINISHED_HARD_HOURS):
            return True
        if age >= timedelta(hours=FINISHED_AFTER_KICKOFF_HOURS) and not game.in_play_hint:
            return True

    close = _parse_iso(game.close_time)
    if close is not None and now_utc > close and not is_in_play(game, now=now_utc):
        return True
    return False


def is_watchable(
    game: SoccerGame,
    *,
    now: datetime | None = None,
    lookback_hours: float = LIVE_LOOKBACK_HOURS,
    horizon_hours: float = SOON_HORIZON_HOURS,
) -> bool:
    """Live, soon, or already in-play by bonded totals (kickoff clock may lag)."""
    if is_finished_game(game, now=now):
        return False
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
    """In-play first, then kickoff-soon, then 24h volume. No team-name bias."""
    notes: list[str] = []
    liveable = [g for g in games if not is_finished_game(g, now=now)]
    soon = [g for g in liveable if is_watchable(g, now=now)]
    later = [g for g in liveable if g not in soon]
    later.sort(key=lambda g: g.total_24h_volume, reverse=True)

    in_play = [g for g in soon if is_in_play(g, now=now)]
    in_play.sort(key=lambda g: g.total_24h_volume, reverse=True)
    selected: list[SoccerGame] = []
    for game in in_play:
        if len(selected) >= max_games:
            break
        selected.append(game)
        notes.append(f"in-play auto-fund: {game.title[:48]} (24h {game.total_24h_volume:.0f})")

    rest = [g for g in soon if g not in selected]
    rest.sort(key=lambda g: (g.kickoff or now, -g.total_24h_volume))
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


def _market_text_blob(market: dict) -> str:
    return " ".join(
        str(market.get(key) or "")
        for key in (
            "title",
            "subtitle",
            "yes_sub_title",
            "no_sub_title",
            "rules_primary",
            "rules_secondary",
        )
    ).lower()


def _series_from_market(market: dict) -> str:
    series = str(market.get("series_ticker") or "").strip().upper()
    if series:
        return series
    ticker = str(market.get("ticker") or "")
    return ticker.split("-", 1)[0].upper() if ticker else ""


def is_soccer_series_ticker(series: str) -> bool:
    """KX*GAME / KX*TOTAL that is not a non-soccer sport. Prefix list is not required."""
    token = (series or "").strip().upper()
    if not SOCCER_SERIES_RE.match(token):
        return False
    for hint in NON_SOCCER_SERIES_HINTS:
        if token.startswith(f"KX{hint}"):
            return False
    return True


def soccer_series_tickers_from_catalog(rows: Sequence[dict] | Iterable[dict]) -> list[str]:
    """Soccer-tagged GAME/TOTAL series from GET /series. Skip deleted titles."""
    out: list[str] = []
    seen: set[str] = set()
    for row in rows:
        ticker = str(row.get("ticker") or "").strip().upper()
        if not ticker or ticker in seen:
            continue
        title = str(row.get("title") or "")
        if "delete" in title.lower():
            continue
        tags = [str(t).lower() for t in (row.get("tags") or [])]
        if "soccer" not in tags and not is_soccer_series_ticker(ticker):
            continue
        if not (ticker.endswith("GAME") or ticker.endswith("TOTAL")):
            continue
        if not is_soccer_series_ticker(ticker):
            continue
        seen.add(ticker)
        out.append(ticker)
    return out


def looks_like_soccer_market(market: dict) -> bool:
    """Fingerprint: 'goals scored' copy or soccer GAME/TOTAL series, not NFL/MLB/…"""
    series = _series_from_market(market)
    blob = _market_text_blob(market)
    if any(hint in blob for hint in NON_SOCCER_TITLE_HINTS):
        return False
    for hint in NON_SOCCER_SERIES_HINTS:
        if series.startswith(f"KX{hint}"):
            return False
    if "goals scored" in blob:
        return True
    if "soccer" in blob:
        return True
    if is_soccer_series_ticker(series):
        return True
    if series in SOCCER_SERIES_PREFIXES:
        return True
    return False


def filter_soccer_markets(markets: Sequence[dict]) -> list[dict]:
    """Keep soccer books even when their series is missing from the prefix tuple."""
    return [m for m in markets if looks_like_soccer_market(m)]


def _get_with_retry(
    session: requests.Session,
    url: str,
    params: dict,
    timeout: float,
    label: str,
) -> dict | None:
    try:
        resp = session.get(url, params=params, timeout=timeout)
        if resp.status_code == 429:
            logger.warning("Rate-limited on %s; retrying once", label)
            time.sleep(1.5)
            resp = session.get(url, params=params, timeout=timeout)
        if resp.status_code != 200:
            logger.warning("HTTP %s on %s", resp.status_code, label)
            return None
        payload = resp.json()
        return payload if isinstance(payload, dict) else None
    except requests.RequestException as exc:
        logger.warning("Failed %s: %s", label, exc)
        return None


def fetch_soccer_series_tickers(
    session: requests.Session,
    rest_base: str,
    timeout: float = 15.0,
) -> list[str]:
    """Catalog-first soccer series. Prefix list is appended as a boost only."""
    rows: list[dict] = []
    cursor = None
    for _ in range(20):
        params: dict[str, Any] = {"limit": 200}
        if cursor:
            params["cursor"] = cursor
        payload = _get_with_retry(session, f"{rest_base}/series", params, timeout, "series")
        if not payload:
            break
        chunk = payload.get("series") or payload.get("series_list") or []
        rows.extend(chunk)
        cursor = payload.get("cursor") or payload.get("next_cursor")
        if not cursor or not chunk:
            break
    catalog = soccer_series_tickers_from_catalog(rows)
    seen = set(catalog)
    out = list(catalog)
    for prefix in SOCCER_SERIES_PREFIXES:
        if prefix not in seen:
            seen.add(prefix)
            out.append(prefix)
    return out


def _fetch_series_markets(rest_base: str, series: str, timeout: float) -> list[dict]:
    session = requests.Session()
    session.headers.update({"User-Agent": "suspension-lab/0.1"})
    payload = _get_with_retry(
        session,
        f"{rest_base}/markets",
        {"series_ticker": series, "status": "open", "limit": 200},
        timeout,
        series,
    )
    if not payload:
        return []
    return list(payload.get("markets") or [])


def fetch_open_soccer_markets(
    rest_base: str = KALSHI_API_BASE,
    timeout: float = 15.0,
) -> list[dict]:
    """Open soccer markets by fingerprint + catalog. Prefix list is a boost only.

    A live Egypt / TFF / Coppa book is kept even if its series is not in
    SOCCER_SERIES_PREFIXES. NFL/MLB/NBA/NHL and other non-soccer sports are dropped.
    """
    session = requests.Session()
    session.headers.update({"User-Agent": "suspension-lab/0.1"})

    by_ticker: dict[str, dict] = {}

    def _absorb(markets: Sequence[dict]) -> None:
        for market in filter_soccer_markets(markets):
            ticker = market.get("ticker")
            if ticker:
                by_ticker[str(ticker)] = market

    series_list = fetch_soccer_series_tickers(session, rest_base, timeout)
    workers = min(12, max(4, len(series_list) or 4))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(_fetch_series_markets, rest_base, series, timeout): series
            for series in series_list
        }
        for fut in as_completed(futures):
            series = futures[fut]
            try:
                _absorb(fut.result())
            except Exception as exc:  # noqa: BLE001
                logger.warning("series fetch %s failed: %s", series, exc)

    # Global open-market scan so a brand-new league is not dropped if /series lags.
    cursor = None
    for page in range(8):
        params: dict[str, Any] = {"status": "open", "limit": 200}
        if cursor:
            params["cursor"] = cursor
        payload = _get_with_retry(
            session, f"{rest_base}/markets", params, timeout, f"markets-page-{page}"
        )
        if not payload:
            break
        chunk = payload.get("markets") or []
        _absorb(chunk)
        cursor = payload.get("cursor") or payload.get("next_cursor")
        if not cursor or not chunk:
            break

    logger.debug("Fingerprint soccer fetch kept %s markets", len(by_ticker))
    return list(by_ticker.values())


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
    status = ""
    for market in markets:
        raw_status = str(market.get("status") or "").strip()
        if raw_status:
            status = raw_status
            if raw_status.lower() not in {"open", "active"}:
                break

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
        status=status,
    )

    game_tickers: list[tuple[str, str]] = []
    tie_ticker: str | None = None
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
                yes = yes_price_from_market(market)
                if (
                    market_is_liquid(market, vol, vol_24h)
                    and not is_bond_yes(yes)
                ):
                    tie_ticker = ticker
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
                    yes_bid=bid,
                    untradeable=bid is None,
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
    if tie_ticker:
        game.tie_ml_ticker = tie_ticker
        game.reasons.append("TIE funded (liquid)")

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
    games = [g for g in games if not is_finished_game(g, now=now)]
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
        "In-game totals follow **live YES nearest 50¢** (ATM) plus the next "
        "liquid strike. 1-1 / ≥3 goals → O3.5+O4.5 only when those books are "
        "the 50¢ tape — not a hard pin. A 0-1 grind with O1.5 at 50¢ funds "
        "O1.5. Dead wings (no bid, YES < ~10¢) are dropped on the rediscover timer.",
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
