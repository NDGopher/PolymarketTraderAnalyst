"""Natural-language strategy analyst: how they win + how to replicate."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def _fmt_money(x: float) -> str:
    sign = "-" if x < 0 else ""
    return f"{sign}${abs(x):,.2f}"


def _fmt_secs(s: int | float | None) -> str:
    if s is None:
        return "n/a"
    s = int(s)
    if s < 60:
        return f"{s}s"
    if s < 3600:
        return f"{s // 60}m {s % 60}s"
    if s < 86400:
        return f"{s // 3600}h {(s % 3600) // 60}m"
    return f"{s // 86400}d {(s % 86400) // 3600}h"


def write_strategy_report(summary: dict[str, Any], validation: dict[str, Any] | None = None) -> str:
    u = summary["username"]
    w = summary["wallet"]
    pnl = summary["pnl"]
    mm = summary["market_making"]
    counts = summary["counts"]
    timing = summary["timing"]
    sizing = summary["sizing"]
    cats = summary["categories"]
    span = summary["span"]

    lines: list[str] = []
    lines.append(f"# Strategy Dossier: {u}")
    lines.append("")
    lines.append(f"- **Wallet:** `{w}`")
    lines.append(f"- **History span:** {span.get('first_iso')} → {span.get('last_iso')} ({span.get('days_active_span')} days)")
    lines.append(f"- **Trades:** {counts['trades']:,} (buys {counts['buys']:,} / sells {counts['sells']:,})")
    lines.append(f"- **Markets touched:** {counts['markets_traded']:,}")
    lines.append(f"- **Closed positions:** {counts['closed_positions']:,}")
    lines.append("")
    lines.append("## Headline performance")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|---|---|")
    lines.append(f"| Realized cashflow (sells − buys + redeems + rebates) | {_fmt_money(pnl['cashflow_realized'])} |")
    lines.append(f"| Core cashflow (ex-rebates) | {_fmt_money(pnl['cashflow_core'])} |")
    lines.append(f"| Closed-positions realized sum | {_fmt_money(pnl['closed_positions_sum'])} |")
    lines.append(f"| Win rate (closed) | {pnl['win_rate']*100:.2f}% ({pnl['closed_wins']}W / {pnl['closed_losses']}L) |")
    lines.append(f"| Profit factor | {pnl['profit_factor']} |")
    lines.append(f"| Gross wins / losses | {_fmt_money(pnl['win_pnl'])} / {_fmt_money(pnl['loss_pnl'])} |")
    lines.append(f"| Equity max drawdown | {_fmt_money(summary['equity']['max_drawdown'])} |")
    if pnl.get("leaderboard_all"):
        lb = pnl["leaderboard_all"]
        lines.append(f"| Polymarket leaderboard (ALL) | {_fmt_money(float(lb.get('pnl') or 0))} PnL · vol {_fmt_money(float(lb.get('vol') or 0))} · rank {lb.get('rank')} |")
    lines.append("")

    if validation:
        lines.append("## Source validation")
        lines.append("")
        for c in validation.get("checks", []):
            flag = "MATCH" if c.get("match") else "DRIFT"
            lines.append(
                f"- **{flag}** `{c['source']}` {c['metric']}: ours={c.get('ours')} ref={c.get('reference')} diff={c.get('diff')}"
            )
        lines.append("")

    lines.append("## What kind of trader is this?")
    lines.append("")
    lines.append(f"**Classification:** `{mm['label']}` (score {mm['score']}/100)")
    lines.append("")
    for s in mm.get("signals") or []:
        lines.append(f"- {s}")
    metrics = mm.get("metrics") or {}
    lines.append("")
    lines.append(
        f"Supporting rates — both-sides markets: {metrics.get('both_sides_rate')}, "
        f"fast round-trips: {metrics.get('fast_roundtrip_rate')}, "
        f"spread-capture rate: {metrics.get('spread_capture_rate')}."
    )
    lines.append("")

    # Core thesis
    lines.append("## Exact edge thesis")
    lines.append("")
    if mm["score"] >= 45:
        lines.append(
            f"{u} primarily monetizes **liquidity / short-horizon mean reversion on sports markets**, "
            "not long-shot directional political bets. The tape shows repeated buy-then-sell "
            "(and often both-outcome inventory) with average exit price above average entry — "
            "the classic market-maker / scalper fingerprint."
        )
    else:
        lines.append(
            f"{u} looks more **directional**: edges concentrate in being right about outcomes "
            "rather than harvesting bid-ask. Study their win rate by category and entry timing "
            "relative to kickoff / resolution."
        )
    lines.append("")

    # Category
    lines.append("## Where the money comes from")
    lines.append("")
    for cat, val in list((cats.get("pnl") or {}).items())[:8]:
        n = (cats.get("counts") or {}).get(cat, 0)
        lines.append(f"- **{cat}**: {_fmt_money(val)} across {n} closed legs")
    lines.append("")

    # Timing & sizing
    lines.append("## Timing")
    lines.append("")
    peak_hours = timing.get("peak_hours") or []
    lines.append(f"- Peak UTC hours: {', '.join(str(h) for h in peak_hours)}")
    lines.append(f"- Peak weekdays (0=Mon): {timing.get('peak_dows')}")
    if metrics.get("median_gap_seconds") is not None:
        lines.append(f"- Median inter-trade gap: {_fmt_secs(metrics['median_gap_seconds'])}")
    lines.append("")
    lines.append("## Sizing")
    lines.append("")
    if sizing:
        lines.append(
            f"- Median ticket {_fmt_money(sizing.get('median_usdc') or 0)}, "
            f"mean {_fmt_money(sizing.get('mean_usdc') or 0)}, "
            f"p90 {_fmt_money(sizing.get('p90_usdc') or 0)}, "
            f"max {_fmt_money(sizing.get('max_usdc') or 0)}"
        )
        lines.append(
            f"- Share size median {sizing.get('median_shares')}, mean {sizing.get('mean_shares')}"
        )
    lines.append("")

    # Trade-by-trade style vignettes
    lines.append("## Trade-by-trade pattern (representative winners)")
    lines.append("")
    lines.append(
        "These vignettes are reconstructed from fills: average entry, average exit, "
        "hold time, and closed realized PnL."
    )
    lines.append("")
    for v in summary.get("strategy_vignettes") or []:
        lines.append(f"### {v['title']}")
        lines.append(
            f"- Entries ≈ **{v['avg_buy']:.3f}** · Exits ≈ **{v['avg_sell']:.3f}** · "
            f"Spread ≈ **{v['spread']:.3f}**"
        )
        lines.append(
            f"- Fills: {v['n_buys']} buys / {v['n_sells']} sells · hold {_fmt_secs(v['hold_seconds'])} · "
            f"both-sides={v['both_sides']} · realized {_fmt_money(v['pnl'])}"
        )
        lines.append("")

    lines.append("## Top closed winners / losers")
    lines.append("")
    lines.append("**Winners**")
    for t in summary.get("top_wins") or []:
        lines.append(
            f"- {t['title']}: {_fmt_money(t['pnl'])} · bought {_fmt_money(t['buy_usdc'])} · "
            f"sold {_fmt_money(t['sell_usdc'])} · hold {_fmt_secs(t.get('hold_seconds'))}"
        )
    lines.append("")
    lines.append("**Losers**")
    for t in summary.get("top_losses") or []:
        lines.append(
            f"- {t['title']}: {_fmt_money(t['pnl'])} · bought {_fmt_money(t['buy_usdc'])} · "
            f"sold {_fmt_money(t['sell_usdc'])}"
        )
    lines.append("")

    # Replication playbook
    lines.append("## Replication playbook (how to copy the edge)")
    lines.append("")
    if mm["score"] >= 45:
        lines.append("1. **Universe:** Focus on liquid sports match + totals (O/U) markets with tight books.")
        lines.append("2. **Role:** Quote or take both sides near mid; prioritize markets you can exit before resolution.")
        lines.append(
            f"3. **Sizing:** Start near their median ticket (~{_fmt_money(sizing.get('median_usdc') or 0)}) and scale only with inventory limits."
        )
        lines.append("4. **Inventory:** Cap net Yes/No (or Over/Under) imbalance; flatten when mid moves through you.")
        lines.append("5. **Hold time:** Target minutes–hours, not overnight directional risk, unless hedged via opposite outcome.")
        lines.append("6. **Edge source:** Capture spread + mean reversion after flow, not oracle forecasting alpha.")
        lines.append("7. **Ops:** Automate via CLOB maker orders; track maker rebates; kill-switch on drawdown.")
        lines.append(
            "8. **Do not blindly copy:** Their edge depends on latency, fee tier, and bankroll. Replicate *mechanics*, not wallet follows."
        )
    else:
        lines.append("1. Restrict to their top categories by PnL contribution.")
        lines.append("2. Mirror entry price percentiles and hold-time distribution rather than exact fills.")
        lines.append("3. Enforce risk: their profit factor and max DD define a hard stop template.")
        lines.append("4. Recompute weekly — edges decay when others copy the same tape.")
    lines.append("")

    detail = pnl.get("cashflow_detail") or {}
    lines.append("## Cashflow anatomy")
    lines.append("")
    lines.append(f"- Buys: {_fmt_money(detail.get('buys_usdc') or 0)}")
    lines.append(f"- Sells: {_fmt_money(detail.get('sells_usdc') or 0)}")
    lines.append(f"- Redeems: {_fmt_money(detail.get('redeems_usdc') or 0)}")
    lines.append(f"- Maker rebates: {_fmt_money(detail.get('maker_rebates_usdc') or 0)}")
    lines.append(f"- Taker rebates: {_fmt_money(detail.get('taker_rebates_usdc') or 0)}")
    lines.append("")
    lines.append(f"_Generated {datetime.now(timezone.utc).isoformat()}_")
    lines.append("")
    return "\n".join(lines)
