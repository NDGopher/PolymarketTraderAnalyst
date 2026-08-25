#!/usr/bin/env python3
"""Generate MASTER reports for all target traders + cross-comparison."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from polyanalyst.mega_report import generate_master  # noqa: E402
from polyanalyst.pipeline import AnalyzerApp  # noqa: E402

TRADERS = ["polika72", "HomeRunHazard", "Winnertraders", "WTSA"]


def _cmp_row(master: dict) -> dict:
    recon = master["reconciliation"]
    pref = recon.get("preferred_pnl") or {}
    ident = master["identity"]
    copy = master["copyability"]
    perf = master["performance"]
    extras = master["extras"]
    eq = perf.get("equity") or {}
    ceq = master.get("equity_closed_summary") or {}
    return {
        "username": master["meta"]["username"],
        "wallet": master["meta"]["wallet"],
        "identity": ident["class"],
        "preferred_pnl_field": pref.get("field"),
        "preferred_pnl": pref.get("value"),
        "leaderboard_pnl": pref.get("leaderboard_all"),
        "cashflow_pnl": recon["ours"]["cashflow_realized"],
        "closed_pnl": recon["ours"]["closed_positions_sum"],
        "trades": recon["ours"]["trades"],
        "buys": recon["ours"]["buys"],
        "sells": recon["ours"]["sells"],
        "win_rate": recon["ours"]["win_rate_legs"],
        "profit_factor": recon["ours"]["profit_factor"],
        "both_sides_rate": ident["both_sides"]["rate"],
        "entry_maker_pct": (ident["maker_taker"].get("entry") or {}).get("maker_pct"),
        "entry_taker_pct": (ident["maker_taker"].get("entry") or {}).get("taker_pct"),
        "clip_median": ident["clip_size_usdc"]["median"],
        "primary_focus": ident["sport_focus"].get("primary"),
        "days_span": perf["span"].get("days_active_span"),
        "cashflow_max_dd": eq.get("max_drawdown"),
        "cashflow_sharpe": eq.get("daily_sharpe_ann"),
        "closed_max_dd": ceq.get("max_drawdown"),
        "closed_sharpe": ceq.get("daily_sharpe_ann"),
        "expectancy": extras.get("expectancy_per_market"),
        "pnl_per_day": extras.get("pnl_per_day"),
        "difficulty": copy["difficulty_1_to_10"],
        "ease": copy["ease_of_copy_1_to_10"],
        "exit_mechanics": copy.get("exit_mechanics"),
        "kalshi_fit": copy.get("kalshi_two_sided_mm_fit"),
        "copy_why": copy.get("why"),
    }


def write_comparison(masters: list[dict], out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = [_cmp_row(m) for m in masters]
    payload = {"traders": rows, "n": len(rows)}
    (out_dir / "comparison.json").write_text(json.dumps(payload, indent=2))

    lines = [
        "# Cross-trader comparison — polika72 · HomeRunHazard · Winnertraders · WTSA",
        "",
        "Preferred PnL = field closest to Polymarket leaderboard ALL (ground truth).",
        "",
        "| Trader | Identity | Preferred PnL | LB ALL | Trades | WR | Both-sides | Entry maker% | Diff/Ease | Exit |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['username']} | `{r['identity']}` | ${r['preferred_pnl']:,.2f} | "
            f"${(r['leaderboard_pnl'] or 0):,.2f} | {r['trades']:,} | "
            f"{100*(r['win_rate'] or 0):.1f}% | {100*(r['both_sides_rate'] or 0):.1f}% | "
            f"{r['entry_maker_pct']} | {r['difficulty']}/{r['ease']} | `{r['exit_mechanics']}` |"
        )
    lines += ["", "## Equity / risk", ""]
    lines.append("| Trader | Cashflow final | Cashflow max DD | Cashflow Sharpe | Closed final | Closed max DD | Closed Sharpe |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for m, r in zip(masters, rows):
        eq = m["performance"]["equity"]
        ceq = m.get("equity_closed_summary") or {}
        lines.append(
            f"| {r['username']} | ${eq.get('final', 0):,.2f} | ${eq.get('max_drawdown', 0):,.2f} | "
            f"{eq.get('daily_sharpe_ann')} | ${ceq.get('final', 0):,.2f} | "
            f"${ceq.get('max_drawdown', 0):,.2f} | {ceq.get('daily_sharpe_ann')} |"
        )
    lines += ["", "## Copyability", ""]
    for r in rows:
        lines.append(f"### {r['username']}")
        lines.append(f"- Difficulty **{r['difficulty']}/10** · Ease **{r['ease']}/10**")
        lines.append(f"- {r['copy_why']}")
        lines.append(f"- Kalshi fit: {r['kalshi_fit']}")
        lines.append("")
    lines += [
        "## Artifact map",
        "",
        "Per trader under `samples/<name>/`:",
        "- `MASTER.md` — human mega-report",
        "- `MASTER.json` — bot schema",
        "- `equity_curve.csv` / `equity_curve_closed.csv`",
        "",
    ]
    path = out_dir / "comparison.md"
    path.write_text("\n".join(lines))
    return path


def main() -> None:
    app = AnalyzerApp(ROOT / "data")
    masters = []
    for name in TRADERS:
        print(f"=== MASTER {name} ===", flush=True)
        path = generate_master(app, name)
        master = json.loads((path.parent / "MASTER.json").read_text())
        masters.append(master)
        print(f"wrote {path} ({path.stat().st_size:,} bytes)", flush=True)

    cmp_path = write_comparison(masters, ROOT / "samples" / "_comparison")
    # mirror under data/reports
    data_cmp = ROOT / "data" / "reports" / "_comparison"
    data_cmp.mkdir(parents=True, exist_ok=True)
    for f in (ROOT / "samples" / "_comparison").iterdir():
        (data_cmp / f.name).write_text(f.read_text())
    print(f"comparison: {cmp_path}", flush=True)


if __name__ == "__main__":
    main()
