"""Fill verifier: estimate whether orders would have filled on goal signals."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from suspension_lab.goal_signal import GoalSignal, GoalSignalDetector
from suspension_lab.orderbook import OrderBook


@dataclass
class FillVerdict:
    ts_iso: str
    ticker: str
    signal_bid_cents: int
    exit_mode: str
    size: int
    strategy: str
    verdict: str
    reason: str
    best_fill_cents: int | None = None
    queue_consumed: float = 0.0


def _short(ticker: str) -> str:
    parts = ticker.split("-")
    return "-".join(parts[-2:]) if len(parts) >= 2 else ticker


def _ticker_prefixes(headers: list[str]) -> list[str]:
    return [h[: -len("_yes_bid")] for h in headers if h.endswith("_yes_bid")]


def _verify_fill_wide(
    rows: list[dict],
    signal_idx: int,
    prefix: str,
    signal_bid_cents: int,
    size: int,
    strategy: str,
    window_ms: int = 5000,
) -> FillVerdict:
    """Check fill possibility from wide-format rows."""
    signal_row = rows[signal_idx]
    ts_iso = signal_row["ts_iso"]
    ts_ms = int(signal_row["ts_ms"])
    initial_qty = float(signal_row.get(f"{prefix}_yes_bid_qty", 0) or 0)
    
    best_fill_cents: int | None = None
    queue_consumed = 0.0
    
    if strategy == "join_bid":
        target_cents = signal_bid_cents
    elif strategy == "bid_plus_1":
        target_cents = signal_bid_cents + 1
    else:
        target_cents = signal_bid_cents + 1
    
    for later in rows[signal_idx + 1 : signal_idx + 100]:
        later_ts = int(later["ts_ms"])
        if later_ts > ts_ms + window_ms:
            break
        
        bid_s = later.get(f"{prefix}_yes_bid", "")
        ask_s = later.get(f"{prefix}_yes_ask", "")
        if not bid_s:
            continue
        
        bid_cents = int(round(Decimal(bid_s) * 100))
        
        if strategy == "lift_ask" and ask_s:
            ask_cents = int(round(Decimal(ask_s) * 100))
            best_fill_cents = ask_cents
            return FillVerdict(
                ts_iso=ts_iso,
                ticker=prefix,
                signal_bid_cents=signal_bid_cents,
                exit_mode="",
                size=size,
                strategy=strategy,
                verdict="FILL",
                reason=f"lifted ask @ {ask_cents}c",
                best_fill_cents=ask_cents,
            )
        
        if bid_cents > target_cents:
            best_fill_cents = bid_cents
            return FillVerdict(
                ts_iso=ts_iso,
                ticker=prefix,
                signal_bid_cents=signal_bid_cents,
                exit_mode="",
                size=size,
                strategy=strategy,
                verdict="FILL",
                reason=f"bid lifted past {target_cents}c to {bid_cents}c",
                best_fill_cents=target_cents if strategy != "lift_ask" else bid_cents,
            )
        
        if bid_cents == target_cents:
            qty = float(later.get(f"{prefix}_yes_bid_qty", 0) or 0)
            consumed = initial_qty - qty
            if consumed > 0:
                queue_consumed = max(queue_consumed, consumed)
                if consumed >= size * 0.5:
                    return FillVerdict(
                        ts_iso=ts_iso,
                        ticker=prefix,
                        signal_bid_cents=signal_bid_cents,
                        exit_mode="",
                        size=size,
                        strategy=strategy,
                        verdict="PARTIAL" if consumed < size else "FILL",
                        reason=f"queue consumed {consumed:.0f} contracts",
                        best_fill_cents=target_cents,
                        queue_consumed=consumed,
                    )
    
    if initial_qty >= size * 3:
        verdict = "NO_FILL"
        reason = f"deep queue ({initial_qty:.0f}ct ahead), no lift"
    elif initial_qty >= size:
        verdict = "PARTIAL"
        reason = f"queue exists ({initial_qty:.0f}ct), partial possible"
    else:
        verdict = "PARTIAL"
        reason = f"thin queue ({initial_qty:.0f}ct), likely partial"
    
    return FillVerdict(
        ts_iso=ts_iso,
        ticker=prefix,
        signal_bid_cents=signal_bid_cents,
        exit_mode="",
        size=size,
        strategy=strategy,
        verdict=verdict,
        reason=reason,
        best_fill_cents=None,
        queue_consumed=queue_consumed,
    )


def _verify_fill_long(
    ticker_rows: list[tuple[int, dict]],
    signal_idx: int,
    ticker: str,
    signal_bid_cents: int,
    size: int,
    strategy: str,
    window_ms: int = 5000,
) -> FillVerdict:
    """Check fill possibility from long-format rows for a single ticker."""
    ts_ms, signal_row = ticker_rows[signal_idx]
    ts_iso = signal_row["ts_iso"]
    initial_qty = float(signal_row.get("yes_bid_qty", 0) or 0)
    
    best_fill_cents: int | None = None
    queue_consumed = 0.0
    
    if strategy == "join_bid":
        target_cents = signal_bid_cents
    elif strategy == "bid_plus_1":
        target_cents = signal_bid_cents + 1
    else:
        target_cents = signal_bid_cents + 1
    
    for later_ts, later in ticker_rows[signal_idx + 1 :]:
        if later_ts > ts_ms + window_ms:
            break
        
        bid_s = later.get("yes_bid", "")
        ask_s = later.get("yes_ask", "")
        if not bid_s:
            continue
        
        bid_cents = int(round(Decimal(bid_s) * 100))
        
        if strategy == "lift_ask" and ask_s:
            ask_cents = int(round(Decimal(ask_s) * 100))
            return FillVerdict(
                ts_iso=ts_iso,
                ticker=ticker,
                signal_bid_cents=signal_bid_cents,
                exit_mode="",
                size=size,
                strategy=strategy,
                verdict="FILL",
                reason=f"lifted ask @ {ask_cents}c",
                best_fill_cents=ask_cents,
            )
        
        if bid_cents > target_cents:
            return FillVerdict(
                ts_iso=ts_iso,
                ticker=ticker,
                signal_bid_cents=signal_bid_cents,
                exit_mode="",
                size=size,
                strategy=strategy,
                verdict="FILL",
                reason=f"bid lifted past {target_cents}c to {bid_cents}c",
                best_fill_cents=target_cents if strategy != "lift_ask" else bid_cents,
            )
        
        if bid_cents == target_cents:
            qty = float(later.get("yes_bid_qty", 0) or 0)
            consumed = initial_qty - qty
            if consumed > 0:
                queue_consumed = max(queue_consumed, consumed)
                if consumed >= size * 0.5:
                    return FillVerdict(
                        ts_iso=ts_iso,
                        ticker=ticker,
                        signal_bid_cents=signal_bid_cents,
                        exit_mode="",
                        size=size,
                        strategy=strategy,
                        verdict="PARTIAL" if consumed < size else "FILL",
                        reason=f"queue consumed {consumed:.0f} contracts",
                        best_fill_cents=target_cents,
                        queue_consumed=consumed,
                    )
    
    if initial_qty >= size * 3:
        verdict = "NO_FILL"
        reason = f"deep queue ({initial_qty:.0f}ct ahead), no lift"
    elif initial_qty >= size:
        verdict = "PARTIAL"
        reason = f"queue exists ({initial_qty:.0f}ct), partial possible"
    else:
        verdict = "PARTIAL"
        reason = f"thin queue ({initial_qty:.0f}ct), likely partial"
    
    return FillVerdict(
        ts_iso=ts_iso,
        ticker=ticker,
        signal_bid_cents=signal_bid_cents,
        exit_mode="",
        size=size,
        strategy=strategy,
        verdict=verdict,
        reason=reason,
        best_fill_cents=None,
        queue_consumed=queue_consumed,
    )


def verify_fills(session_dir: Path, *, size: int = 50) -> tuple[list[FillVerdict], str]:
    """Verify fills for all goal signals in a session.
    
    Returns (verdicts, markdown_report).
    """
    long_path = session_dir / "books_long.csv"
    use_long = long_path.exists()
    
    verdicts: list[FillVerdict] = []
    
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
        
        signal_locs: list[tuple[str, int, GoalSignal]] = []
        
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
                idx = next(
                    i for i, (t, r) in enumerate(ticker_rows[ticker]) if t == ts_ms
                )
                signal_locs.append((ticker, idx, result))
        
        for ticker, idx, signal in signal_locs:
            signal_cents = int(round(signal.new_bid * 100))
            for strategy in ("join_bid", "bid_plus_1", "lift_ask"):
                v = _verify_fill_long(
                    ticker_rows[ticker],
                    idx,
                    ticker,
                    signal_cents,
                    size,
                    strategy,
                )
                v.exit_mode = signal.exit_mode
                verdicts.append(v)
    else:
        books_path = session_dir / "books.csv"
        with books_path.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            prefixes = _ticker_prefixes(headers)
            rows = list(reader)
        
        detectors = {p: GoalSignalDetector() for p in prefixes}
        signal_locs: list[tuple[str, int, GoalSignal]] = []
        
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
                    signal_locs.append((prefix, i, result))
        
        for prefix, idx, signal in signal_locs:
            signal_cents = int(round(signal.new_bid * 100))
            for strategy in ("join_bid", "bid_plus_1", "lift_ask"):
                v = _verify_fill_wide(rows, idx, prefix, signal_cents, size, strategy)
                v.exit_mode = signal.exit_mode
                verdicts.append(v)
    
    lines = [
        f"# Fill verification: {session_dir.name}",
        "",
        f"Target size: **{size} contracts**",
        "",
        "Queue risk: ~500 MM top qty typical on Kalshi soccer; this analysis checks whether",
        "price lifts or queue consumes enough to suggest fill.",
        "",
        "| Time | Ticker | Signal | Mode | Strategy | Verdict | Reason |",
        "|------|--------|--------|------|----------|---------|--------|",
    ]
    
    for v in verdicts:
        emoji = {"FILL": "✅", "PARTIAL": "🟡", "NO_FILL": "❌"}.get(v.verdict, "")
        lines.append(
            f"| {v.ts_iso[11:19]} | {_short(v.ticker)} | {v.signal_bid_cents}c | "
            f"`{v.exit_mode}` | {v.strategy} | {emoji} {v.verdict} | {v.reason} |"
        )
    
    lines.extend([
        "",
        "## Summary",
        "",
    ])
    
    by_signal: dict[tuple[str, str], list[FillVerdict]] = {}
    for v in verdicts:
        key = (v.ts_iso, v.ticker)
        by_signal.setdefault(key, []).append(v)
    
    fill_count = sum(1 for vlist in by_signal.values() if any(v.verdict == "FILL" for v in vlist))
    partial_count = sum(
        1 for vlist in by_signal.values()
        if not any(v.verdict == "FILL" for v in vlist) and any(v.verdict == "PARTIAL" for v in vlist)
    )
    no_fill_count = len(by_signal) - fill_count - partial_count
    
    lines.extend([
        f"- **{len(by_signal)}** goal signals analyzed",
        f"- **{fill_count}** would have filled (at least one strategy)",
        f"- **{partial_count}** partial fill likely",
        f"- **{no_fill_count}** unlikely to fill at join-bid",
        "",
        "### P&L implications",
        "",
        "- Backtest P&L should only count FILL or conservative PARTIAL",
        "- NO_FILL signals should be excluded from realized P&L",
        "",
    ])
    
    report = "\n".join(lines)
    return verdicts, report


def run_verify_fills(session_dir: Path, *, size: int = 50) -> Path:
    """Run fill verification and save results."""
    verdicts, report = verify_fills(session_dir, size=size)
    
    csv_path = session_dir / "fill_would_have.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "ts_iso", "ticker", "signal_bid_cents", "exit_mode", "size",
            "strategy", "verdict", "reason", "best_fill_cents", "queue_consumed"
        ])
        for v in verdicts:
            writer.writerow([
                v.ts_iso, v.ticker, v.signal_bid_cents, v.exit_mode, v.size,
                v.strategy, v.verdict, v.reason, v.best_fill_cents or "", v.queue_consumed
            ])
    
    md_path = session_dir / "fill_would_have.md"
    md_path.write_text(report, encoding="utf-8")
    
    return md_path


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python -m suspension_lab.fill_verifier <session_folder> [size]")
        raise SystemExit(1)
    
    folder = Path(sys.argv[1]).resolve()
    sz = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    _, report = verify_fills(folder, size=sz)
    print(report)
    path = run_verify_fills(folder, size=sz)
    print(f"\nSaved: {path}")
