"""Designer-lock helpers for the paper-lab board. No Tk import.

Mechanical wrap/scroll lives in ui.py (BookGrid / canvas). This module owns
English copy, ASCII punctuation, fonts, tape/P&L/heartbeat strings.
"""

from __future__ import annotations

from datetime import datetime

from suspension_lab.market_labels import MarketLabel
from suspension_lab.soccer_discovery import SoccerGame

WINDOW_GEOMETRY = "1100x720"
WINDOW_MIN_WIDTH = 900
WINDOW_MIN_HEIGHT = 600
GRID_BREAK_PX = 1000
TICKER_FONT = ("Consolas", 11)
PRICE_FONT = ("Consolas", 22, "bold")
LINE_FONT = ("Segoe UI", 10, "bold")
DISPLAY_FONT = ("Segoe UI", 13, "bold")
STATUS_FONT = ("Segoe UI", 11)
CLOCK_FONT = ("Consolas", 11)
TAPE_FONT = ("Consolas", 10)
FLASH_SECONDS = 5
HEARTBEAT_MS = 250
TAPE_HIDE_KINDS = frozenset({"HEARTBEAT", "HB", "PUMP", "TICK", "BOOK", "HEALTH"})

_DASH_REPLACEMENTS = (
    "\u2014",  # em dash
    "\u2013",  # en dash
    "\u2012",  # figure dash
    "\u2212",  # minus
    "â€”",
    "â€“",
    "â€�",
)


def ascii_text(value: object) -> str:
    """Replace em/en dashes and common mojibake with ASCII '-'."""
    text = "" if value is None else str(value)
    for bad in _DASH_REPLACEMENTS:
        text = text.replace(bad, "-")
    return text


def tile_columns_for_width(width: int) -> int:
    """3 columns when the card is at least 1000px wide, else 2. Never a single row."""
    return 3 if int(width) >= GRID_BREAK_PX else 2


def format_yes_price(value) -> str:
    """Missing YES price is ASCII '-' (never an em dash)."""
    if value is None or value == "" or value == "?":
        return "-"
    return str(value)


def format_yes_cents(value) -> str:
    """Large board number in cents, or ASCII '-'."""
    if value is None or value == "" or value == "?":
        return "-"
    try:
        raw = float(value)
    except (TypeError, ValueError):
        return "-"
    if 0.0 <= raw <= 1.0:
        return str(int(round(raw * 100)))
    return str(int(round(raw)))


def matchup_hero(game: SoccerGame, label: MarketLabel | None = None) -> str:
    """English matchup for the card hero - not a raw KX ticker."""
    if label is not None and (label.matchup or "").strip():
        return ascii_text(label.matchup.strip())
    title = (game.title or "").strip()
    if title and not title.upper().startswith("KX"):
        return ascii_text(title)
    home = (game.home_team or "").strip()
    away = (game.away_team or "").strip()
    if home and away:
        return ascii_text(f"{home} vs {away}")
    if home or away:
        return ascii_text(home or away)
    return "Soccer match"


def english_line(label: MarketLabel | None, fallback: str) -> str:
    """Book-tile title: ATM total / Over 3.5 / Home ML. Never a KX ticker."""
    if label is not None and (label.line or "").strip():
        line = ascii_text(label.line.strip())
        if line and not line.upper().startswith("KX"):
            return line
    text = ascii_text(fallback or "Book")
    if text.upper().startswith("KX"):
        return "Book"
    return text or "Book"


def ticker_subtitle(ticker: str) -> str:
    """11px mono subtitle only - never the hero."""
    return ascii_text(ticker or "-")


def slot_title_for_ticker(ticker: str, fallback: str) -> str:
    """English line for a loose/manual book. Uses MarketLabel.fallback."""
    return english_line(MarketLabel.fallback(ticker), fallback)


def tape_kind_tag(kind: str) -> str:
    key = (kind or "").upper()
    if key in {"EXIT", "FILL"}:
        return "FILL"
    if key in {"429", "LIMIT", "RATE"}:
        return "LIMIT"
    return key


def show_on_tape(kind: str) -> bool:
    """Hide heartbeat/pump firehose. GOAL / FILL / 429 stay."""
    return tape_kind_tag(kind) not in TAPE_HIDE_KINDS


def format_tape_line(event, label: MarketLabel | None = None) -> str:
    """Dense English tape row. Newest-on-top is the widget's job."""
    ts = ""
    raw_ts = getattr(event, "ts_iso", "") or ""
    if len(raw_ts) >= 19:
        ts = raw_ts[11:19]
    kind = ascii_text(getattr(event, "kind", "") or "")
    matchup = ""
    line = ""
    if label is not None:
        matchup = ascii_text((label.matchup or "").strip())
        line = ascii_text((label.line or "").strip())
    if not matchup:
        fallback = ascii_text(getattr(event, "label", "") or "")
        matchup = fallback.split(" - ")[0].strip() if fallback else ""
    detail = ascii_text(getattr(event, "detail", "") or "")
    parts = [p for p in (ts, kind, matchup, line, detail) if p]
    return "  ".join(parts)


def format_clock(now: datetime) -> str:
    """Tenth-second clock so a 250ms `after` tick is visible. If it stops, Tk is wedged."""
    tenth = int(now.microsecond / 100_000)
    return now.strftime("%H:%M:%S") + f".{tenth}"


def format_last_book(age_s: float | None) -> str:
    if age_s is None:
        return "last book -"
    return f"last book {age_s:.1f}s ago"


def stale_banner_text(health: str, age_s: float | None) -> str:
    n = "-" if age_s is None else str(int(age_s))
    if health == "FROZEN":
        return f"BOARD FROZEN - last tick {n}s ago"
    return f"BOARD STALE - last tick {n}s ago"


def health_badge_text(health: str) -> str:
    if health == "429":
        return "RATE LIMITED"
    return health or "LIVE"


def transport_label(*, ws_connected: bool, using_slow_rest: bool) -> str:
    if ws_connected:
        return "WS"
    if using_slow_rest:
        return "REST"
    return "IDLE"


def format_paper_pnl(session_cents: int, open_n: int, last_fill: str) -> str:
    fill = ascii_text(last_fill or "-")
    return f"P&L {session_cents:+d}c    OPEN {open_n}    LAST FILL {fill}"
