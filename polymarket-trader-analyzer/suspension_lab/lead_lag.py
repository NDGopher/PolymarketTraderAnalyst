"""Lead/lag analysis: track which ticker moves first on goal episodes."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from suspension_lab.goal_signal import GoalSignal, GoalSignalDetector
from suspension_lab.orderbook import OrderBook


@dataclass
class LeadLagEntry:
    episode_ts_iso: str
    episode_ticker: str
    tracked_ticker: str
    ticker_type: str
    first_bid_jump_10c_ts_ms: int | None
    first_bid_jump_10c_ts_iso: str
    first_ask_jump_3c_ts_ms: int | None
    first_ask_jump_3c_ts_iso: str
    bid_jump_lag_ms: int | None
    ask_jump_lag_ms: int | None


def _short(ticker: str) -> str:
    parts = ticker.split("-")
    return "-".join(parts[-2:]) if len(parts) >= 2 else ticker


def _ticker_type(ticker: str) -> str:
    """Classify ticker as ML (moneyline), O0.5, O1.5, O2.5, etc."""
    ticker_upper = ticker.upper()
    if "GAME" in ticker_upper:
        if ticker.endswith("-MEL") or ticker.endswith("-CAG"):
            return "ML-away" if ticker.endswith("-MEL") else "ML-home"
        return "ML"
    if "TOTAL" in ticker_upper:
        import re
        match = re.search(r"-(\d+)$", ticker)
        if match:
            strike = int(match.group(1))
            goals = (strike - 1) / 2
            return f"O{goals:.1f}"
    return "unknown"


def _ticker_prefixes(headers: list[str]) -> list[str]:
    return [h[: -len("_yes_bid")] for h in headers if h.endswith("_yes_bid")]


def _find_first_jumps(
    ticker_rows: list[tuple[int, dict]],
    episode_ts_ms: int,
    window_ms: int = 30000,
    bid_jump_cents: int = 10,
    ask_jump_cents: int = 3,
) -> tuple[tuple[int, str] | None, tuple[int, str] | None]:
    """Find first bid jump ≥10c and first ask jump ≥3c after episode start.
    
    Returns ((bid_ts_ms, bid_ts_iso), (ask_ts_ms, ask_ts_iso)) or None for each.
    """
    prev_bid: Decimal | None = None
    prev_ask: Decimal | None = None
    first_bid_jump: tuple[int, str] | None = None
    first_ask_jump: tuple[int, str] | None = None
    
    for ts_ms, row in ticker_rows:
        if ts_ms < episode_ts_ms - 1000:
            bid_s = row.get("yes_bid", "") or row.get(f"{row.get('_prefix', '')}_yes_bid", "")
            ask_s = row.get("yes_ask", "") or row.get(f"{row.get('_prefix', '')}_yes_ask", "")
            if bid_s:
                prev_bid = Decimal(bid_s)
            if ask_s:
                prev_ask = Decimal(ask_s)
            continue
        
        if ts_ms > episode_ts_ms + window_ms:
            break
        
        bid_s = row.get("yes_bid", "") or row.get(f"{row.get('_prefix', '')}_yes_bid", "")
        ask_s = row.get("yes_ask", "") or row.get(f"{row.get('_prefix', '')}_yes_ask", "")
        ts_iso = row.get("ts_iso", "")
        
        if bid_s and prev_bid is not None and first_bid_jump is None:
            bid = Decimal(bid_s)
            jump = int(round((bid - prev_bid) * 100))
            if jump >= bid_jump_cents:
                first_bid_jump = (ts_ms, ts_iso)
        
        if ask_s and prev_ask is not None and first_ask_jump is None:
            ask = Decimal(ask_s)
            jump = int(round((ask - prev_ask) * 100))
            if jump >= ask_jump_cents:
                first_ask_jump = (ts_ms, ts_iso)
        
        if bid_s:
            prev_bid = Decimal(bid_s)
        if ask_s:
            prev_ask = Decimal(ask_s)
        
        if first_bid_jump and first_ask_jump:
            break
    
    return first_bid_jump, first_ask_jump


def analyze_lead_lag(session_dir: Path) -> tuple[list[LeadLagEntry], str]:
    """Analyze lead/lag timing across tickers for each goal episode."""
    long_path = session_dir / "books_long.csv"
    use_long = long_path.exists()
    
    entries: list[LeadLagEntry] = []
    episodes: list[tuple[int, str, str]] = []
    
    if use_long:
        with long_path.open(encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        
        tickers = sorted({r["ticker"] for r in rows if r.get("ticker")})
        detectors = {t: GoalSignalDetector() for t in tickers}
        
        ticker_rows: dict[str, list[tuple[int, dict]]] = {t: [] for t in tickers}
        for row in rows:
            ticker = row.get("ticker", "")
            if ticker and ticker in tickers:
                ticker_rows[ticker].append((int(row["ts_ms"]), row))
        
        for row in rows:
            ticker = row.get("ticker", "")
            if not ticker or ticker not in tickers:
                continue
            bid_s = row.get("yes_bid", "")
            ask_s = row.get("yes_ask", "")
            if not bid_s or not ask_s:
                continue
            ts_ms = int(row["ts_ms"])
            book = OrderBook(ticker)
            book.set_from_top(
                bid=bid_s,
                ask=ask_s,
                bid_qty=row.get("yes_bid_qty", "0") or "0",
                ask_qty=row.get("yes_ask_qty", "0") or "0",
                updated_ms=ts_ms,
            )
            result = detectors[ticker].evaluate(ticker, book)
            if isinstance(result, GoalSignal):
                episodes.append((ts_ms, row["ts_iso"], ticker))
        
        for ep_ts_ms, ep_ts_iso, ep_ticker in episodes:
            for ticker in tickers:
                first_bid, first_ask = _find_first_jumps(ticker_rows[ticker], ep_ts_ms)
                
                bid_lag = (first_bid[0] - ep_ts_ms) if first_bid else None
                ask_lag = (first_ask[0] - ep_ts_ms) if first_ask else None
                
                entries.append(LeadLagEntry(
                    episode_ts_iso=ep_ts_iso,
                    episode_ticker=ep_ticker,
                    tracked_ticker=ticker,
                    ticker_type=_ticker_type(ticker),
                    first_bid_jump_10c_ts_ms=first_bid[0] if first_bid else None,
                    first_bid_jump_10c_ts_iso=first_bid[1] if first_bid else "",
                    first_ask_jump_3c_ts_ms=first_ask[0] if first_ask else None,
                    first_ask_jump_3c_ts_iso=first_ask[1] if first_ask else "",
                    bid_jump_lag_ms=bid_lag,
                    ask_jump_lag_ms=ask_lag,
                ))
    else:
        books_path = session_dir / "books.csv"
        with books_path.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            prefixes = _ticker_prefixes(headers)
            rows = list(reader)
        
        detectors = {p: GoalSignalDetector() for p in prefixes}
        
        ticker_rows: dict[str, list[tuple[int, dict]]] = {p: [] for p in prefixes}
        for row in rows:
            ts_ms = int(row["ts_ms"])
            for prefix in prefixes:
                row_copy = dict(row)
                row_copy["_prefix"] = prefix
                row_copy["yes_bid"] = row.get(f"{prefix}_yes_bid", "")
                row_copy["yes_ask"] = row.get(f"{prefix}_yes_ask", "")
                ticker_rows[prefix].append((ts_ms, row_copy))
        
        for i, row in enumerate(rows):
            ts_ms = int(row["ts_ms"])
            for prefix in prefixes:
                bid_s = row.get(f"{prefix}_yes_bid", "")
                ask_s = row.get(f"{prefix}_yes_ask", "")
                if not bid_s or not ask_s:
                    continue
                book = OrderBook(prefix)
                book.set_from_top(
                    bid=bid_s,
                    ask=ask_s,
                    bid_qty=row.get(f"{prefix}_yes_bid_qty", "0") or "0",
                    ask_qty=row.get(f"{prefix}_yes_ask_qty", "0") or "0",
                    updated_ms=ts_ms,
                )
                result = detectors[prefix].evaluate(prefix, book)
                if isinstance(result, GoalSignal):
                    episodes.append((ts_ms, row["ts_iso"], prefix))
        
        for ep_ts_ms, ep_ts_iso, ep_ticker in episodes:
            for prefix in prefixes:
                first_bid, first_ask = _find_first_jumps(ticker_rows[prefix], ep_ts_ms)
                
                bid_lag = (first_bid[0] - ep_ts_ms) if first_bid else None
                ask_lag = (first_ask[0] - ep_ts_ms) if first_ask else None
                
                entries.append(LeadLagEntry(
                    episode_ts_iso=ep_ts_iso,
                    episode_ticker=ep_ticker,
                    tracked_ticker=prefix,
                    ticker_type=_ticker_type(prefix),
                    first_bid_jump_10c_ts_ms=first_bid[0] if first_bid else None,
                    first_bid_jump_10c_ts_iso=first_bid[1] if first_bid else "",
                    first_ask_jump_3c_ts_ms=first_ask[0] if first_ask else None,
                    first_ask_jump_3c_ts_iso=first_ask[1] if first_ask else "",
                    bid_jump_lag_ms=bid_lag,
                    ask_jump_lag_ms=ask_lag,
                ))
    
    lines = [
        f"# Lead/Lag Analysis: {session_dir.name}",
        "",
        "For each goal episode, this shows the first timestamp where each tracked ticker's",
        "bid jumped ≥10¢ or ask jumped ≥3¢, relative to the episode trigger.",
        "",
    ]
    
    ep_groups: dict[str, list[LeadLagEntry]] = {}
    for e in entries:
        ep_groups.setdefault(e.episode_ts_iso, []).append(e)
    
    for ep_ts, group in sorted(ep_groups.items()):
        first_entry = group[0]
        lines.append(f"## Episode: {ep_ts[:19]} ({_short(first_entry.episode_ticker)})")
        lines.append("")
        lines.append("| Ticker | Type | Bid ≥10¢ jump | Lag (ms) | Ask ≥3¢ jump | Lag (ms) |")
        lines.append("|--------|------|---------------|----------|--------------|----------|")
        
        group_sorted = sorted(group, key=lambda e: (e.bid_jump_lag_ms or 999999, e.ask_jump_lag_ms or 999999))
        
        for e in group_sorted:
            bid_ts = e.first_bid_jump_10c_ts_iso[11:23] if e.first_bid_jump_10c_ts_iso else "—"
            ask_ts = e.first_ask_jump_3c_ts_iso[11:23] if e.first_ask_jump_3c_ts_iso else "—"
            bid_lag = f"{e.bid_jump_lag_ms:+d}" if e.bid_jump_lag_ms is not None else "—"
            ask_lag = f"{e.ask_jump_lag_ms:+d}" if e.ask_jump_lag_ms is not None else "—"
            
            lines.append(
                f"| {_short(e.tracked_ticker)} | {e.ticker_type} | {bid_ts} | {bid_lag} | {ask_ts} | {ask_lag} |"
            )
        
        lines.append("")
    
    if episodes:
        lines.append("## Summary")
        lines.append("")
        
        bid_leaders: dict[str, int] = {}
        ask_leaders: dict[str, int] = {}
        
        for ep_ts, group in ep_groups.items():
            bid_entries = [e for e in group if e.bid_jump_lag_ms is not None]
            ask_entries = [e for e in group if e.ask_jump_lag_ms is not None]
            
            if bid_entries:
                leader = min(bid_entries, key=lambda e: e.bid_jump_lag_ms)
                bid_leaders[leader.ticker_type] = bid_leaders.get(leader.ticker_type, 0) + 1
            
            if ask_entries:
                leader = min(ask_entries, key=lambda e: e.ask_jump_lag_ms)
                ask_leaders[leader.ticker_type] = ask_leaders.get(leader.ticker_type, 0) + 1
        
        lines.append("### Bid jump leaders (first ≥10¢ move)")
        lines.append("")
        for ticker_type, count in sorted(bid_leaders.items(), key=lambda x: -x[1]):
            lines.append(f"- **{ticker_type}**: {count} episode(s)")
        lines.append("")
        
        lines.append("### Ask jump leaders (first ≥3¢ move)")
        lines.append("")
        for ticker_type, count in sorted(ask_leaders.items(), key=lambda x: -x[1]):
            lines.append(f"- **{ticker_type}**: {count} episode(s)")
        lines.append("")
    
    report = "\n".join(lines)
    return entries, report


def run_lead_lag(session_dir: Path) -> Path:
    """Run lead/lag analysis and save results."""
    entries, report = analyze_lead_lag(session_dir)
    
    csv_path = session_dir / "lead_lag.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "episode_ts_iso", "episode_ticker", "tracked_ticker", "ticker_type",
            "first_bid_jump_10c_ts_ms", "first_bid_jump_10c_ts_iso",
            "first_ask_jump_3c_ts_ms", "first_ask_jump_3c_ts_iso",
            "bid_jump_lag_ms", "ask_jump_lag_ms"
        ])
        for e in entries:
            writer.writerow([
                e.episode_ts_iso, e.episode_ticker, e.tracked_ticker, e.ticker_type,
                e.first_bid_jump_10c_ts_ms or "", e.first_bid_jump_10c_ts_iso,
                e.first_ask_jump_3c_ts_ms or "", e.first_ask_jump_3c_ts_iso,
                e.bid_jump_lag_ms if e.bid_jump_lag_ms is not None else "",
                e.ask_jump_lag_ms if e.ask_jump_lag_ms is not None else ""
            ])
    
    md_path = session_dir / "lead_lag.md"
    md_path.write_text(report, encoding="utf-8")
    
    return md_path


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python -m suspension_lab.lead_lag <session_folder>")
        raise SystemExit(1)
    
    folder = Path(sys.argv[1]).resolve()
    _, report = analyze_lead_lag(folder)
    print(report)
    path = run_lead_lag(folder)
    print(f"\nSaved: {path}")
