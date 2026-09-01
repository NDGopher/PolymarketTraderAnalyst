"""Estimate fill feasibility at goal-signal entries from saved session tape."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from suspension_lab.goal_signal import GoalSignal, GoalSignalDetector
from suspension_lab.orderbook import OrderBook


def _ticker_prefixes(headers: list[str]) -> list[str]:
    return [h[: -len("_yes_bid")] for h in headers if h.endswith("_yes_bid")]


def _short(prefix: str) -> str:
    parts = prefix.split("-")
    return "-".join(parts[-2:]) if len(parts) >= 2 else prefix


@dataclass
class FillReport:
    ts_iso: str
    ticker: str
    entry_cents: int
    top_bid_qty: float
    bid_depth_3: float
    ask_qty: float
    spread_cents: str
    exit_mode: str
    target_size: int
    queue_ahead: float
    verdict: str
    note: str


def analyze_fills(session_dir: Path, *, target_size: int = 100) -> str:
    books_path = session_dir / "books.csv"
    with books_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        prefixes = _ticker_prefixes(headers)
        rows = list(reader)

    detectors = {p: GoalSignalDetector() for p in prefixes}
    reports: list[FillReport] = []

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
            if not isinstance(result, GoalSignal):
                continue

            entry_cents = int(round(result.new_bid * 100))
            top_qty = float(row.get(f"{prefix}_yes_bid_qty", 0) or 0)
            levels = book.top_levels()
            depth_3 = float(levels.get("bid_depth_3", 0) or 0)
            spread = str(row.get(f"{prefix}_spread_cents", ""))

            note = ""
            for later in rows[i + 1 : i + 20]:
                if int(later["ts_ms"]) > ts_ms + 5000:
                    break
                lb = later.get(f"{prefix}_yes_bid", "")
                if not lb:
                    continue
                lb_c = int(round(Decimal(lb) * 100))
                if lb_c > entry_cents:
                    note = f"bid lifted to {lb_c}c within 5s"
                    break
                if lb_c == entry_cents:
                    lq = float(later.get(f"{prefix}_yes_bid_qty", 0) or 0)
                    if lq < top_qty - 10:
                        note = f"qty at {entry_cents}c fell {top_qty:.0f}->{lq:.0f} in 5s"
                        break

            if top_qty >= target_size * 3:
                verdict = "back of queue — partial/none likely at join-bid"
            elif top_qty >= target_size:
                verdict = "queue exists — bid+1c or wait for lift"
            elif depth_3 >= target_size:
                verdict = "thin top but 3-level depth OK — bid+1c likely fills"
            else:
                verdict = "thin book — may need to lift ask (taker)"

            reports.append(
                FillReport(
                    ts_iso=row["ts_iso"],
                    ticker=prefix,
                    entry_cents=entry_cents,
                    top_bid_qty=top_qty,
                    bid_depth_3=depth_3,
                    ask_qty=float(row.get(f"{prefix}_yes_ask_qty", 0) or 0),
                    spread_cents=spread,
                    exit_mode=result.exit_mode,
                    target_size=target_size,
                    queue_ahead=top_qty,
                    verdict=verdict,
                    note=note,
                )
            )

    lines = [
        f"# Fill analysis: {session_dir.name}",
        "",
        f"Target size: **{target_size} contracts** at signal bid (join queue, not bid+1).",
        "",
        "Kalshi almost always shows **500** at the jump price — that is the house/MM layer.",
        "Joining that bid puts you behind it. Fills happen when sellers hit the stack or you bid +1¢.",
        "",
        "| Time | Ticker | Entry | Top bid qty | 3-lvl bid | Spread | Mode | Verdict |",
        "|------|--------|-------|-------------|-----------|--------|------|---------|",
    ]
    for r in reports:
        lines.append(
            f"| {r.ts_iso[11:19]} | {_short(r.ticker)} | {r.entry_cents}¢ | "
            f"{r.top_bid_qty:.0f} | {r.bid_depth_3:.0f} | {r.spread_cents}¢ | "
            f"`{r.exit_mode}` | {r.verdict} |"
        )
        if r.note:
            lines.append(f"| | | | | | | | _{r.note}_ |")

    lines.extend(
        [
            "",
            "## Practical sizing",
            "",
            "- **Join bid at signal:** assume 0–partial fill unless top qty < 50",
            "- **Bid +1¢:** better fill odds; costs 1¢ more",
            "- **100 contracts:** fine on liquid EFL lines; reduce on Swiss/thin books",
            "- **Penalty reviews:** often no ≥10¢ bid jump — green box may not fire (expected)",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m suspension_lab.analyze_fills <session_folder> [size]")
        raise SystemExit(1)
    folder = Path(sys.argv[1]).resolve()
    size = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    report = analyze_fills(folder, target_size=size)
    print(report)
    out = folder / "fill_analysis.md"
    out.write_text(report, encoding="utf-8")
    print(f"\nSaved: {out}")
