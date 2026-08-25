"""Compare multiple analyzed traders: commons + differences."""

from __future__ import annotations

from typing import Any


def compare_traders(summaries: list[dict[str, Any]]) -> dict[str, Any]:
    if len(summaries) < 2:
        raise ValueError("Need at least two trader summaries to compare")

    rows = []
    for s in summaries:
        mm = s.get("market_making") or {}
        pnl = s.get("pnl") or {}
        sizing = s.get("sizing") or {}
        cats = (s.get("categories") or {}).get("pnl") or {}
        top_cat = next(iter(cats.keys()), None)
        rows.append(
            {
                "username": s.get("username"),
                "wallet": s.get("wallet"),
                "realized_cashflow": pnl.get("cashflow_realized"),
                "closed_pnl": pnl.get("closed_positions_sum"),
                "win_rate": pnl.get("win_rate"),
                "profit_factor": pnl.get("profit_factor"),
                "trades": (s.get("counts") or {}).get("trades"),
                "markets": (s.get("counts") or {}).get("markets_traded"),
                "mm_label": mm.get("label"),
                "mm_score": mm.get("score"),
                "both_sides_rate": (mm.get("metrics") or {}).get("both_sides_rate"),
                "spread_capture_rate": (mm.get("metrics") or {}).get("spread_capture_rate"),
                "median_ticket": sizing.get("median_usdc"),
                "max_dd": (s.get("equity") or {}).get("max_drawdown"),
                "top_category": top_cat,
                "category_pnl": cats,
            }
        )

    # Common / different qualitative flags
    labels = {r["mm_label"] for r in rows}
    top_cats = {r["top_category"] for r in rows}
    commons = []
    diffs = []
    if len(labels) == 1:
        commons.append(f"All classified as `{next(iter(labels))}`")
    else:
        diffs.append(f"Strategy labels diverge: {', '.join(f'{r['username']}={r['mm_label']}' for r in rows)}")
    if len(top_cats) == 1:
        commons.append(f"Same primary PnL category: `{next(iter(top_cats))}`")
    else:
        diffs.append(
            "Primary categories differ: "
            + ", ".join(f"{r['username']}={r['top_category']}" for r in rows)
        )

    wr = [r["win_rate"] for r in rows if r["win_rate"] is not None]
    if wr and max(wr) - min(wr) < 0.05:
        commons.append(f"Similar win rates (~{100*sum(wr)/len(wr):.1f}%)")
    elif wr:
        diffs.append(
            "Win rates: " + ", ".join(f"{r['username']}={100*(r['win_rate'] or 0):.1f}%" for r in rows)
        )

    mm_scores = [r["mm_score"] or 0 for r in rows]
    if min(mm_scores) >= 45:
        commons.append("All show market-making / spread-capture fingerprints")
    elif max(mm_scores) >= 45 and min(mm_scores) < 45:
        diffs.append("Mix of MM-like and directional profiles")

    # Numeric deltas vs first trader as baseline
    base = rows[0]
    relative = []
    for r in rows[1:]:
        relative.append(
            {
                "vs": f"{r['username']} vs {base['username']}",
                "pnl_delta": (r["realized_cashflow"] or 0) - (base["realized_cashflow"] or 0),
                "win_rate_delta": (r["win_rate"] or 0) - (base["win_rate"] or 0),
                "trades_ratio": ((r["trades"] or 0) / (base["trades"] or 1)),
                "mm_score_delta": (r["mm_score"] or 0) - (base["mm_score"] or 0),
            }
        )

    return {
        "traders": rows,
        "commons": commons,
        "differences": diffs,
        "relative": relative,
    }


def format_comparison(report: dict[str, Any]) -> str:
    lines = ["# Trader comparison", ""]
    lines.append("## Snapshot")
    lines.append("")
    lines.append("| Trader | Realized CF | Win rate | Trades | MM label | Top category |")
    lines.append("|---|---:|---:|---:|---|---|")
    for r in report["traders"]:
        lines.append(
            f"| {r['username']} | {r['realized_cashflow']:,.2f} | {100*(r['win_rate'] or 0):.1f}% | "
            f"{r['trades']:,} | {r['mm_label']} | {r['top_category']} |"
        )
    lines.append("")
    lines.append("## In common")
    lines.append("")
    for c in report.get("commons") or ["(none flagged)"]:
        lines.append(f"- {c}")
    lines.append("")
    lines.append("## Differences")
    lines.append("")
    for d in report.get("differences") or ["(none flagged)"]:
        lines.append(f"- {d}")
    lines.append("")
    if report.get("relative"):
        lines.append("## Relative to first trader")
        lines.append("")
        for rel in report["relative"]:
            lines.append(
                f"- {rel['vs']}: PnL Δ {rel['pnl_delta']:,.2f}, "
                f"win-rate Δ {100*rel['win_rate_delta']:.1f}pp, "
                f"trade-count ×{rel['trades_ratio']:.2f}, "
                f"MM-score Δ {rel['mm_score_delta']}"
            )
        lines.append("")
    return "\n".join(lines)
