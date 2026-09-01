from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from suspension_lab.config import MARKOUT_SECONDS


def _f(val: Any) -> float | None:
    if val is None or val == "":
        return None
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def _bool(val: Any) -> bool:
    return str(val).lower() in ("true", "1", "yes")


def _ms_to_local(ms: int) -> str:
    from datetime import datetime

    return datetime.fromtimestamp(ms / 1000).strftime("%H:%M:%S.%f")[:-3]


@dataclass
class LabEvent:
    event_id: int
    ts_ms: int
    event_type: str
    b365: str
    fd: str
    dk: str
    ticker_data: dict[str, dict[str, Any]] = field(default_factory=dict)
    markouts: dict[str, dict[int, dict[str, Any]]] = field(default_factory=dict)


@dataclass
class BookRow:
    ts_ms: int
    b365: str
    fd: str
    dk: str
    tickers: dict[str, dict[str, Any]]


def _ticker_prefixes(headers: list[str]) -> list[str]:
    mids = [h for h in headers if h.endswith("_yes_mid")]
    return [h[: -len("_yes_mid")] for h in mids]


def load_session(session_dir: Path) -> tuple[dict, list[LabEvent], list[BookRow], list[str]]:
    meta = json.loads((session_dir / "session.json").read_text(encoding="utf-8"))
    tickers: list[str] = meta.get("tickers", [])

    events: list[LabEvent] = []
    with (session_dir / "events.csv").open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        prefixes = _ticker_prefixes(headers) or [t.replace(",", "_") for t in tickers]

        for row in reader:
            td: dict[str, dict[str, Any]] = {}
            mo: dict[str, dict[int, dict[str, Any]]] = {}
            for prefix in prefixes:
                td[prefix] = {
                    "yes_bid": row.get(f"{prefix}_yes_bid", ""),
                    "yes_ask": row.get(f"{prefix}_yes_ask", ""),
                    "yes_mid": _f(row.get(f"{prefix}_yes_mid")),
                    "spread_cents": row.get(f"{prefix}_spread_cents", ""),
                    "wide_spread": _bool(row.get(f"{prefix}_wide_spread")),
                    "tight_spread": _bool(row.get(f"{prefix}_tight_spread")),
                    "untradeable": _bool(row.get(f"{prefix}_untradeable")),
                    "suggested_bid": row.get(f"{prefix}_suggested_bid_plus_2c", ""),
                }
                mo[prefix] = {}
                for sec in MARKOUT_SECONDS:
                    mo[prefix][sec] = {
                        "yes_mid": _f(row.get(f"{prefix}_mid_{sec}s")),
                        "spread_cents": row.get(f"{prefix}_spread_cents_{sec}s", ""),
                    }

            events.append(
                LabEvent(
                    event_id=int(row["event_id"]),
                    ts_ms=int(row["event_ts_ms"]),
                    event_type=row["event_type"],
                    b365=row["b365_state"],
                    fd=row["fd_state"],
                    dk=row["dk_state"],
                    ticker_data=td,
                    markouts=mo,
                )
            )

    books: list[BookRow] = []
    with (session_dir / "books.csv").open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        prefixes = _ticker_prefixes(headers) or [t.replace(",", "_") for t in tickers]
        for row in reader:
            td = {}
            for prefix in prefixes:
                td[prefix] = {
                    "yes_mid": _f(row.get(f"{prefix}_yes_mid")),
                    "spread_cents": row.get(f"{prefix}_spread_cents", ""),
                    "wide_spread": _bool(row.get(f"{prefix}_wide_spread")),
                    "tight_spread": _bool(row.get(f"{prefix}_tight_spread")),
                    "untradeable": _bool(row.get(f"{prefix}_untradeable")),
                }
            books.append(
                BookRow(
                    ts_ms=int(row["ts_ms"]),
                    b365=row.get("b365_state", ""),
                    fd=row.get("fd_state", ""),
                    dk=row.get("dk_state", ""),
                    tickers=td,
                )
            )

    return meta, events, books, prefixes


def _pick_primary_ticker(prefixes: list[str], events: list[LabEvent], books: list[BookRow]) -> str:
    """Prefer non-bond ticker with most mid movement."""
    best = prefixes[0] if prefixes else ""
    best_range = -1.0
    for prefix in prefixes:
        mids = [e.ticker_data.get(prefix, {}).get("yes_mid") for e in events]
        mids += [b.tickers.get(prefix, {}).get("yes_mid") for b in books]
        vals = [m for m in mids if m is not None]
        if len(vals) < 2:
            continue
        rng = max(vals) - min(vals)
        if rng > best_range:
            best_range = rng
            best = prefix
    return best


def _find_mid_jumps(
    books: list[BookRow], prefix: str, *, min_jump_cents: float = 5.0, window_ms: int = 3000
) -> list[dict]:
    jumps: list[dict] = []
    for i in range(1, len(books)):
        prev = books[i - 1].tickers.get(prefix, {}).get("yes_mid")
        cur = books[i].tickers.get(prefix, {}).get("yes_mid")
        if prev is None or cur is None:
            continue
        delta_c = (cur - prev) * 100
        if abs(delta_c) >= min_jump_cents:
            ts = books[i].ts_ms
            jumps.append(
                {
                    "ts_ms": ts,
                    "time": _ms_to_local(ts),
                    "from_mid": prev,
                    "to_mid": cur,
                    "delta_cents": round(delta_c, 1),
                    "spread_cents": books[i].tickers.get(prefix, {}).get("spread_cents"),
                    "wide": books[i].tickers.get(prefix, {}).get("wide_spread"),
                }
            )
    # dedupe clusters within window
    if not jumps:
        return []
    merged = [jumps[0]]
    for j in jumps[1:]:
        if j["ts_ms"] - merged[-1]["ts_ms"] < window_ms:
            if abs(j["delta_cents"]) > abs(merged[-1]["delta_cents"]):
                merged[-1] = j
        else:
            merged.append(j)
    return merged


def _first_book_state_change(events: list[LabEvent], book: str, to_state: str) -> LabEvent | None:
    for e in events:
        state = {"b365": e.b365, "fd": e.fd, "dk": e.dk}[book]
        if e.event_type.upper().startswith(book.upper()) and to_state.upper() in e.event_type.upper():
            return e
        if state.upper() == to_state.upper() and e.event_type.endswith(f"_{to_state.upper()}"):
            return e
    for e in events:
        if book == "b365" and "B365" in e.event_type and to_state.upper() in e.event_type:
            return e
        if book == "fd" and "FANDUEL" in e.event_type and to_state.upper() in e.event_type:
            return e
        if book == "dk" and "DRAFTKINGS" in e.event_type and to_state.upper() in e.event_type:
            return e
    return None


def analyze_session(session_dir: Path) -> str:
    meta, events, books, prefixes = load_session(session_dir)
    primary = _pick_primary_ticker(prefixes, events, books)
    game = meta.get("game_label", session_dir.name)
    lines: list[str] = []

    lines.append(f"# Suspension Lab Analysis: {game}")
    lines.append("")
    lines.append(f"Session: `{session_dir.name}`")
    lines.append(f"Started: {meta.get('started_at', '?')}")
    lines.append(f"Tickers tracked: {len(prefixes)}")
    lines.append(f"Primary analysis ticker (most movement): `{primary}`")
    lines.append(f"Book tape rows: {len(books):,} (~{len(books) * 0.2:.0f}s at 200ms)")
    lines.append(f"Manual events: {len(events)}")
    lines.append("")

  # --- Manual click timeline ---
    lines.append("## Sportsbook click timeline")
    lines.append("")
    if not events:
        lines.append("*No manual B/F/D clicks logged.*")
    else:
        lines.append("| Time | Event | B365 | FD | DK | Primary mid | Spread | Wide? |")
        lines.append("|------|-------|------|----|----|-------------|--------|-------|")
        for e in events:
            td = e.ticker_data.get(primary, {})
            mid = td.get("yes_mid")
            mid_s = f"{mid:.2f}" if mid is not None else "?"
            sp = td.get("spread_cents", "?")
            wide = "YES" if td.get("wide_spread") else "no"
            lines.append(
                f"| {_ms_to_local(e.ts_ms)} | {e.event_type} | {e.b365} | {e.fd} | {e.dk} | "
                f"{mid_s} | {sp}c | {wide} |"
            )
    lines.append("")

    # --- Book suspension cluster from flags ---
    b365_down = _first_book_state_change(events, "b365", "DOWN")
    dk_down = _first_book_state_change(events, "dk", "DOWN")
    fd_down = _first_book_state_change(events, "fd", "DOWN")
    b365_up = _first_book_state_change(events, "b365", "UP")
    dk_up = _first_book_state_change(events, "dk", "UP")
    fd_up = _first_book_state_change(events, "fd", "UP")

    lines.append("## Suspension timing (your clicks)")
    lines.append("")
    for label, ev in [
        ("bet365 DOWN", b365_down),
        ("DraftKings DOWN", dk_down),
        ("FanDuel DOWN", fd_down),
        ("bet365 UP", b365_up),
        ("DraftKings UP", dk_up),
        ("FanDuel UP", fd_up),
    ]:
        if ev:
            gap = ""
            if b365_down and ev != b365_down:
                gap = f" (+{(ev.ts_ms - b365_down.ts_ms) / 1000:.2f}s vs b365 first down)"
            lines.append(f"- **{label}:** {_ms_to_local(ev.ts_ms)}{gap}")
        else:
            lines.append(f"- **{label}:** (not logged)")
    if b365_down and dk_down:
        lines.append(
            f"- **b365 → DK lag:** {(dk_down.ts_ms - b365_down.ts_ms) / 1000:.2f}s"
        )
    if b365_down and fd_down:
        lines.append(
            f"- **b365 → FD lag:** {(fd_down.ts_ms - b365_down.ts_ms) / 1000:.2f}s"
        )
    if b365_up and fd_up:
        lines.append(
            f"- **b365 → FD reopen lag:** {(fd_up.ts_ms - b365_up.ts_ms) / 1000:.2f}s"
        )
    lines.append("")

    # --- Kalshi jumps from tape (no clicks needed) ---
    jumps = _find_mid_jumps(books, primary)
    lines.append("## Kalshi mid jumps (from 200ms tape, no clicks needed)")
    lines.append("")
    if not jumps:
        lines.append("*No >=5c mid jumps detected on primary ticker.*")
    else:
        lines.append("| Time | Mid move | Spread | Wide? |")
        lines.append("|------|----------|--------|-------|")
        for j in jumps[:15]:
            lines.append(
                f"| {j['time']} | {j['from_mid']:.2f} → {j['to_mid']:.2f} "
                f"({j['delta_cents']:+.0f}c) | {j['spread_cents']}c | "
                f"{'YES' if j['wide'] else 'no'} |"
            )
    lines.append("")

    # --- Lag: books vs Kalshi ---
    lines.append("## Lag analysis: books vs Kalshi")
    lines.append("")
    if b365_down and jumps:
        first_jump = min(jumps, key=lambda x: x["ts_ms"])
        lag_ms = first_jump["ts_ms"] - b365_down.ts_ms
        lines.append(
            f"- First Kalshi jump (>=5c): **{_ms_to_local(first_jump['ts_ms'])}** "
            f"({first_jump['from_mid']:.2f} → {first_jump['to_mid']:.2f})"
        )
        lines.append(
            f"- vs your **b365 DOWN** click: **{lag_ms / 1000:+.2f}s** "
            f"(negative = Kalshi moved before you clicked)"
        )
        if dk_down:
            lag_dk = first_jump["ts_ms"] - dk_down.ts_ms
            lines.append(f"- vs your **DK DOWN** click: **{lag_dk / 1000:+.2f}s**")
    elif jumps and not b365_down:
        lines.append("*Kalshi moved but no b365 DOWN click logged — check events.csv.*")
    else:
        lines.append("*Insufficient data for lag comparison.*")
    lines.append("")

    # --- Markouts on DOWN events ---
    lines.append("## Markouts after suspension clicks (primary ticker)")
    lines.append("")
    down_events = [e for e in events if "DOWN" in e.event_type]
    if not down_events:
        lines.append("*No DOWN events.*")
    else:
        for e in down_events:
            td = e.ticker_data.get(primary, {})
            mid0 = td.get("yes_mid")
            lines.append(f"### {e.event_type} @ {_ms_to_local(e.ts_ms)}")
            if mid0 is not None:
                lines.append(f"- At click: mid **{mid0:.2f}**, spread **{td.get('spread_cents')}c**, "
                             f"wide={'YES' if td.get('wide_spread') else 'no'}, "
                             f"suggest bid **{td.get('suggested_bid')}**")
            mo = e.markouts.get(primary, {})
            parts = []
            for sec in MARKOUT_SECONDS:
                m = mo.get(sec, {}).get("yes_mid")
                sp = mo.get(sec, {}).get("spread_cents")
                if m is not None and mid0 is not None:
                    parts.append(f"+{sec}s: {m:.2f} ({(m - mid0) * 100:+.0f}c, spread {sp}c)")
                elif m is not None:
                    parts.append(f"+{sec}s: {m:.2f}")
            if parts:
                lines.append("- Markouts: " + " | ".join(parts))
            lines.append("")

    # --- Tradeability verdict ---
    lines.append("## Tradeability at suspension")
    lines.append("")
    if b365_down:
        td = b365_down.ticker_data.get(primary, {})
        wide = td.get("wide_spread")
        untrade = td.get("untradeable")
        lines.append(
            f"At **b365 DOWN**: spread **{td.get('spread_cents')}c**, "
            f"wide={'YES — do NOT hit ask' if wide else 'no — tight book'}, "
            f"untradeable flag={'YES' if untrade else 'no'}"
        )
        if wide:
            lines.append(
                f"- Strategy: bid **{td.get('suggested_bid')}** (best bid +2c), not taker at ask"
            )
        else:
            lines.append("- Strategy: could consider bidding near mid or lifting ask if liquidity exists")
    lines.append("")

    # --- Summary ---
    lines.append("## Summary")
    lines.append("")
    if b365_down and dk_down and fd_down:
        cluster_ms = max(dk_down.ts_ms, fd_down.ts_ms) - b365_down.ts_ms
        lines.append(
            f"1. **Book order:** b365 first, DK {(dk_down.ts_ms - b365_down.ts_ms) * 1000:.0f}ms later, "
            f"FD {(fd_down.ts_ms - b365_down.ts_ms) * 1000:.0f}ms after b365."
        )
    if b365_up and fd_up and (fd_up.ts_ms - b365_up.ts_ms) > 500:
        lines.append(
            f"2. **Reopen:** FD lagged b365 by {(fd_up.ts_ms - b365_up.ts_ms) / 1000:.1f}s on the way back up."
        )
    if jumps:
        biggest = max(jumps, key=lambda x: abs(x["delta_cents"]))
        lines.append(
            f"3. **Kalshi:** largest move {biggest['delta_cents']:+.0f}c at {biggest['time']} "
            f"({biggest['from_mid']:.2f} → {biggest['to_mid']:.2f})."
        )
    lines.append("")

    return "\n".join(lines)


def run_analysis(session_dir: Path) -> Path:
    report = analyze_session(session_dir)
    out = session_dir / "analysis.md"
    out.write_text(report, encoding="utf-8")
    return out


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m suspension_lab.analyze_session <session_folder>")
        raise SystemExit(1)
    folder = Path(sys.argv[1]).resolve()
    print(analyze_session(folder))
    out = run_analysis(folder)
    print(f"\nSaved: {out}")
