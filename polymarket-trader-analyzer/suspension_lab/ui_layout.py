"""Designer-lock helpers for the paper-lab board. No Tk import."""

from __future__ import annotations

from suspension_lab.soccer_discovery import SoccerGame

WINDOW_GEOMETRY = "1100x720"
WINDOW_MIN_WIDTH = 900
WINDOW_MIN_HEIGHT = 600
GRID_BREAK_PX = 1000
TICKER_FONT = ("Consolas", 11)
PRICE_FONT = ("Consolas", 16, "bold")
LINE_FONT = ("Segoe UI", 10, "bold")


def tile_columns_for_width(width: int) -> int:
    """3 columns when the card is at least 1000px wide, else 2. Never a single row."""
    return 3 if int(width) >= GRID_BREAK_PX else 2


def format_yes_price(value) -> str:
    """Missing YES price is ASCII '-' (never an em dash)."""
    if value is None or value == "" or value == "?":
        return "-"
    return str(value)


def matchup_hero(game: SoccerGame) -> str:
    """English matchup for the card hero - not a raw KX ticker."""
    title = (game.title or "").strip()
    if title and not title.upper().startswith("KX"):
        return title
    home = (game.home_team or "").strip()
    away = (game.away_team or "").strip()
    if home and away:
        return f"{home} vs {away}"
    if home or away:
        return home or away
    return "Soccer match"
