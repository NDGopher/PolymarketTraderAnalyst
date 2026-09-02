"""Tests for replay using books_long.csv format."""

import csv
import json
import tempfile
from pathlib import Path

import pytest

from suspension_lab.replay_goal_signals import replay_session


def _create_test_session(tmpdir: Path, use_long: bool = True) -> Path:
    """Create a minimal test session with goal signal + spoof scenario."""
    session_dir = tmpdir / "test_session"
    session_dir.mkdir()
    
    session_json = {
        "game_label": "TEST",
        "tickers": ["TICKER-ML", "TICKER-O05"],
        "started_at": "2026-09-01T21:00:00+00:00",
    }
    (session_dir / "session.json").write_text(json.dumps(session_json))
    
    if use_long:
        with (session_dir / "books_long.csv").open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "ts_ms", "ts_iso", "ticker", "yes_bid", "yes_ask", "yes_mid",
                "spread_cents", "yes_bid_qty", "yes_ask_qty", "tight_spread",
                "wide_spread", "untradeable"
            ])
            
            base_ms = 1788296940000
            
            for i, ms_offset in enumerate(range(0, 5000, 200)):
                ts_ms = base_ms + ms_offset
                ts_iso = f"2026-09-01T21:09:{ms_offset // 1000:02d}.{ms_offset % 1000:03d}000+00:00"
                
                writer.writerow([
                    ts_ms, ts_iso, "TICKER-ML",
                    "0.50", "0.52", "0.51", "2", "500", "500", "True", "False", "False"
                ])
                writer.writerow([
                    ts_ms, ts_iso, "TICKER-O05",
                    "0.60", "0.65", "0.625", "5", "200", "100", "False", "False", "False"
                ])
            
            ts_ms = base_ms + 5000
            ts_iso = "2026-09-01T21:09:05.000000+00:00"
            writer.writerow([
                ts_ms, ts_iso, "TICKER-ML",
                "0.65", "0.68", "0.665", "3", "500", "500", "True", "False", "False"
            ])
            writer.writerow([
                ts_ms, ts_iso, "TICKER-O05",
                "0.80", "0.85", "0.825", "5", "300", "150", "False", "False", "False"
            ])
            
            for ms_offset in range(5200, 10000, 200):
                ts_ms = base_ms + ms_offset
                ts_iso = f"2026-09-01T21:09:{ms_offset // 1000:02d}.{ms_offset % 1000:03d}000+00:00"
                
                writer.writerow([
                    ts_ms, ts_iso, "TICKER-ML",
                    "0.70", "0.72", "0.71", "2", "500", "500", "True", "False", "False"
                ])
                writer.writerow([
                    ts_ms, ts_iso, "TICKER-O05",
                    "0.98", "0.99", "0.985", "1", "200", "100", "True", "False", "False"
                ])
            
            ts_ms = base_ms + 10000
            ts_iso = "2026-09-01T21:09:10.000000+00:00"
            writer.writerow([
                ts_ms, ts_iso, "TICKER-ML",
                "0.70", "0.72", "0.71", "2", "500", "500", "True", "False", "False"
            ])
            writer.writerow([
                ts_ms, ts_iso, "TICKER-O05",
                "0.75", "0.99", "0.87", "24", "8", "100", "False", "True", "False"
            ])
            
            for ms_offset in range(10200, 15000, 200):
                ts_ms = base_ms + ms_offset
                ts_iso = f"2026-09-01T21:09:{ms_offset // 1000:02d}.{ms_offset % 1000:03d}000+00:00"
                
                writer.writerow([
                    ts_ms, ts_iso, "TICKER-ML",
                    "0.70", "0.72", "0.71", "2", "500", "500", "True", "False", "False"
                ])
                writer.writerow([
                    ts_ms, ts_iso, "TICKER-O05",
                    "0.99", "0.99", "0.99", "0", "200", "0", "False", "False", "True"
                ])
    
    return session_dir


class TestReplayLong:
    """Tests for replay using books_long.csv format."""

    def test_finds_goal_signal(self, tmp_path):
        """Replay should find goal signals from books_long.csv."""
        session_dir = _create_test_session(tmp_path, use_long=True)
        events = replay_session(session_dir)
        
        goal_events = [e for e in events if e.kind == "GOAL"]
        assert len(goal_events) >= 1

    def test_finds_spoof_notice(self, tmp_path):
        """Replay should detect spoof bid on bonded O0.5."""
        session_dir = _create_test_session(tmp_path, use_long=True)
        events = replay_session(session_dir)
        
        spoof_events = [e for e in events if e.kind == "SPOOF"]
        assert len(spoof_events) >= 1, f"Expected SPOOF event, got: {[e.kind for e in events]}"

    def test_no_var_on_spoof(self, tmp_path):
        """Spoof bid should NOT trigger VAR alert."""
        session_dir = _create_test_session(tmp_path, use_long=True)
        events = replay_session(session_dir)
        
        o05_events = [e for e in events if "O05" in e.ticker]
        var_events = [e for e in o05_events if e.kind == "VAR"]
        
        assert len(var_events) == 0, f"Got unexpected VAR: {var_events}"

    def test_prefers_long_over_wide(self, tmp_path):
        """When both books.csv and books_long.csv exist, prefer long."""
        session_dir = _create_test_session(tmp_path, use_long=True)
        
        with (session_dir / "books.csv").open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ts_ms", "ts_iso", "TICKER-ML_yes_bid", "TICKER-ML_yes_ask"])
            writer.writerow([1788296940000, "2026-09-01T21:09:00+00:00", "0.50", "0.52"])
        
        events = replay_session(session_dir)
        
        o05_events = [e for e in events if "O05" in e.ticker]
        assert len(o05_events) > 0, "Should have found O05 events from books_long.csv"
