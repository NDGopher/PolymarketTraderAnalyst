"""Backtest exit strategies on goal-signal entries from a saved session."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path

from suspension_lab.goal_signal import GoalSignal, GoalSignalDetector
from suspension_lab.orderbook import OrderBook


def _ticker_prefixes(headers: list[str]) -> list[str]:
    return [h[: -len("_yes_bid")] for h in headers if h.endswith("_yes_bid")]


def _short_ticker(prefix: str) -> str:
    parts = prefix.split("-")
    return "-".join(parts[-2:]) if len(parts) >= 2 else prefix


@dataclass
class TapePoint:
    ts_ms: int
    bid_cents: int
    ask_cents: int


@dataclass
class TradeEntry:
    ts_ms: int
    ts_iso: str
    ticker: str
    entry_cents: int
    exit_mode: str
    bid_jump_cents: int


@dataclass
class TradeResult:
    entry: TradeEntry
    strategy: str
    exit_cents: int
    exit_at_sec: float
    exit_reason: str
    pnl_cents: int
    markouts: dict[int, int] = field(default_factory=dict)

    @property
    def pnl_dollars(self) -> float:
        return self.pnl_cents / 100.0


def _load_tape(session_dir: Path) -> tuple[dict[str, list[TapePoint]], list[TradeEntry]]:
    books_path = session_dir / "books.csv"
    with books_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        prefixes = _ticker_prefixes(headers)
        rows = list(reader)

    tape: dict[str, list[TapePoint]] = {p: [] for p in prefixes}
    for row in rows:
        ts_ms = int(row["ts_ms"])
        for prefix in prefixes:
            bid_s = row.get(f"{prefix}_yes_bid", "")
            ask_s = row.get(f"{prefix}_yes_ask", "")
            if not bid_s or not ask_s:
                continue
            tape[prefix].append(
                TapePoint(
                    ts_ms=ts_ms,
                    bid_cents=int(round(Decimal(bid_s) * 100)),
                    ask_cents=int(round(Decimal(ask_s) * 100)),
                )
            )

    detectors: dict[str, GoalSignalDetector] = {p: GoalSignalDetector() for p in prefixes}
    entries: list[TradeEntry] = []
    for row in rows:
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
                entries.append(
                    TradeEntry(
                        ts_ms=ts_ms,
                        ts_iso=row["ts_iso"],
                        ticker=prefix,
                        entry_cents=int(round(result.new_bid * 100)),
                        exit_mode=result.exit_mode,
                        bid_jump_cents=result.bid_jump_cents,
                    )
                )
    return tape, entries


def _bid_at_offset(tape: list[TapePoint], entry_ms: int, offset_sec: float) -> int | None:
    target = entry_ms + int(offset_sec * 1000)
    best: TapePoint | None = None
    for pt in tape:
        if pt.ts_ms >= target:
            best = pt
            break
    return best.bid_cents if best else None


def _bid_series(
    tape: list[TapePoint], entry_ms: int, until_sec: float
) -> list[tuple[float, int]]:
    end = entry_ms + int(until_sec * 1000)
    out: list[tuple[float, int]] = []
    for pt in tape:
        if pt.ts_ms < entry_ms:
            continue
        if pt.ts_ms > end:
            break
        out.append(((pt.ts_ms - entry_ms) / 1000.0, pt.bid_cents))
    return out


def _simulate_limit_scalp(entry: TradeEntry, tape: list[TapePoint], target_plus: int = 7) -> TradeResult:
    """Limit sell at entry + target_plus cents; else exit at bid after 45s."""
    target = entry.entry_cents + target_plus
    series = _bid_series(tape, entry.ts_ms, 45.0)
    markouts = {}
    for sec in (5, 10, 15, 20, 25, 30, 35, 45):
        b = _bid_at_offset(tape, entry.ts_ms, sec)
        if b is not None:
            markouts[sec] = b

    for elapsed, bid in series:
        if bid >= target:
            return TradeResult(
                entry=entry,
                strategy=f"limit_+{target_plus}c",
                exit_cents=target,
                exit_at_sec=elapsed,
                exit_reason=f"limit fill @ {target}c",
                pnl_cents=target_plus,
                markouts=markouts,
            )
    final = series[-1][1] if series else entry.entry_cents
    return TradeResult(
        entry=entry,
        strategy=f"limit_+{target_plus}c",
        exit_cents=final,
        exit_at_sec=45.0,
        exit_reason="time stop 45s",
        pnl_cents=final - entry.entry_cents,
        markouts=markouts,
    )


def _simulate_hold_bond(entry: TradeEntry, tape: list[TapePoint]) -> TradeResult:
    """Hold until bid >= 95c or 120s."""
    series = _bid_series(tape, entry.ts_ms, 120.0)
    markouts = {}
    for sec in (5, 10, 15, 20, 25, 30, 35, 45, 60, 90, 120):
        b = _bid_at_offset(tape, entry.ts_ms, sec)
        if b is not None:
            markouts[sec] = b

    peak = entry.entry_cents
    for elapsed, bid in series:
        peak = max(peak, bid)
        if bid >= 95:
            return TradeResult(
                entry=entry,
                strategy="hold_bond",
                exit_cents=bid,
                exit_at_sec=elapsed,
                exit_reason=f"bond @ {bid}c",
                pnl_cents=bid - entry.entry_cents,
                markouts=markouts,
            )
    final = series[-1][1] if series else entry.entry_cents
    return TradeResult(
        entry=entry,
        strategy="hold_bond",
        exit_cents=final,
        exit_at_sec=120.0,
        exit_reason="held 120s",
        pnl_cents=final - entry.entry_cents,
        markouts=markouts,
    )


def _simulate_time_collar(
    entry: TradeEntry,
    tape: list[TapePoint],
    *,
    stall_sec: float = 20.0,
    scalp_plus: int = 7,
    bond_cents: int = 95,
    progress_min_cents: int = 3,
) -> TradeResult:
    """
    Move-or-die exit (Gemini time collar):
    1. Limit +7c if hit first
    2. Bond 95c+ if surging
    3. At stall_sec: if no new high since entry AND bid hasn't gained progress_min, dump
    4. Otherwise keep monitoring until 45s or bond
    """
    series = _bid_series(tape, entry.ts_ms, 45.0)
    markouts: dict[int, int] = {}
    for sec in (5, 10, 15, 20, 25, 30, 35, 45):
        b = _bid_at_offset(tape, entry.ts_ms, sec)
        if b is not None:
            markouts[sec] = b

    target = entry.entry_cents + scalp_plus
    peak = entry.entry_cents
    stall_checked = False

    for elapsed, bid in series:
        peak = max(peak, bid)

        if bid >= target:
            return TradeResult(
                entry=entry,
                strategy=f"time_collar_{int(stall_sec)}s",
                exit_cents=target,
                exit_at_sec=elapsed,
                exit_reason=f"scalp limit +{scalp_plus}c",
                pnl_cents=scalp_plus,
                markouts=markouts,
            )

        if bid >= bond_cents:
            return TradeResult(
                entry=entry,
                strategy=f"time_collar_{int(stall_sec)}s",
                exit_cents=bid,
                exit_at_sec=elapsed,
                exit_reason=f"bond surge @ {bid}c",
                pnl_cents=bid - entry.entry_cents,
                markouts=markouts,
            )

        if not stall_checked and elapsed >= stall_sec:
            stall_checked = True
            made_new_high = peak > entry.entry_cents
            gained = bid - entry.entry_cents
            if not made_new_high or gained < progress_min_cents:
                return TradeResult(
                    entry=entry,
                    strategy=f"time_collar_{int(stall_sec)}s",
                    exit_cents=bid,
                    exit_at_sec=elapsed,
                    exit_reason=f"stall @ {int(stall_sec)}s (peak {peak}c, bid {bid}c)",
                    pnl_cents=bid - entry.entry_cents,
                    markouts=markouts,
                )

    final = series[-1][1] if series else entry.entry_cents
    return TradeResult(
        entry=entry,
        strategy=f"time_collar_{int(stall_sec)}s",
        exit_cents=final,
        exit_at_sec=45.0,
        exit_reason="time stop 45s",
        pnl_cents=final - entry.entry_cents,
        markouts=markouts,
    )


def _simulate_var_watch_collar(
    entry: TradeEntry,
    tape: list[TapePoint],
    *,
    check_sec: float = 25.0,
    limbo_max_gain: int = 3,
    limbo_peak_cap: int = 88,
) -> TradeResult:
    """
    Tight collar for VAR-risk entries (Gemini Flag #10 logic):
    - Take +7c scalp if available
    - At check_sec: if peak < limbo_peak_cap and bid hasn't cleared entry+limbo_max_gain, dump
    - Trailing: exit if bid drops 8c from peak after check_sec
    """
    series = _bid_series(tape, entry.ts_ms, 45.0)
    markouts: dict[int, int] = {}
    for sec in (5, 10, 15, 20, 25, 30, 35, 45):
        b = _bid_at_offset(tape, entry.ts_ms, sec)
        if b is not None:
            markouts[sec] = b

    target = entry.entry_cents + 7
    peak = entry.entry_cents
    limbo_checked = False

    for elapsed, bid in series:
        peak = max(peak, bid)

        if bid >= target:
            return TradeResult(
                entry=entry,
                strategy="var_watch_collar",
                exit_cents=target,
                exit_at_sec=elapsed,
                exit_reason=f"scalp limit +7c",
                pnl_cents=7,
                markouts=markouts,
            )

        if not limbo_checked and elapsed >= check_sec:
            limbo_checked = True
            if peak < limbo_peak_cap and bid <= entry.entry_cents + limbo_max_gain:
                return TradeResult(
                    entry=entry,
                    strategy="var_watch_collar",
                    exit_cents=bid,
                    exit_at_sec=elapsed,
                    exit_reason=f"VAR limbo @ {int(check_sec)}s (peak {peak}c, bid {bid}c)",
                    pnl_cents=bid - entry.entry_cents,
                    markouts=markouts,
                )

        if limbo_checked and peak - bid >= 8:
            return TradeResult(
                entry=entry,
                strategy="var_watch_collar",
                exit_cents=bid,
                exit_at_sec=elapsed,
                exit_reason=f"trailing stop from peak {peak}c",
                pnl_cents=bid - entry.entry_cents,
                markouts=markouts,
            )

    final = series[-1][1] if series else entry.entry_cents
    return TradeResult(
        entry=entry,
        strategy="var_watch_collar",
        exit_cents=final,
        exit_at_sec=45.0,
        exit_reason="time stop 45s",
        pnl_cents=final - entry.entry_cents,
        markouts=markouts,
    )


def _simulate_recommended(entry: TradeEntry, tape: list[TapePoint]) -> TradeResult:
    """Use exit_mode hint: hold_bond -> hold; var_watch -> tight collar; else time collar."""
    if entry.exit_mode == "hold_bond":
        return _simulate_hold_bond(entry, tape)
    if entry.exit_mode == "var_watch":
        return _simulate_var_watch_collar(entry, tape)
    return _simulate_time_collar(entry, tape, stall_sec=20.0, progress_min_cents=3)


def backtest_session(session_dir: Path) -> str:
    tape, entries = _load_tape(session_dir)
    lines: list[str] = []
    lines.append(f"# Exit backtest: {session_dir.name}")
    lines.append("")
    lines.append(f"Goal signals detected: **{len(entries)}**")
    lines.append("")

    strategies = ["limit_+7c", "hold_bond", "time_collar_20s", "var_watch_collar", "recommended"]
    totals: dict[str, int] = {s: 0 for s in strategies}

    for i, entry in enumerate(entries, 1):
        t = tape[entry.ticker]
        short = _short_ticker(entry.ticker)
        lines.append(f"## Trade {i}: {short} @ {entry.ts_iso[:19]}")
        lines.append(
            f"- Entry: **{entry.entry_cents}¢** | jump +{entry.bid_jump_cents}¢ | mode: `{entry.exit_mode}`"
        )
        markout_parts = []
        for sec in (15, 20, 25, 30):
            b = _bid_at_offset(t, entry.ts_ms, sec)
            if b is not None:
                markout_parts.append(f"+{sec}s: {b}¢ ({b - entry.entry_cents:+d}¢)")
        if markout_parts:
            lines.append("- Markouts: " + " | ".join(markout_parts))
        lines.append("")
        lines.append("| Strategy | Exit | P&L | Reason |")
        lines.append("|----------|------|-----|--------|")

        results = [
            _simulate_limit_scalp(entry, t),
            _simulate_hold_bond(entry, t),
            _simulate_time_collar(entry, t, stall_sec=20.0),
            _simulate_var_watch_collar(entry, t) if entry.exit_mode == "var_watch" else None,
            _simulate_recommended(entry, t),
        ]
        labels = ["limit_+7c", "hold_bond", "time_collar_20s", "var_watch_collar", "recommended"]
        for label, res in zip(labels, results):
            if res is None:
                continue
            totals[label] += res.pnl_cents
            lines.append(
                f"| {label} | {res.exit_cents}¢ @ {res.exit_at_sec:.0f}s | "
                f"**{res.pnl_cents:+d}¢** | {res.exit_reason} |"
            )
        lines.append("")

    lines.append("## Session totals (per contract)")
    lines.append("")
    lines.append("| Strategy | Total P&L |")
    lines.append("|----------|-----------|")
    for label in strategies:
        lines.append(f"| {label} | **{totals[label]:+d}¢** (${totals[label]/100:+.2f}) |")
    lines.append("")
    lines.append("### Notes")
    lines.append("- Entry assumes fill at signal bid (queue risk not modeled).")
    lines.append("- `time_collar_20s`: exit at +20s if bid hasn't made new high or gained ≥3¢.")
    lines.append("- `var_watch_collar`: at +25s exit if peak <88¢ and bid ≤ entry+3¢; trailing -8¢ from peak.")
    lines.append("- Not every line reaches 95¢ — time collar lets mid-price winners run via +7¢ limit.")
    lines.append("")
    return "\n".join(lines)


def run_backtest(session_dir: Path) -> Path:
    report = backtest_session(session_dir)
    out = session_dir / "exit_backtest.md"
    out.write_text(report, encoding="utf-8")
    return out


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m suspension_lab.backtest_exits <session_folder>")
        raise SystemExit(1)
    folder = Path(sys.argv[1]).resolve()
    print(backtest_session(folder))
    path = run_backtest(folder)
    print(f"\nSaved: {path}")
