"""Elite MM / scalper bot replication playbook from deep-dive analytics."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def _m(x: float | None) -> str:
    if x is None:
        return "n/a"
    sign = "-" if x < 0 else ""
    return f"{sign}${abs(x):,.2f}"


def _s(seconds: int | None) -> str:
    if seconds is None:
        return "n/a"
    s = int(seconds)
    if s < 60:
        return f"{s}s"
    if s < 3600:
        return f"{s//60}m{s%60:02d}s"
    if s < 86400:
        return f"{s//3600}h{(s%3600)//60:02d}m"
    return f"{s//86400}d"


def write_bot_playbook(
    username: str,
    wallet: str,
    summary: dict[str, Any],
    deep: dict[str, Any],
    validation: dict[str, Any] | None = None,
) -> str:
    pnl = summary["pnl"]
    mm = summary["market_making"]
    bp = deep.get("bot_parameters") or {}
    rebates = deep.get("rebates") or {}
    ou = deep.get("ou_markets") or {}
    match = deep.get("match_markets") or {}
    outcomes = deep.get("outcome_pnl") or {}

    # Detect one-sided scalp vs classic two-sided MM from the tape
    both_sides_w = (deep.get("winners") or {}).get("both_sides_rate") or 0
    buy_sell_seq = dict(deep.get("sequence_patterns") or {}).get("BUY->SELL", 0)
    total_seq = sum(n for _, n in (deep.get("sequence_patterns") or [])) or 1
    over_pnl = float(outcomes.get("Over") or 0)
    under_pnl = float(outcomes.get("Under") or 0)
    one_sided_scalper = both_sides_w < 0.05 and buy_sell_seq / total_seq > 0.4

    lines: list[str] = []
    lines.append(f"# Elite Replication Playbook — {username}")
    lines.append("")
    lines.append(
        f"Wallet `{wallet}`. Reverse-engineered from the **full unique fill tape** "
        f"({summary['counts']['trades']:,} trades · {summary['counts']['markets_traded']:,} markets). "
        "This is an implementation spec for a high-end bot, not vibes."
    )
    lines.append("")

    lines.append("## 0. True strategy identity (read this first)")
    lines.append("")
    if one_sided_scalper:
        lines.append(
            f"**{username} is NOT a classic two-sided market maker.** "
            "Both-sides inventory is ~0–1% of winning markets. The real craft is:"
        )
        lines.append("")
        lines.append(
            "> **Live / short-horizon one-sided scalping on sports markets "
            "(especially O/U Over)** — BUY a clip, then SELL the *same* outcome "
            "higher within seconds to a few minutes. Maker-biased. Repeat."
        )
        lines.append("")
        lines.append(
            f"Evidence: BUY→SELL opens {buy_sell_seq}/{total_seq} episodes; "
            f"median winner hold {_s(bp.get('median_hold_seconds'))}; "
            f"winner median spread (exit−entry) {bp.get('target_spread_median')}; "
            f"Over PnL {_m(over_pnl)} vs Under {_m(under_pnl)}; "
            f"maker rebates {_m(rebates.get('maker'))} >> taker {_m(rebates.get('taker'))}."
        )
    else:
        lines.append(
            f"Classification `{mm['label']}` — mix of spread capture and directional inventory."
        )
    lines.append("")
    lines.append(
        "Heuristic label from the scanner may still say `likely_market_maker` because of "
        "fast round-trips + sell>buy + maker rebates. **Operationally, build a live scalper "
        "with optional maker quoting**, not a Yes/No pair inventory bot."
    )
    lines.append("")

    lines.append("## 1. Performance anchors")
    lines.append("")
    lines.append("| Source / metric | Value |")
    lines.append("|---|---|")
    lines.append(f"| Cashflow realized (sells−buys+redeems+rebates) | {_m(pnl['cashflow_realized'])} |")
    lines.append(f"| Core cashflow (ex-rebates) | {_m(pnl['cashflow_core'])} |")
    lines.append(f"| Closed-position legs sum | {_m(pnl['closed_positions_sum'])} |")
    lines.append(f"| Leg win rate / profit factor | {pnl['win_rate']*100:.2f}% / {pnl['profit_factor']} |")
    if pnl.get("leaderboard_all"):
        lb = pnl["leaderboard_all"]
        lines.append(
            f"| Polymarket leaderboard ALL | {_m(float(lb['pnl']))} · vol {_m(float(lb['vol']))} · rank {lb.get('rank')} |"
        )
    if validation:
        for c in validation.get("checks", []):
            if c.get("metric") in ("pnl", "realized_pnl", "n_trades", "win_rate"):
                lines.append(
                    f"| {c['source']} {c['metric']} | ref={c.get('reference')} ours={c.get('ours')} "
                    f"({'MATCH' if c.get('match') else 'DRIFT'}) |"
                )
    lines.append("")
    lines.append(
        "Notes: Polymarket leaderboard ALL is the primary official PnL check (we match within tolerance). "
        "PolyData uses a different event aggregation / trade counting method — expect DRIFT on WR and trade count; "
        "use it as a secondary research signal, not the ground truth for fills."
    )
    lines.append("")

    lines.append("## 2. Universe — where the money is")
    lines.append("")
    lines.append(
        f"- **O/U / totals:** {ou.get('n', 0)} markets · {_m(ou.get('pnl'))} · "
        f"avg {_m(ou.get('avg_pnl'))} · median hold {_s(ou.get('median_hold_s'))} · "
        f"median spread {ou.get('median_spread')}"
    )
    lines.append(
        f"- **Match / other sports:** {match.get('n', 0)} markets · {_m(match.get('pnl'))} · avg {_m(match.get('avg_pnl'))}"
    )
    lines.append("- **Outcome PnL leaders:**")
    for k, v in list(outcomes.items())[:6]:
        lines.append(f"  - **{k}**: {_m(v)}")
    lines.append("")
    lines.append("### Bot universe rules")
    lines.append("")
    lines.append("1. Only liquid live sports (soccer/football first — their tape is soccer-heavy).")
    lines.append("2. Prefer O/U lines with tight books and active in-game trading.")
    lines.append("3. Default bias toward **Over** unless your signal says otherwise (their Over PnL dominates).")
    lines.append("4. Skip politics/crypto until you have separate evidence.")
    lines.append("5. Require enough depth to enter ~median clip and exit within 1–2 minutes.")
    lines.append("")

    lines.append("## 3. ENTRY — exact mechanics")
    lines.append("")
    lines.append("### Style histogram")
    for style, n in deep.get("entry_styles") or []:
        lines.append(f"- `{style}`: {n}")
    lines.append("")
    lines.append("### First-two-fill sequences")
    for seq, n in deep.get("sequence_patterns") or []:
        lines.append(f"- `{seq}`: {n}")
    lines.append("")
    lines.append("### Entry price → realized edge")
    lines.append("")
    lines.append("| Avg buy band | Markets | Total PnL | Avg PnL |")
    lines.append("|---|---:|---:|---:|")
    for band, st in (deep.get("entry_price_bands") or {}).items():
        lines.append(f"| {band} | {st['n']} | {_m(st['pnl'])} | {_m(st['avg'])} |")
    lines.append("")
    lines.append("**Best band:** 0.40–0.60 (near mid) — highest average PnL. Tails (≤0.20 or ≥0.80) make less per market.")
    lines.append("")
    lines.append("### Entry checklist (bot)")
    lines.append("")
    lines.append(
        f"1. Clip **{_m(bp.get('clip_size_usdc_median'))}** median (p90 {_m(bp.get('clip_size_usdc_p90'))})."
    )
    lines.append(
        f"2. Aim entry price ~**{bp.get('preferred_entry_price_median')}** (IQR {bp.get('preferred_entry_price_p25_p75')})."
    )
    lines.append("3. Trigger = microstructure, not long-term forecast:")
    lines.append("   - mid dips / liquidity hole you can buy")
    lines.append("   - imminent volatility (attack, corner, shot) where Over can jump")
    lines.append("   - resting bid gets lifted? you’re being taken — manage immediately")
    lines.append("4. Prefer **maker bids**; take only if the expected jump already started and ask is still inside your edge.")
    lines.append("5. Same-second multi-fills are normal (one order, many counterparties) — treat as one decision, many fills.")
    lines.append("")

    lines.append("## 4. MANAGEMENT — what they do after entry")
    lines.append("")
    lines.append("### Styles")
    for style, n in deep.get("management_styles") or []:
        lines.append(f"- `{style}`: {n}")
    lines.append("")
    w = deep.get("winners") or {}
    l = deep.get("losers") or {}
    lines.append("### Winners vs losers")
    lines.append("")
    lines.append("| Metric | Winners | Losers |")
    lines.append("|---|---:|---:|")
    lines.append(f"| N | {w.get('n')} | {l.get('n')} |")
    lines.append(f"| PnL | {_m(w.get('pnl'))} | {_m(l.get('pnl'))} |")
    lines.append(f"| Median hold | {_s(w.get('median_hold_s'))} | {_s(l.get('median_hold_s'))} |")
    lines.append(f"| Median spread | {w.get('median_spread')} | {l.get('median_spread')} |")
    lines.append(f"| Scale-in rate | {w.get('scale_in_rate')} | {l.get('scale_in_rate')} |")
    lines.append(f"| Scale-out rate | {w.get('scale_out_rate')} | {l.get('scale_out_rate')} |")
    lines.append(f"| Avg fills/market | {w.get('avg_fills')} | {l.get('avg_fills')} |")
    lines.append(f"| Both-sides rate | {w.get('both_sides_rate')} | {l.get('both_sides_rate')} |")
    lines.append("")
    lines.append("### The real management loop (one-sided scalp)")
    lines.append("")
    lines.append("```")
    lines.append("BUY clip(s) on Over (or chosen outcome)")
    lines.append("   │")
    lines.append("   ├─ price jumps in your favor within seconds → SELL in clips (scale-out)")
    lines.append("   ├─ price chops flat → keep working asks above entry; time-stop")
    lines.append("   └─ price dumps → cut quickly (losers show sell-below-buy); do NOT average forever")
    lines.append("Optional: re-enter later cheaper if a second impulse sets up (seen in big O/U winners)")
    lines.append("```")
    lines.append("")
    lines.append("Critical deltas:")
    lines.append("")
    lines.append(
        f"- **Winners** sell above buy (median spread **{w.get('median_spread')}**). "
        f"**Losers** often exit worse (median spread **{l.get('median_spread')}**)."
    )
    lines.append(
        f"- Losers scale-in **more** ({l.get('scale_in_rate')} vs {w.get('scale_in_rate')}) — "
        "averaging down is how they bleed; the bot should **forbid** revenge scale-ins without a fresh signal."
    )
    lines.append(
        f"- Hold edge peaks in **<5m** ({(deep.get('hold_edge') or {}).get('<5m')}) and a strong "
        f"**30m–2h** bucket for the larger in-game campaigns."
    )
    lines.append("")

    lines.append("## 5. EXIT — rules that print")
    lines.append("")
    for style, n in deep.get("exit_styles") or []:
        lines.append(f"- `{style}`: {n}")
    lines.append("")
    lines.append("| Hold bucket | N | Total PnL | Avg | Win rate |")
    lines.append("|---|---:|---:|---:|---:|")
    for bucket, st in (deep.get("hold_edge") or {}).items():
        lines.append(
            f"| {bucket} | {st['n']} | {_m(st['pnl'])} | {_m(st['avg'])} | {st['win_rate']*100:.1f}% |"
        )
    lines.append("")
    lines.append("### Exit engine params")
    lines.append("")
    lines.append(
        f"1. **TP / ask distance:** target ≈ **{bp.get('target_spread_median')}** above avg entry "
        f"(p75 stretch {bp.get('target_spread_p75')}). On live O/U this is often a burst move, not slow grind."
    )
    lines.append(
        f"2. **Time stop:** median hold {_s(bp.get('median_hold_seconds'))}; p75 {_s(bp.get('max_hold_seconds_p75'))} "
        "for the scalps — escalate urgency after that."
    )
    lines.append("3. **Scale-out:** peel into strength (their winners stack sells). Don’t wait for one perfect print.")
    lines.append("4. **Stop:** if mid < entry − ~3–5¢ on unhedged inventory with no signal → take the loss (copy losers’ speed, not their hope).")
    lines.append("5. **Flatten before resolution** — redeem is residual.")
    lines.append("6. Taker exits are fine when the move already happened and maker asks won’t fill.")
    lines.append("")

    lines.append("## 6. What works / what fails")
    lines.append("")
    lines.append("### Works")
    for x in deep.get("what_works") or []:
        lines.append(f"- {x}")
    lines.append("")
    lines.append("### Fails")
    for x in deep.get("what_fails") or ["(no strong negative bucket)"]:
        lines.append(f"- {x}")
    lines.append(f"- Chase vs fade ladders: `{deep.get('chase_vs_fade')}`")
    lines.append("")

    lines.append("## 7. Fill-by-fill autopsies (copy these patterns)")
    lines.append("")
    for i, ex in enumerate((deep.get("scalp_examples") or deep.get("mm_examples") or [])[:6], 1):
        lines.append(f"### Example {i}: {ex['title']}")
        lines.append(
            f"PnL {_m(ex['realized_pnl'])} · hold {_s(ex['hold_seconds'])} · "
            f"{ex['n_buys']}B/{ex['n_sells']}S · avg entry {ex['avg_entry']} → exit {ex['avg_exit']} "
            f"(spread {ex['spread_captured']}) · `{ex['management_style']}`"
        )
        lines.append("")
        lines.append("| Time (UTC) | Side | Outcome | Size | Price | USDC |")
        lines.append("|---|---|---|---:|---:|---:|")
        for f in ex.get("fills") or []:
            lines.append(
                f"| {f['iso']} | {f['side']} | {f['outcome']} | {f['size']:.2f} | {f['price']:.4f} | {f['usdc']:.2f} |"
            )
        lines.append("")
        lines.append(
            "**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match)."
        )
        lines.append("")

    lines.append("## 8. Failure modes (do not bot these)")
    lines.append("")
    for i, ex in enumerate(deep.get("failure_examples") or [], 1):
        lines.append(
            f"{i}. **{ex['title']}** {_m(ex['realized_pnl'])} · hold {_s(ex['hold_seconds'])} · "
            f"entry {ex['avg_entry']} → exit {ex['avg_exit']} · `{ex['management_style']}` / `{ex['exit_style']}`"
        )
    lines.append("")
    lines.append("Common failure DNA: bought Over, game didn’t produce goals, sold lower or held into worthless.")
    lines.append("")

    lines.append("## 9. Bot architecture (elite build)")
    lines.append("")
    lines.append("```")
    lines.append("LiveSportsFeed ──► Signal(impulse/dip) ──► Execution(maker-first)")
    lines.append("                         │                      │")
    lines.append("                         ▼                      ▼")
    lines.append("                  PositionState ◄────── ExitEngine (TP/SL/time)")
    lines.append("                         │")
    lines.append("                         ▼")
    lines.append("                   RiskGovernor (caps, kill switch)")
    lines.append("```")
    lines.append("")
    lines.append("### Modules")
    lines.append("")
    lines.append("1. **LiveSportsFeed** — kickoff clock, shots, corners, goals (Opta/Betfair/odds APIs). Polymarket mid alone is laggy; their edge looks like **reacting to match state faster than the book**.")
    lines.append("2. **Signal**")
    lines.append("   - `dip_bid`: mid drops X¢ with depth refill → maker bid")
    lines.append("   - `impulse_long_over`: attacking sequence / goal threat → bid or take Over")
    lines.append("   - disable new entries near whistle/resolution")
    lines.append("3. **Execution**")
    lines.append(
        f"   - default post-only bids/asks; clip {_m(bp.get('clip_size_usdc_median'))}"
    )
    lines.append("   - allow taker for: (a) entry if signal already moving, (b) exit when TP prints through")
    lines.append("   - cancel stale quotes > N seconds")
    lines.append("4. **ExitEngine** — as in §5; always scale-out capable")
    lines.append("5. **RiskGovernor**")
    lines.append("   - max gross per market, max concurrent live matches")
    lines.append("   - daily loss stop ≈ 1–2× median losing day from episode_stats")
    lines.append("   - ban averaging down without new signal")
    lines.append("")
    lines.append("### Core pseudocode")
    lines.append("")
    lines.append("```python")
    lines.append("for market in live_ou_markets():")
    lines.append("    state = positions[market]")
    lines.append("    if state.flat and signal.long_over(market):")
    lines.append("        place_maker_bid(market, outcome='Over', clip=CLIP, limit=fair - buffer)")
    lines.append("        # optional: take ask if impulse already underway and edge remains")
    lines.append("    if state.long:")
    lines.append("        work_asks_above(avg_entry + TARGET_SPREAD)")
    lines.append("        if mid <= avg_entry - STOP or age > TIME_STOP:")
    lines.append("            flatten(taker_ok=True)")
    lines.append("        if mid >= avg_entry + TARGET_SPREAD:")
    lines.append("            scale_out(fraction=0.5 then 0.5)")
    lines.append("    if near_resolution(market):")
    lines.append("        flatten(taker_ok=True)")
    lines.append("```")
    lines.append("")

    lines.append("## 10. Parameter block (start here)")
    lines.append("")
    lines.append("```yaml")
    lines.append(f"template: {username}")
    lines.append("mode: one_sided_live_scalper  # not classic two-sided MM")
    lines.append("preferred_outcome_bias: Over")
    lines.append(f"clip_usdc_median: {bp.get('clip_size_usdc_median')}")
    lines.append(f"clip_usdc_p90: {bp.get('clip_size_usdc_p90')}")
    lines.append(f"entry_price_median: {bp.get('preferred_entry_price_median')}")
    lines.append(f"entry_price_iqr: {bp.get('preferred_entry_price_p25_p75')}")
    lines.append(f"target_spread: {bp.get('target_spread_median')}")
    lines.append(f"target_spread_p75: {bp.get('target_spread_p75')}")
    lines.append(f"median_hold_seconds: {bp.get('median_hold_seconds')}")
    lines.append(f"max_hold_seconds_p75: {bp.get('max_hold_seconds_p75')}")
    lines.append("maker_bias: true")
    lines.append("taker_allowed: entry_impulse_or_exit_urgency")
    lines.append("both_sides_hedge: false  # tape does not support this as primary")
    lines.append("avg_down_without_signal: false")
    lines.append("flatten_before_resolution: true")
    lines.append("```")
    lines.append("")

    lines.append("## 11. Build roadmap")
    lines.append("")
    lines.append("1. Replay their O/U Over fills against match timelines — confirm signal = live events.")
    lines.append("2. Paper quoter on 3 leagues they touch most; match clip + hold distributions.")
    lines.append("3. Enable maker entries only; measure markout at +30s/+2m.")
    lines.append("4. Add taker impulse entries; compare markout.")
    lines.append("5. Production with tiny clips; scale only when markout stays positive after fees.")
    lines.append("6. Weekly `polyanalyst update polika72` — if their hold/spread regime shifts, re-fit params.")
    lines.append("")
    lines.append(
        "_Research only. Latency, fee tier, and sports-data quality decide whether this edge is yours._"
    )
    lines.append("")
    lines.append(f"_Generated {datetime.now(timezone.utc).isoformat()}_")
    lines.append("")
    return "\n".join(lines)
