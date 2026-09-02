"""Post-session or rolling digest: signals, spoof vs VAR, fill-would-have P&L.

Produces a compact summary of:
- Goal signals detected
- Spoof bids vs true VAR events
- Fill verification (FILL/PARTIAL only P&L)
- Per-line exit performance (never scalp bonded O0.5)
- Whether paper edge looks real

Can be run:
- Post-session: python -m suspension_lab.analyze_digest <session_folder>
- Rolling (live): called from UI during session
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any

from suspension_lab.exit_engine import is_total_05_ticker, scalp_target_cents
from suspension_lab.fill_verifier import FillVerdict, verify_fills
from suspension_lab.goal_signal import GoalSignal, GoalSignalDetector, SpoofBidNotice, VarRevertAlert
from suspension_lab.lead_lag import analyze_lead_lag
from suspension_lab.orderbook import OrderBook


@dataclass
class SignalSummary:
    """Summary of a single goal signal and its outcome."""

    ts_iso: str
    ticker: str
    ticker_type: str
    entry_cents: int
    exit_mode: str
    exit_cents: int | None = None
    exit_reason: str = ""
    pnl_cents: int = 0
    fill_verdict: str = ""
    fill_strategy: str = ""
    was_spoof: bool = False
    was_var: bool = False


@dataclass
class DigestResult:
    """Full session analysis digest."""

    session_name: str
    session_dir: Path
    game_label: str = ""
    tickers_tracked: list[str] = field(default_factory=list)
    duration_minutes: float = 0.0

    total_signals: int = 0
    signals: list[SignalSummary] = field(default_factory=list)

    spoof_count: int = 0
    var_count: int = 0

    fill_count: int = 0
    partial_count: int = 0
    no_fill_count: int = 0

    gross_pnl_cents: int = 0
    adjusted_pnl_cents: int = 0

    per_line_summary: dict[str, dict[str, Any]] = field(default_factory=dict)

    lead_lag_leader: str = ""

    conclusions: list[str] = field(default_factory=list)

    def edge_looks_real(self) -> bool:
        if self.fill_count + self.partial_count == 0:
            return False
        if self.adjusted_pnl_cents <= 0:
            return False
        hit_rate = self.fill_count / max(self.total_signals, 1)
        return hit_rate >= 0.3 and self.adjusted_pnl_cents > 0


def _ticker_type(ticker: str) -> str:
    """Classify ticker as ML, O0.5, O1.5, etc."""
    ticker_upper = ticker.upper()
    if "GAME" in ticker_upper:
        return "ML"
    if "TOTAL" in ticker_upper:
        import re

        match = re.search(r"-(\d+)$", ticker)
        if match:
            strike = int(match.group(1))
            if strike == 1:
                return "O0.5"
            elif strike == 2:
                return "O1.5"
            else:
                goals = (strike - 1) * 0.5
                return f"O{goals:.1f}"
    return "other"


def _short(ticker: str) -> str:
    parts = ticker.split("-")
    return "-".join(parts[-2:]) if len(parts) >= 2 else ticker


def _load_paper_trades(session_dir: Path) -> list[dict]:
    """Load paper trades from CSV."""
    path = session_dir / "paper_trades.csv"
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _load_goal_signals(session_dir: Path) -> list[dict]:
    """Load goal signals from CSV."""
    path = session_dir / "goal_signals.csv"
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _load_session_meta(session_dir: Path) -> dict:
    """Load session metadata."""
    path = session_dir / "session.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _detect_spoofs_and_vars(session_dir: Path) -> tuple[int, int, list[tuple[str, str, str]]]:
    """Detect spoof bids and VAR events from book tape.

    Returns (spoof_count, var_count, event_list).
    Event list: [(ts_iso, ticker, "spoof"|"var")]
    """
    long_path = session_dir / "books_long.csv"
    if not long_path.exists():
        return 0, 0, []

    with long_path.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    tickers = sorted({r["ticker"] for r in rows if r.get("ticker")})
    detectors = {t: GoalSignalDetector() for t in tickers}

    spoofs: list[tuple[str, str]] = []
    vars_: list[tuple[str, str]] = []

    for row in rows:
        ticker = row.get("ticker", "")
        if not ticker or ticker not in tickers:
            continue
        bid_s = row.get("yes_bid", "")
        ask_s = row.get("yes_ask", "")
        if not bid_s:
            continue
        ts_ms = int(row["ts_ms"])
        book = OrderBook(ticker)
        book.set_from_top(
            bid=bid_s,
            ask=ask_s or "",
            bid_qty=row.get("yes_bid_qty", "0") or "0",
            ask_qty=row.get("yes_ask_qty", "0") or "0",
            updated_ms=ts_ms,
        )
        result = detectors[ticker].evaluate(ticker, book)
        if isinstance(result, SpoofBidNotice):
            spoofs.append((row["ts_iso"], ticker))
        elif isinstance(result, VarRevertAlert) and not result.is_spoof:
            vars_.append((row["ts_iso"], ticker))

    events = [(ts, t, "spoof") for ts, t in spoofs] + [(ts, t, "var") for ts, t in vars_]
    events.sort(key=lambda x: x[0])
    return len(spoofs), len(vars_), events


def analyze_session(session_dir: Path, *, size: int = 50) -> DigestResult:
    """Analyze a session and produce a digest.

    Args:
        session_dir: Path to session folder
        size: Position size for fill verification

    Returns:
        DigestResult with full analysis
    """
    meta = _load_session_meta(session_dir)
    goal_signals = _load_goal_signals(session_dir)
    paper_trades = _load_paper_trades(session_dir)

    result = DigestResult(
        session_name=session_dir.name,
        session_dir=session_dir,
        game_label=meta.get("game_label", ""),
        tickers_tracked=meta.get("tickers", []),
    )

    started = meta.get("started_at")
    ended = meta.get("ended_at")
    if started and ended:
        try:
            start_dt = datetime.fromisoformat(started.replace("Z", "+00:00"))
            end_dt = datetime.fromisoformat(ended.replace("Z", "+00:00"))
            result.duration_minutes = (end_dt - start_dt).total_seconds() / 60
        except (ValueError, TypeError):
            pass

    result.total_signals = len(goal_signals)

    spoof_count, var_count, events = _detect_spoofs_and_vars(session_dir)
    result.spoof_count = spoof_count
    result.var_count = var_count

    verdicts, _ = verify_fills(session_dir, size=size)
    verdict_map: dict[tuple[str, str], list[FillVerdict]] = {}
    for v in verdicts:
        key = (v.ts_iso, v.ticker)
        verdict_map.setdefault(key, []).append(v)

    for v in verdicts:
        if v.verdict == "FILL":
            result.fill_count += 1
        elif v.verdict == "PARTIAL":
            result.partial_count += 1
        else:
            result.no_fill_count += 1

    result.fill_count //= 3
    result.partial_count //= 3
    result.no_fill_count //= 3

    trade_by_ticker: dict[str, dict] = {}
    for trade in paper_trades:
        ticker = trade.get("ticker", "")
        if ticker and trade.get("status") == "closed":
            if ticker not in trade_by_ticker:
                trade_by_ticker[ticker] = trade

    for sig in goal_signals:
        ts_iso = sig.get("signal_ts_iso", "")
        ticker = sig.get("ticker", "")
        entry_cents = int(sig.get("new_bid", "0").replace(".", "").lstrip("0") or "0")
        if "." in sig.get("new_bid", ""):
            entry_cents = int(round(float(sig.get("new_bid", "0")) * 100))
        exit_mode = sig.get("exit_mode", "")

        ticker_type = _ticker_type(ticker)

        exit_cents = None
        exit_reason = ""
        pnl = 0

        if ticker in trade_by_ticker:
            trade = trade_by_ticker[ticker]
            try:
                exit_cents = int(trade.get("exit_cents", "") or 0)
                entry_paper = int(trade.get("entry_cents", "") or entry_cents)
                pnl = exit_cents - entry_paper
            except ValueError:
                pass
            exit_reason = trade.get("exit_reason", "")

        vs = verdict_map.get((ts_iso, ticker), [])
        fill_verdict = ""
        fill_strategy = ""
        if vs:
            best = next((v for v in vs if v.verdict == "FILL"), None)
            if not best:
                best = next((v for v in vs if v.verdict == "PARTIAL"), None)
            if not best:
                best = vs[0]
            fill_verdict = best.verdict
            fill_strategy = best.strategy

        was_spoof = any(e[0] == ts_iso and e[1] == ticker and e[2] == "spoof" for e in events)
        was_var = any(e[0] == ts_iso and e[1] == ticker and e[2] == "var" for e in events)

        summary = SignalSummary(
            ts_iso=ts_iso,
            ticker=ticker,
            ticker_type=ticker_type,
            entry_cents=entry_cents,
            exit_mode=exit_mode,
            exit_cents=exit_cents,
            exit_reason=exit_reason,
            pnl_cents=pnl,
            fill_verdict=fill_verdict,
            fill_strategy=fill_strategy,
            was_spoof=was_spoof,
            was_var=was_var,
        )
        result.signals.append(summary)

    for sig in result.signals:
        result.gross_pnl_cents += sig.pnl_cents
        if sig.fill_verdict in ("FILL", "PARTIAL"):
            result.adjusted_pnl_cents += sig.pnl_cents

    for sig in result.signals:
        ttype = sig.ticker_type
        if ttype not in result.per_line_summary:
            result.per_line_summary[ttype] = {
                "count": 0,
                "total_pnl": 0,
                "fills": 0,
                "partials": 0,
                "no_fills": 0,
            }
        stats = result.per_line_summary[ttype]
        stats["count"] += 1
        stats["total_pnl"] += sig.pnl_cents
        if sig.fill_verdict == "FILL":
            stats["fills"] += 1
        elif sig.fill_verdict == "PARTIAL":
            stats["partials"] += 1
        else:
            stats["no_fills"] += 1

    try:
        lead_entries, _ = analyze_lead_lag(session_dir)
        if lead_entries:
            bid_leaders: dict[str, int] = {}
            for e in lead_entries:
                if e.bid_jump_lag_ms == 0 or (
                    e.bid_jump_lag_ms is not None and e.bid_jump_lag_ms < 500
                ):
                    bid_leaders[e.ticker_type] = bid_leaders.get(e.ticker_type, 0) + 1
            if bid_leaders:
                result.lead_lag_leader = max(bid_leaders, key=bid_leaders.get)
    except Exception:
        pass

    if result.total_signals == 0:
        result.conclusions.append("No goal signals detected — game may have been scoreless or lab ran briefly.")
    else:
        if result.spoof_count > result.var_count:
            result.conclusions.append(
                f"More spoof bids ({result.spoof_count}) than true VAR events ({result.var_count}). "
                "Spoof filter is working — do not exit on lowball bids."
            )
        elif result.var_count > 0:
            result.conclusions.append(
                f"VAR events detected: {result.var_count}. VAR protection is critical on this game."
            )

        if result.fill_count > 0 and result.adjusted_pnl_cents > 0:
            result.conclusions.append(
                f"Adjusted P&L (FILL/PARTIAL only): +{result.adjusted_pnl_cents}¢ — edge looks real."
            )
        elif result.adjusted_pnl_cents <= 0 and result.fill_count > 0:
            result.conclusions.append(
                f"Adjusted P&L: {result.adjusted_pnl_cents}¢ — no edge detected on filled signals."
            )

        o05_stats = result.per_line_summary.get("O0.5", {})
        if o05_stats.get("count", 0) > 0:
            if o05_stats.get("total_pnl", 0) > 0:
                result.conclusions.append(
                    f"O0.5 performance: {o05_stats['count']} signals, +{o05_stats['total_pnl']}¢. "
                    "Hold-bond strategy working."
                )

    return result


def format_digest(result: DigestResult) -> str:
    """Format digest as markdown."""
    lines = [
        f"# Session Digest: {result.session_name}",
        "",
        f"**Game:** {result.game_label or '(unnamed)'}",
        f"**Duration:** {result.duration_minutes:.1f} minutes",
        f"**Tickers:** {len(result.tickers_tracked)}",
        "",
        "---",
        "",
        "## Signal Summary",
        "",
        f"- **Total signals:** {result.total_signals}",
        f"- **Spoof bids:** {result.spoof_count}",
        f"- **VAR events:** {result.var_count}",
        "",
        "## Fill Verification",
        "",
        f"- **Would fill:** {result.fill_count}",
        f"- **Partial fill:** {result.partial_count}",
        f"- **No fill:** {result.no_fill_count}",
        "",
        "## P&L",
        "",
        f"- **Gross P&L:** {result.gross_pnl_cents:+d}¢ (all paper trades)",
        f"- **Adjusted P&L:** {result.adjusted_pnl_cents:+d}¢ (FILL/PARTIAL only)",
        "",
    ]

    if result.signals:
        lines.extend(
            [
                "## Signal Details",
                "",
                "| Time | Ticker | Type | Entry | Exit | P&L | Fill | Spoof? | VAR? |",
                "|------|--------|------|-------|------|-----|------|--------|------|",
            ]
        )
        for sig in result.signals:
            exit_str = f"{sig.exit_cents}¢" if sig.exit_cents else "—"
            pnl_str = f"{sig.pnl_cents:+d}¢" if sig.exit_cents else "—"
            spoof_str = "⚠️" if sig.was_spoof else ""
            var_str = "🔴" if sig.was_var else ""
            fill_emoji = {"FILL": "✅", "PARTIAL": "🟡", "NO_FILL": "❌"}.get(sig.fill_verdict, "")
            lines.append(
                f"| {sig.ts_iso[11:19]} | {_short(sig.ticker)} | {sig.ticker_type} | "
                f"{sig.entry_cents}¢ | {exit_str} | {pnl_str} | {fill_emoji} | {spoof_str} | {var_str} |"
            )
        lines.append("")

    if result.per_line_summary:
        lines.extend(
            [
                "## Per-Line Performance",
                "",
                "| Type | Signals | P&L | Fills | Partials | No Fill |",
                "|------|---------|-----|-------|----------|---------|",
            ]
        )
        for ttype, stats in sorted(result.per_line_summary.items()):
            lines.append(
                f"| {ttype} | {stats['count']} | {stats['total_pnl']:+d}¢ | "
                f"{stats['fills']} | {stats['partials']} | {stats['no_fills']} |"
            )
        lines.append("")

    if result.lead_lag_leader:
        lines.extend(
            [
                "## Lead/Lag",
                "",
                f"Most frequent lead ticker type: **{result.lead_lag_leader}**",
                "",
            ]
        )

    lines.extend(
        [
            "## Conclusions",
            "",
        ]
    )
    for c in result.conclusions:
        lines.append(f"- {c}")
    lines.append("")

    edge_str = "✅ Yes" if result.edge_looks_real() else "❌ No"
    lines.extend(
        [
            "---",
            "",
            f"**Edge looks real:** {edge_str}",
            "",
        ]
    )

    return "\n".join(lines)


def run_digest(session_dir: Path, *, size: int = 50) -> Path:
    """Run full digest analysis and save results."""
    result = analyze_session(session_dir, size=size)
    report = format_digest(result)

    md_path = session_dir / "analysis.md"
    md_path.write_text(report, encoding="utf-8")

    return md_path


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m suspension_lab.analyze_digest <session_folder> [size]")
        raise SystemExit(1)

    folder = Path(sys.argv[1]).resolve()
    sz = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    result = analyze_session(folder, size=sz)
    report = format_digest(result)
    print(report)
    path = run_digest(folder, size=sz)
    print(f"\nSaved: {path}")
