"""Unit tests for bond spoof detection and per-line exit policies."""

import pytest
from suspension_lab.exit_engine import (
    is_bond_spoof_bid,
    is_total_05_ticker,
    get_per_line_exit_mode,
)


class TestIsBondSpoofBid:
    """Tests for is_bond_spoof_bid() — detect lowball bids on bonded markets."""

    def test_melgar_spoof_scenario(self):
        """MELGAR O0.5: peak 99¢, bid drops to 75¢ x7.6, ask stays 99¢ → spoof."""
        result = is_bond_spoof_bid(
            peak_cents=99,
            current_bid_cents=75,
            current_ask_cents=99,
            bid_qty=7.6,
        )
        assert result is True

    def test_zurich_collapse_scenario(self):
        """Zürich-like collapse: peak 85¢, bid drops to 60¢, ask also drops → real VAR."""
        result = is_bond_spoof_bid(
            peak_cents=85,
            current_bid_cents=60,
            current_ask_cents=65,
            bid_qty=50.0,
        )
        assert result is False

    def test_bonded_market_both_sides_drop(self):
        """Bonded market where both bid and ask collapse together → real VAR."""
        result = is_bond_spoof_bid(
            peak_cents=98,
            current_bid_cents=70,
            current_ask_cents=72,
            bid_qty=100.0,
        )
        assert result is False

    def test_peak_not_bonded(self):
        """Peak < 95¢ → not a bond situation, not spoof."""
        result = is_bond_spoof_bid(
            peak_cents=80,
            current_bid_cents=60,
            current_ask_cents=99,
            bid_qty=5.0,
        )
        assert result is False

    def test_ask_dropped_below_bond(self):
        """Ask dropped below 95¢ → market is reverting, not spoof."""
        result = is_bond_spoof_bid(
            peak_cents=99,
            current_bid_cents=75,
            current_ask_cents=80,
            bid_qty=5.0,
        )
        assert result is False

    def test_spread_too_tight(self):
        """Spread < 10¢ → not a spoof pattern (market makers still there)."""
        result = is_bond_spoof_bid(
            peak_cents=99,
            current_bid_cents=92,
            current_ask_cents=99,
            bid_qty=5.0,
        )
        assert result is False

    def test_large_qty_not_spoof(self):
        """Large bid qty (> 100) on bonded market → probably real, not spoof."""
        result = is_bond_spoof_bid(
            peak_cents=99,
            current_bid_cents=75,
            current_ask_cents=99,
            bid_qty=150.0,
        )
        assert result is False

    def test_thin_qty_is_spoof(self):
        """Thin bid qty (< 100) with wide spread → likely spoof."""
        result = is_bond_spoof_bid(
            peak_cents=99,
            current_bid_cents=70,
            current_ask_cents=99,
            bid_qty=50.0,
        )
        assert result is True

    def test_no_ask_data(self):
        """No ask data available → cannot determine spoof."""
        result = is_bond_spoof_bid(
            peak_cents=99,
            current_bid_cents=75,
            current_ask_cents=None,
            bid_qty=5.0,
        )
        assert result is False


class TestIsTotal05Ticker:
    """Tests for is_total_05_ticker() — identify O0.5 totals lines."""

    def test_o05_ticker(self):
        """TOTAL ticker ending in -1 is O0.5."""
        assert is_total_05_ticker("KXPERLIGA1TOTAL-26AUG31CAGMEL-1") is True

    def test_o15_ticker(self):
        """TOTAL ticker ending in -2 is O1.5, not O0.5."""
        assert is_total_05_ticker("KXPERLIGA1TOTAL-26AUG31CAGMEL-2") is False

    def test_o25_ticker(self):
        """TOTAL ticker ending in -3 is O2.5, not O0.5."""
        assert is_total_05_ticker("KXPERLIGA1TOTAL-26AUG31CAGMEL-3") is False

    def test_moneyline_ticker(self):
        """GAME ticker (moneyline) is not a totals line."""
        assert is_total_05_ticker("KXPERLIGA1GAME-26AUG31CAGMEL-CAG") is False
        assert is_total_05_ticker("KXPERLIGA1GAME-26AUG31CAGMEL-MEL") is False

    def test_no_total_keyword(self):
        """Ticker without TOTAL is not a totals line."""
        assert is_total_05_ticker("SOME-OTHER-TICKER-1") is False

    def test_lowercase(self):
        """Case insensitive check for TOTAL."""
        assert is_total_05_ticker("kxperliga1total-26aug31cagmel-1") is True


class TestGetPerLineExitMode:
    """Tests for get_per_line_exit_mode() — per-line exit policy."""

    def test_o05_bonded_forces_hold_bond(self):
        """O0.5 that has bonded should hold_bond, never scalp."""
        result = get_per_line_exit_mode(
            ticker="KXPERLIGA1TOTAL-26AUG31CAGMEL-1",
            base_exit_mode="scalp",
            is_bonded=True,
        )
        assert result == "hold_bond"

    def test_o05_not_bonded_keeps_base(self):
        """O0.5 that hasn't bonded keeps its base mode."""
        result = get_per_line_exit_mode(
            ticker="KXPERLIGA1TOTAL-26AUG31CAGMEL-1",
            base_exit_mode="scalp",
            is_bonded=False,
        )
        assert result == "scalp"

    def test_o15_keeps_base_mode(self):
        """O1.5+ tickers keep their base exit mode."""
        result = get_per_line_exit_mode(
            ticker="KXPERLIGA1TOTAL-26AUG31CAGMEL-2",
            base_exit_mode="scalp",
            is_bonded=True,
        )
        assert result == "scalp"

    def test_moneyline_keeps_base_mode(self):
        """Moneyline tickers keep their base exit mode."""
        result = get_per_line_exit_mode(
            ticker="KXPERLIGA1GAME-26AUG31CAGMEL-CAG",
            base_exit_mode="var_watch",
            is_bonded=True,
        )
        assert result == "var_watch"

    def test_moneyline_scalp_allowed(self):
        """Moneyline tickers can scalp +7."""
        result = get_per_line_exit_mode(
            ticker="KXPERLIGA1GAME-26AUG31CAGMEL-MEL",
            base_exit_mode="scalp",
            is_bonded=False,
        )
        assert result == "scalp"
