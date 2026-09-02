"""Look-only desk helpers: English titles, ASCII '-', flash/P&L/stale copy."""

from datetime import datetime, timezone
from pathlib import Path

from suspension_lab.market_labels import MarketLabel
from suspension_lab.soccer_discovery import SoccerGame
from suspension_lab.tape_engine import TapeEvent
from suspension_lab.ui_layout import (
    FLASH_SECONDS,
    HEARTBEAT_MS,
    PRICE_FONT,
    STATUS_FONT,
    TICKER_FONT,
    ascii_text,
    english_line,
    format_clock,
    format_last_book,
    format_paper_pnl,
    format_tape_line,
    format_yes_cents,
    format_yes_price,
    health_badge_text,
    matchup_hero,
    show_on_tape,
    slot_title_for_ticker,
    stale_banner_text,
    tape_kind_tag,
    ticker_subtitle,
)

UI_PY = Path(__file__).resolve().parents[1] / "suspension_lab" / "ui.py"
LAYOUT_PY = Path(__file__).resolve().parents[1] / "suspension_lab" / "ui_layout.py"


def _game() -> SoccerGame:
    return SoccerGame(
        event_ticker="KXCOPPAITALIAGAME-26SEP02UDIVEN",
        title="Udinese vs Venezia",
        home_team="Udinese",
        away_team="Venezia",
        close_time="",
        total_atm_label="ATM total",
        total_atm_ticker="KXCOPPAITALIATOTAL-26SEP02UDIVEN-4",
    )


class TestAsciiAndPrices:
    def test_strips_em_en_dash_and_mojibake(self):
        assert ascii_text("Peru Liga 1 \u2014 Atletico") == "Peru Liga 1 - Atletico"
        assert ascii_text("a \u2013 b") == "a - b"
        assert "-" in ascii_text("â€”")
        assert "\u2014" not in ascii_text("\u2014")
        assert "\u2013" not in ascii_text("\u2013")

    def test_missing_yes_is_ascii_hyphen(self):
        assert format_yes_price(None) == "-"
        assert format_yes_cents(None) == "-"
        assert format_yes_cents("") == "-"
        assert format_yes_cents("?") == "-"
        assert format_yes_cents("0.24") == "24"
        assert format_yes_cents("0.36") == "36"
        assert format_yes_cents(0.24) == "24"

    def test_source_has_no_em_dash(self):
        for path in (UI_PY, LAYOUT_PY):
            text = path.read_text(encoding="utf-8")
            assert "\u2014" not in text
            assert "\u2013" not in text


class TestEnglishTitles:
    def test_hero_prefers_label_matchup(self):
        label = MarketLabel(
            ticker="KXCOPPAITALIATOTAL-26SEP02UDIVEN-4",
            display="Serie A \u2014 Udinese vs Venezia \u2014 Over 3.5",
            competition="Serie A",
            matchup="Udinese vs Venezia",
            line="Over 3.5",
        )
        raw = SoccerGame(
            event_ticker="KX",
            title="KXCOPPAITALIAGAME-26SEP02UDIVEN",
            home_team="",
            away_team="",
            close_time="",
        )
        assert matchup_hero(raw, label) == "Udinese vs Venezia"
        assert matchup_hero(_game()) == "Udinese vs Venezia"

    def test_line_never_kx_hero(self):
        label = MarketLabel(
            ticker="KXCOPPAITALIATOTAL-26SEP02UDIVEN-4",
            display="x",
            competition="",
            matchup="Udinese vs Venezia",
            line="ATM total",
        )
        assert english_line(label, "KXCOPPAITALIATOTAL-26SEP02UDIVEN-4") == "ATM total"
        assert english_line(None, "Home ML") == "Home ML"
        assert not slot_title_for_ticker(
            "KXCOPPAITALIATOTAL-26SEP02UDIVEN-4", "Book"
        ).upper().startswith("KX")
        assert ticker_subtitle("KXCOPPAITALIATOTAL-26SEP02UDIVEN-4").startswith("KX")


class TestTapeAndHealthCopy:
    def test_tape_english_and_hides_heartbeats(self):
        label = MarketLabel(
            ticker="T",
            display="Serie A \u2014 Udinese vs Venezia \u2014 Over 3.5",
            competition="Serie A",
            matchup="Udinese vs Venezia",
            line="Over 3.5",
        )
        event = TapeEvent(
            "GOAL",
            "T",
            label.display,
            "GOAL SIGNAL bid 0.24->0.36 (+12c)",
            "2026-09-02T16:09:11+00:00",
        )
        line = format_tape_line(event, label)
        assert "Udinese vs Venezia" in line
        assert "Over 3.5" in line
        assert "\u2014" not in line
        assert "GOAL" in line
        assert show_on_tape("GOAL")
        assert show_on_tape("FILL")
        assert show_on_tape("429")
        assert not show_on_tape("HEARTBEAT")
        assert not show_on_tape("PUMP")
        assert tape_kind_tag("EXIT") == "FILL"
        assert tape_kind_tag("429") == "LIMIT"

    def test_health_and_paper_strip(self):
        assert health_badge_text("429") == "RATE LIMITED"
        assert health_badge_text("LIVE") == "LIVE"
        assert format_last_book(0.4) == "last book 0.4s ago"
        assert format_last_book(None) == "last book -"
        assert stale_banner_text("STALE", 3.2) == "BOARD STALE - last tick 3s ago"
        assert stale_banner_text("FROZEN", 9) == "BOARD FROZEN - last tick 9s ago"
        assert "\u2014" not in stale_banner_text("STALE", 3)
        pnl = format_paper_pnl(12, 1, "Over 3.5 +8c")
        assert "P&L +12c" in pnl
        assert "OPEN 1" in pnl
        assert "LAST FILL" in pnl

    def test_clock_shows_tenths(self):
        now = datetime(2026, 9, 2, 16, 9, 11, 250000, tzinfo=timezone.utc)
        clock = format_clock(now)
        assert clock.endswith(".2")
        assert "16:09:11" in clock


class TestLookConstantsAndUiSource:
    def test_type_and_heartbeat(self):
        assert PRICE_FONT[1] > TICKER_FONT[1]
        assert STATUS_FONT[1] >= 11
        assert TICKER_FONT[1] == 11
        assert FLASH_SECONDS >= 4
        assert HEARTBEAT_MS == 250

    def test_ui_keeps_layout_pr_mechanics_and_look(self):
        src = UI_PY.read_text(encoding="utf-8")
        assert "MouseWheel" in src
        assert "Button-4" in src
        assert "winfo_width" in src
        assert "class BookGrid" in src
        assert "RATE LIMITED" in src or "health_badge_text" in src
        assert "PAPER" in src
        assert "GOAL_FLASH" in src
        assert 'insert("1.0"' in src
        assert "HEARTBEAT_MS" in src
        start = src.index("def _create_book_box")
        end = src.index("def _sync_trader_toggle")
        assert 'side="left"' not in src[start:end]
        assert "trader.config.live = False" in src
