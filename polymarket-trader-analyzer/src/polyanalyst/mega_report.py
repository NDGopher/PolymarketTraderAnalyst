"""Generate one massive MASTER report per trader (human + machine readable)."""

from __future__ import annotations

import csv
import json
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .autopsy import fetch_taker_keys, run_autopsy
from .deep_dive import build_episodes
from .pipeline import AnalyzerApp
from .validate import fetch_polydata_snapshot


def _m(x) -> str:
    if x is None:
        return "n/a"
    try:
        x = float(x)
    except Exception:
        return str(x)
    sign = "-" if x < 0 else ""
    return f"{sign}${abs(x):,.2f}"


def _pct(x) -> str:
    if x is None:
        return "n/a"
    return f"{100*float(x):.2f}%"


def generate_master(app: AnalyzerApp, username: str, wallet: str | None = None) -> Path:
    """Build MASTER.md + MASTER.json + equity_curve.csv under samples/<user>/."""
    # Resolve wallet from store/traders table or reports
    store = app.store
    if not wallet:
        rows = store.list_traders()
        match = next((r for r in rows if (r.get("username") or "").lower() == username.lower()), None)
        if match:
            wallet = match["wallet"]
        else:
            # try samples stats
            p = app.reports_dir / username / "stats.json"
            if p.exists():
                wallet = json.loads(p.read_text())["wallet"]
            else:
                resolved = app.client.resolve_trader(username)
                wallet = resolved["wallet"]
                username = resolved["username"]

    wallet = wallet.lower()
    activity = store.load_activity(wallet)
    trades = store.load_trades(wallet)
    closed = store.load_closed_positions(wallet)
    opened = store.load_open_positions(wallet)
    if not trades and not activity:
        raise RuntimeError(f"No synced data for {username}. Run autopsy first.")

    leaderboard = app.client.leaderboard_entry(wallet, "ALL")
    polydata = fetch_polydata_snapshot(username)

    # Load or fetch taker keys
    cache = app.reports_dir / username / "taker_keys.json"
    taker_keys = set(json.loads(cache.read_text())) if cache.exists() else None
    if taker_keys is None and trades:
        start_ts = min(int(t.get("timestamp") or 0) for t in trades)
        end_ts = max(int(t.get("timestamp") or 0) for t in trades) + 1
        taker_keys = fetch_taker_keys(app.client, wallet, start_ts, end_ts)
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps(list(taker_keys)))

    # polika bench from sample
    bench = {
        "identity": "one_sided_informed_scalper",
        "trades": 19978,
        "cashflow_pnl": 58204.98,
        "win_rate": 0.8008,
        "entry_taker_pct": 61.6,
        "both_sides_rate": 0.008,
        "median_clip": 11.29,
        "campaign_pct": 5.85,
        "max_dd": None,
        "time_to_mfe_med": 64,
    }
    ps = app.reports_dir / "polika72" / "summary.json"
    if ps.exists():
        s = json.loads(ps.read_text())
        bench.update(
            {
                "trades": s.get("counts", {}).get("trades"),
                "cashflow_pnl": s.get("pnl", {}).get("cashflow_realized"),
                "win_rate": s.get("pnl", {}).get("win_rate"),
                "max_dd": s.get("equity", {}).get("max_drawdown"),
            }
        )
    # also additional breakdown / stats if present
    pstats = app.reports_dir / "polika72" / "stats.json"
    if pstats.exists():
        st = json.loads(pstats.read_text())
        bench["identity"] = st.get("identity", bench["identity"])
        if st.get("maker_taker", {}).get("entry"):
            bench["entry_taker_pct"] = st["maker_taker"]["entry"].get("taker_pct")
        bench["both_sides_rate"] = (st.get("both_sides") or {}).get("rate", bench["both_sides_rate"])
        bench["campaign_pct"] = (st.get("campaigns") or {}).get("pct", bench["campaign_pct"])
        bench["time_to_mfe_med"] = (st.get("latency") or {}).get("time_to_mfe_median", bench["time_to_mfe_med"])
        if st.get("equity"):
            bench["max_dd"] = st["equity"].get("max_drawdown", bench["max_dd"])

    from .autopsy import run_autopsy

    result = run_autopsy(
        username=username,
        wallet=wallet,
        activity=activity,
        trades=trades,
        closed=closed,
        open_positions=opened,
        leaderboard=leaderboard,
        polydata=polydata,
        taker_keys=taker_keys,
        polika_benchmark=bench,
    )
    stats = result["stats"]
    summary = result["summary"]
    deep = result["deep"]
    validation = result["validation"]
    eps = build_episodes(trades, closed)

    # Extra metrics pack
    extras = _extra_metrics(trades, activity, closed, opened, eps, stats, deep)
    closed_equity = _closed_daily_equity(closed)
    preferred = _preferred_pnl(summary, validation, leaderboard)

    master_json = {
        "meta": {
            "username": username,
            "wallet": wallet,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "schema_version": "1.1",
            "purpose": "human+bot consumable master autopsy",
        },
        "reconciliation": {
            "preferred_pnl": preferred,
            "ours": {
                "cashflow_realized": summary["pnl"]["cashflow_realized"],
                "cashflow_core": summary["pnl"]["cashflow_core"],
                "closed_positions_sum": summary["pnl"]["closed_positions_sum"],
                "trades": summary["counts"]["trades"],
                "buys": summary["counts"]["buys"],
                "sells": summary["counts"]["sells"],
                "win_rate_legs": summary["pnl"]["win_rate"],
                "profit_factor": summary["pnl"]["profit_factor"],
                "volume_proxy_buy_plus_sell": round(
                    summary["pnl"]["cashflow_detail"]["buys_usdc"] + summary["pnl"]["cashflow_detail"]["sells_usdc"],
                    2,
                ),
                "note_buy_only": summary["counts"]["sells"] == 0,
            },
            "polymarket_leaderboard_ALL": leaderboard,
            "polydata": polydata,
            "validation": validation,
        },
        "identity": {
            "class": stats["identity"],
            "mm_scanner": stats["market_making"],
            "sport_focus": stats["sport_focus"],
            "both_sides": stats["both_sides"],
            "maker_taker": stats["maker_taker"],
            "clip_size_usdc": stats["clip_size_usdc"],
        },
        "performance": {
            "pnl": summary["pnl"],
            "counts": summary["counts"],
            "span": summary["span"],
            "hold_time": stats["hold_time"],
            "entry_price_band": stats["entry_price_band"],
            "family": stats["family"],
            "equity": stats["equity"],
            "contribution": stats["contribution"],
            "risk": stats["risk"],
            "latency": stats["latency"],
            "campaigns": stats["campaigns"],
            "adverse_management": stats["adverse_management"],
            "favorable_management": stats["favorable_management"],
            "avg_down": stats["avg_down"],
            "resolution_behavior": stats["resolution_behavior"],
        },
        "extras": extras,
        "deep_dive_highlights": {
            "what_works": deep.get("what_works"),
            "what_fails": deep.get("what_fails"),
            "bot_parameters": deep.get("bot_parameters"),
            "rebates": deep.get("rebates"),
            "management_styles": deep.get("management_styles"),
            "entry_styles": deep.get("entry_styles"),
            "exit_styles": deep.get("exit_styles"),
            "mm_examples": deep.get("mm_examples", [])[:5],
            "scalp_examples": deep.get("scalp_examples", [])[:5],
            "failure_examples": deep.get("failure_examples", [])[:8],
        },
        "copyability": _copyability(stats, summary, deep, bench),
        "vs_polika72": stats.get("polika_benchmark"),
        "equity_curve_daily": stats["equity_curve_daily"],
        "equity_curve_closed_daily": closed_equity.get("curve", []),
        "equity_closed_summary": {k: v for k, v in closed_equity.items() if k != "curve"},
        "documents": {
            "autopsy_md_included": True,
            "strategy_md_included": True,
            "bot_playbook_md_included": True,
            "equity_curve_csv": "equity_curve.csv",
            "equity_curve_closed_csv": "equity_curve_closed.csv",
        },
    }

    md = _render_master_md(master_json, result["autopsy_md"], result["strategy_md"], result["bot_md"])

    out_data = app.reports_dir / username
    out_samples = Path(__file__).resolve().parents[2] / "samples" / username
    out_data.mkdir(parents=True, exist_ok=True)
    out_samples.mkdir(parents=True, exist_ok=True)

    # equity csv (cashflow + closed)
    for out in (out_data, out_samples):
        csv_path = out / "equity_curve.csv"
        with csv_path.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["date", "equity", "daily_pnl", "drawdown", "source"])
            w.writeheader()
            for row in stats["equity_curve_daily"]:
                w.writerow({**row, "source": "cashflow_activity"})
        closed_csv = out / "equity_curve_closed.csv"
        with closed_csv.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["date", "equity", "daily_pnl", "drawdown", "source"])
            w.writeheader()
            for row in closed_equity.get("curve", []):
                w.writerow({**row, "source": "closed_positions"})
        (out / "MASTER.json").write_text(json.dumps(master_json, indent=2))
        (out / "MASTER.md").write_text(md)
        # also refresh component files
        (out / "autopsy.md").write_text(result["autopsy_md"])
        (out / "strategy.md").write_text(result["strategy_md"])
        (out / "bot_playbook.md").write_text(result["bot_md"])
        (out / "stats.json").write_text(
            json.dumps({k: v for k, v in stats.items() if k not in ("equity_curve_daily", "deep")}, indent=2)
        )
        (out / "validation.json").write_text(json.dumps(validation, indent=2))
        (out / "equity_curve.json").write_text(json.dumps(stats["equity_curve_daily"], indent=2))
        (out / "equity_curve_closed.json").write_text(json.dumps(closed_equity.get("curve", []), indent=2))
        (out / "summary.json").write_text(
            json.dumps({k: v for k, v in summary.items() if k != "markets"}, indent=2)
        )

    return out_samples / "MASTER.md"


def _preferred_pnl(summary: dict, validation: dict, leaderboard: dict | None) -> dict[str, Any]:
    """Pick the PnL number closest to Polymarket leaderboard ALL (ground truth)."""
    lb = float((leaderboard or {}).get("pnl") or 0)
    candidates = {
        "cashflow_realized": float(summary["pnl"]["cashflow_realized"]),
        "cashflow_core": float(summary["pnl"]["cashflow_core"]),
        "closed_positions_sum": float(summary["pnl"]["closed_positions_sum"]),
    }
    best_name, best_val = min(candidates.items(), key=lambda kv: abs(kv[1] - lb)) if leaderboard else ("cashflow_realized", candidates["cashflow_realized"])
    check = next((c for c in (validation.get("checks") or []) if c.get("source") == "polymarket_leaderboard_ALL"), None)
    return {
        "field": best_name if not check else check.get("ours_field", best_name),
        "value": best_val if not check else check.get("ours", best_val),
        "leaderboard_all": lb if leaderboard else None,
        "match": bool(check and check.get("match")),
        "note": (
            "For buy-only / merge-redeem traders, cashflow equity can look deeply negative "
            "while closed-legs + leaderboard show true realized edge."
            if summary["counts"].get("sells", 1) == 0
            else "Cashflow usually tracks leaderboard for buy+sell scalpers."
        ),
    }


def _closed_daily_equity(closed: list[dict]) -> dict[str, Any]:
    """Cumulative realized PnL by closed-position timestamp (alt equity for buy-only books)."""
    from collections import defaultdict

    by_day: dict[str, float] = defaultdict(float)
    for p in closed:
        ts = int(p.get("timestamp") or 0)
        if not ts:
            continue
        day = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
        by_day[day] += float(p.get("realizedPnl") or p.get("realized_pnl") or 0)
    curve = []
    eq = peak = 0.0
    max_dd = 0.0
    for day in sorted(by_day):
        eq += by_day[day]
        peak = max(peak, eq)
        dd = eq - peak
        max_dd = min(max_dd, dd)
        curve.append(
            {
                "date": day,
                "equity": round(eq, 4),
                "daily_pnl": round(by_day[day], 4),
                "drawdown": round(dd, 4),
            }
        )
    daily = [p["daily_pnl"] for p in curve]
    sharpe = None
    if len(daily) >= 5 and statistics.pstdev(daily) > 0:
        sharpe = (statistics.mean(daily) / statistics.pstdev(daily)) * (365 ** 0.5)
    return {
        "curve": curve,
        "final": curve[-1]["equity"] if curve else 0.0,
        "max_drawdown": round(max_dd, 4),
        "daily_sharpe_ann": round(sharpe, 3) if sharpe is not None else None,
        "n_days": len(curve),
    }


def _extra_metrics(trades, activity, closed, opened, eps, stats, deep) -> dict[str, Any]:
    buys = [t for t in trades if (t.get("side") or "").upper() == "BUY"]
    sells = [t for t in trades if (t.get("side") or "").upper() == "SELL"]
    buy_px = [float(t["price"]) for t in buys if t.get("price") is not None]
    sell_px = [float(t["price"]) for t in sells if t.get("price") is not None]
    notionals = [float(t.get("size") or 0) * float(t.get("price") or 0) for t in trades]
    notionals = [n for n in notionals if n > 0]

    # Hour / DOW from deep timing already in summary — recompute volume by hour
    from collections import Counter, defaultdict
    from datetime import datetime, timezone

    hour_usdc = defaultdict(float)
    dow_usdc = defaultdict(float)
    for t in trades:
        ts = int(t.get("timestamp") or 0)
        if not ts:
            continue
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        u = float(t.get("size") or 0) * float(t.get("price") or 0)
        hour_usdc[dt.hour] += u
        dow_usdc[dt.weekday()] += u

    # Expectancy
    pnls = [e.realized_pnl for e in eps]
    wins = [p for p in pnls if p > 0]
    losses = [p for p in pnls if p < 0]
    wr = len(wins) / max(1, len(wins) + len(losses))
    avg_w = statistics.mean(wins) if wins else 0
    avg_l = statistics.mean(losses) if losses else 0
    expectancy = wr * avg_w + (1 - wr) * avg_l

    # Concentration HHI of market PnL
    abs_pnls = [abs(e.realized_pnl) for e in eps if abs(e.realized_pnl) > 1e-9]
    total_abs = sum(abs_pnls) or 1
    shares = [p / total_abs for p in abs_pnls]
    hhi = sum(s * s for s in shares)

    # Activity type mix
    types = Counter((a.get("type") or "") for a in activity)

    # Open risk
    open_risk = {
        "n": len(opened),
        "cash_pnl": round(sum(float(p.get("cashPnl") or 0) for p in opened), 2),
        "current_value": round(sum(float(p.get("currentValue") or 0) for p in opened), 2),
        "redeemable": sum(1 for p in opened if p.get("redeemable")),
    }

    # Edge per day
    days = max(1, stats["span"].get("days_active_span") or 1)
    cashflow = stats["pnl"]["cashflow_realized"]

    return {
        "buy_price": {
            "mean": round(statistics.mean(buy_px), 4) if buy_px else None,
            "median": round(statistics.median(buy_px), 4) if buy_px else None,
            "p10": round(sorted(buy_px)[int(0.1 * (len(buy_px) - 1))], 4) if buy_px else None,
            "p90": round(sorted(buy_px)[int(0.9 * (len(buy_px) - 1))], 4) if buy_px else None,
        },
        "sell_price": {
            "mean": round(statistics.mean(sell_px), 4) if sell_px else None,
            "median": round(statistics.median(sell_px), 4) if sell_px else None,
        },
        "notional": {
            "mean": round(statistics.mean(notionals), 4) if notionals else None,
            "median": round(statistics.median(notionals), 4) if notionals else None,
            "p90": round(sorted(notionals)[int(0.9 * (len(notionals) - 1))], 4) if notionals else None,
            "sum": round(sum(notionals), 2) if notionals else 0,
        },
        "expectancy_per_market": round(expectancy, 4),
        "avg_win": round(avg_w, 4),
        "avg_loss": round(avg_l, 4),
        "win_loss_ratio": round(abs(avg_w / avg_l), 4) if avg_l else None,
        "pnl_concentration_hhi": round(hhi, 6),
        "pnl_per_day": round(cashflow / days, 2),
        "trades_per_day": round(len(trades) / days, 2),
        "markets_per_day": round(len(eps) / days, 2),
        "activity_type_counts": dict(types),
        "hour_volume_usdc_utc": {str(h): round(hour_usdc.get(h, 0), 2) for h in range(24)},
        "dow_volume_usdc_utc": {str(d): round(dow_usdc.get(d, 0), 2) for d in range(7)},
        "open_risk": open_risk,
        "start_side": {
            "buy_first": sum(1 for e in eps if e.fills and (e.fills[0].get("side") or "").upper() == "BUY"),
            "sell_first": sum(1 for e in eps if e.fills and (e.fills[0].get("side") or "").upper() == "SELL"),
        },
        "outcome_volume": _outcome_volume(trades),
    }


def _outcome_volume(trades):
    from collections import defaultdict

    buy = defaultdict(float)
    sell = defaultdict(float)
    for t in trades:
        oc = t.get("outcome") or "?"
        u = float(t.get("size") or 0) * float(t.get("price") or 0)
        if (t.get("side") or "").upper() == "BUY":
            buy[oc] += u
        else:
            sell[oc] += u
    keys = sorted(set(buy) | set(sell), key=lambda k: -(buy[k] + sell[k]))
    return {
        k: {"buy_usdc": round(buy[k], 2), "sell_usdc": round(sell[k], 2), "net_sell_minus_buy": round(sell[k] - buy[k], 2)}
        for k in keys[:20]
    }


def _copyability(stats, summary, deep, bench) -> dict[str, Any]:
    identity = stats["identity"]
    mt = stats["maker_taker"]
    entry_taker = (mt.get("entry") or {}).get("taker_pct") or 0
    entry_maker = (mt.get("entry") or {}).get("maker_pct") or 0
    both = stats["both_sides"]["rate"]
    buy_only = summary["counts"].get("sells", 1) == 0
    redeems = summary["pnl"]["cashflow_detail"].get("redeems_usdc") or 0
    merges = summary["pnl"]["cashflow_detail"].get("merges_usdc") or 0

    # Score difficulty 1-10 (10 = hardest to copy profitably)
    if identity == "one_sided_informed_scalper" and entry_taker >= 55:
        difficulty = 8
        why = "Requires live event latency + execution; pattern is clear but edge is speed/data."
        build = [
            "Live sports feed (goals/shots/xG / play-by-play)",
            "Taker entry on impulse + maker exit engine",
            "Universe filter: liquid O/U / match markets",
            "Markout kill-switch at +5s/+30s/+60s",
            "No avg-down without new event confirmation",
            "Size to clip median first; scale only after markout match",
        ]
    elif identity == "directional_hold_to_resolution" or (buy_only and redeems > 0 and both < 0.1):
        difficulty = 9
        why = (
            "Buy-and-hold / resolution harvesting at large notional. Easy mechanically "
            "(buy → wait → redeem) but edge is selection + bankroll + path risk, not a simple rule."
        )
        build = [
            "Build a directional edge model (not a tape-copy) for the same market universe",
            "Enter via maker when possible to cut fees; allow taker for urgency",
            "Exit primarily via REDEEM (and MERGE if pairing YES/NO) — no mid-market sell loop required",
            "Hard per-market and portfolio max inventory; expect multi-day underwater mark-to-market",
            "Paper the full hold-to-resolution cycle including open-risk volatility",
        ]
    elif identity == "two_sided_inventory_mm" or both >= 0.2:
        difficulty = 7 if not buy_only else 8
        why = (
            "Two-sided inventory MM DNA (often buy YES + buy NO then MERGE/REDEEM). "
            "Needs quoting/inventory stack; buy-only books exit via merge/redeem instead of sells."
            if buy_only
            else "Needs quoting stack, inventory skew, cancel/replace; closer to classic MM."
        )
        build = [
            "Two-sided quoter (or dual one-sided bids) with inventory caps on each outcome",
            "Skew toward informed mid / live event state",
            "Maker-first entries; taker only to flatten or complete a pair",
            "If buy-only: implement MERGE when holding complementary shares + REDEEM at resolution",
            "Per-market and portfolio risk limits; kill runaway inventory",
            "Match their median gap cadence and clip distribution before adding size",
        ]
    elif entry_maker >= 55:
        difficulty = 6
        why = "Maker-led entries reduce latency race; still needs solid risk + universe selection."
        build = [
            "Post-only bids in preferred price bands",
            "Work asks above entry for exits (or redeem path if applicable)",
            "Focus bands that print positive expectancy (see entry_price_band)",
            "Paper trade until markout distribution matches",
        ]
    else:
        difficulty = 7
        why = "Hybrid profile — cherry-pick modules after verifying markouts."
        build = [
            "Replicate hold-time bucket edge first",
            "Match clip size distribution",
            "Add maker/taker mix gradually",
            "Compare daily equity shape before scaling capital",
        ]

    ease = 11 - difficulty
    return {
        "difficulty_1_to_10": difficulty,
        "ease_of_copy_1_to_10": ease,
        "why": why,
        "build_steps": build,
        "exit_mechanics": (
            "merge_and_or_redeem_dominant"
            if buy_only and (merges > 0 or redeems > 0)
            else "sell_secondary_market"
        ),
        "bot_parameters": deep.get("bot_parameters"),
        "steal_from_them": _steal_list(stats, bench),
        "avoid": _avoid_list(stats),
        "kalshi_two_sided_mm_fit": _kalshi(stats),
    }


def _steal_list(stats, bench):
    out = []
    if stats["both_sides"]["rate"] > 0.15:
        out.append("Both-sides inventory discipline")
    if (stats["maker_taker"].get("entry") or {}).get("maker_pct", 0) >= 50:
        out.append("Maker-led entry style (better for quoting bots)")
    if stats["campaigns"]["pct"] > 8:
        out.append("Same-market campaign re-entries")
    if stats["latency"].get("pct_big_within_60s", 0) >= 40:
        out.append("Short-horizon impulse capture within ~60s")
    # best hold bucket
    ht = stats.get("hold_time") or {}
    if ht:
        best = max(ht.items(), key=lambda kv: (kv[1] or {}).get("total_pnl") or -1e18)
        out.append(f"Prioritize hold bucket {best[0]} (their PnL engine)")
    return out or ["Match clip sizing + preferred price bands first"]


def _avoid_list(stats):
    out = []
    if stats["avg_down"]["pct_losers"] > 5:
        out.append("Averaging down while red on losers")
    if abs(stats["equity"]["max_drawdown"]) > 50000:
        out.append("Their raw size/drawdown — scale down hard")
    if stats["identity"] == "directional_hold_to_resolution":
        out.append("Blind hold-to-resolution without edge model")
    top_loss_share = stats["contribution"].get("top10_losers_share_of_losses_pct") or 0
    if top_loss_share > 25:
        out.append("Fat left-tail single-market blowups — enforce per-market caps")
    return out or ["Don't copy size before matching markout distributions"]


def _kalshi(stats):
    if stats["both_sides"]["rate"] >= 0.2:
        return "HIGH — closest to two-sided informed MM DNA"
    if (stats["maker_taker"].get("entry") or {}).get("maker_pct", 0) >= 55:
        return "MEDIUM-HIGH — maker entries transfer well; add explicit both-sides module"
    if stats["identity"] == "one_sided_informed_scalper":
        return "MEDIUM — use as taker/impulse overlay on a Kalshi MM core, not as the core itself"
    return "MEDIUM — extract risk + hold rules; re-fit microstructure on Kalshi"


def _render_master_md(master: dict, autopsy_md: str, strategy_md: str, bot_md: str) -> str:
    u = master["meta"]["username"]
    perf = master["performance"]
    ident = master["identity"]
    recon = master["reconciliation"]
    copy = master["copyability"]
    extras = master["extras"]
    eq = perf["equity"]
    curve = master["equity_curve_daily"]

    lines = []
    lines.append(f"# MASTER AUTOPSY — {u}")
    lines.append("")
    lines.append("> Single file for humans **and** bots. Machine-readable twin: `MASTER.json` · Equity: `equity_curve.csv`.")
    lines.append("")
    lines.append(f"- Wallet: `{master['meta']['wallet']}`")
    lines.append(f"- Generated: `{master['meta']['generated_at']}`")
    lines.append(f"- Identity class: **`{ident['class']}`**")
    lines.append("")

    pref = recon.get("preferred_pnl") or {}
    lines.append("## 0. Executive verdict")
    lines.append("")
    lines.append(
        f"This trader is classified as **{ident['class']}** with primary focus "
        f"**{ident['sport_focus'].get('primary')}**. "
        f"Preferred PnL (**{pref.get('field')}**) **{_m(pref.get('value'))}** "
        f"(leaderboard ALL {_m(pref.get('leaderboard_all'))}; "
        f"{'MATCH' if pref.get('match') else 'REVIEW'}). "
        f"Unique trades **{recon['ours']['trades']:,}**. "
        f"Copy difficulty **{copy['difficulty_1_to_10']}/10** · ease **{copy['ease_of_copy_1_to_10']}/10**. "
        f"{copy['why']}"
    )
    lines.append("")
    lines.append(f"**Exit mechanics:** `{copy.get('exit_mechanics')}`")
    lines.append(f"**Kalshi two-sided MM fit:** {copy['kalshi_two_sided_mm_fit']}")
    lines.append(f"**Preferred PnL note:** {pref.get('note')}")
    lines.append("")

    lines.append("## 1. Reconciliation (mandatory)")
    lines.append("")
    lines.append("| Source | PnL | Extra |")
    lines.append("|---|---:|---|")
    lines.append(
        f"| **Preferred ({pref.get('field')})** | **{_m(pref.get('value'))}** | "
        f"vs LB diff={None if pref.get('leaderboard_all') is None else round(float(pref.get('value') or 0) - float(pref.get('leaderboard_all') or 0), 2)} |"
    )
    lines.append(f"| Ours cashflow realized | {_m(recon['ours']['cashflow_realized'])} | trades={recon['ours']['trades']:,} buy_only={recon['ours'].get('note_buy_only')} |")
    lines.append(f"| Ours core (ex-rebate) | {_m(recon['ours']['cashflow_core'])} | WR legs={_pct(recon['ours']['win_rate_legs'])} |")
    lines.append(f"| Ours closed-legs sum | {_m(recon['ours']['closed_positions_sum'])} | PF={recon['ours']['profit_factor']} |")
    lb = recon.get("polymarket_leaderboard_ALL") or {}
    if lb:
        lines.append(f"| Polymarket leaderboard ALL | {_m(lb.get('pnl'))} | vol={_m(lb.get('vol'))} rank={lb.get('rank')} |")
    pd = recon.get("polydata") or {}
    if pd:
        ref = pd.get("realized_pnl") or pd.get("headline_pnl")
        lines.append(
            f"| PolyData | {_m(ref)} | trades={pd.get('n_trades') or (pd.get('raw_meta') or {}).get('n_trades')} "
            f"WR={pd.get('raw_meta',{}).get('win_rate') or pd.get('win_rate_pct')} |"
        )
    lines.append("")
    for c in (recon.get("validation") or {}).get("checks", []):
        lines.append(
            f"- {'MATCH' if c.get('match') else 'DRIFT'}: `{c['source']}` {c['metric']} "
            f"ours={c.get('ours')} field={c.get('ours_field')} ref={c.get('reference')} diff={c.get('diff')}"
        )
    lines.append("")

    lines.append("## 2. Identity & microstructure")
    lines.append("")
    lines.append(f"- Both-sides rate: {_pct(ident['both_sides']['rate'])} ({ident['both_sides']['n']} markets)")
    lines.append(f"- Clip median/p90/max: {_m(ident['clip_size_usdc']['median'])} / {_m(ident['clip_size_usdc']['p90'])} / {_m(ident['clip_size_usdc']['max'])}")
    lines.append(f"- Category PnL: `{ident['sport_focus'].get('category_pnl')}`")
    lines.append(f"- Start BUY first: {extras['start_side']['buy_first']} · SELL first: {extras['start_side']['sell_first']}")
    mt = ident["maker_taker"]
    if mt.get("classified"):
        lines.append(
            f"- Entry maker/taker: {mt['entry']['maker_pct']}% / {mt['entry']['taker_pct']}% "
            f"({mt['entry']['maker_fills']:,}/{mt['entry']['taker_fills']:,} fills)"
        )
        lines.append(
            f"- Exit maker/taker: {mt['exit']['maker_pct']}% / {mt['exit']['taker_pct']}% "
            f"({mt['exit']['maker_fills']:,}/{mt['exit']['taker_fills']:,} fills)"
        )
        lines.append(f"- Patterns: `{mt['patterns']}`")
    lines.append("")
    lines.append("### Outcome volume (top)")
    lines.append("")
    lines.append("| Outcome | Buy USDC | Sell USDC | Sell−Buy |")
    lines.append("|---|---:|---:|---:|")
    for oc, v in list((extras.get("outcome_volume") or {}).items())[:12]:
        lines.append(f"| {oc} | {_m(v['buy_usdc'])} | {_m(v['sell_usdc'])} | {_m(v['net_sell_minus_buy'])} |")
    lines.append("")

    lines.append("## 3. Performance metrics (kitchen sink)")
    lines.append("")
    lines.append(f"- Expectancy / market: {_m(extras['expectancy_per_market'])}")
    lines.append(f"- Avg win / avg loss: {_m(extras['avg_win'])} / {_m(extras['avg_loss'])} · ratio={extras['win_loss_ratio']}")
    lines.append(f"- PnL / day: {_m(extras['pnl_per_day'])} · trades/day={extras['trades_per_day']} · markets/day={extras['markets_per_day']}")
    lines.append(f"- PnL concentration HHI: {extras['pnl_concentration_hhi']} (higher=more concentrated)")
    lines.append(f"- Notional sum: {_m(extras['notional']['sum'])} · median ticket {_m(extras['notional']['median'])}")
    lines.append(f"- Buy price median: {extras['buy_price']['median']} · Sell price median: {extras['sell_price']['median']}")
    lines.append(f"- Activity types: `{extras['activity_type_counts']}`")
    lines.append(f"- Open risk: `{extras['open_risk']}`")
    lines.append("")
    lines.append("### Hold-time engine")
    lines.append("")
    lines.append("| Bucket | N | WR | Total PnL | Avg | Median |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for k, s in (perf.get("hold_time") or {}).items():
        if not s:
            continue
        lines.append(
            f"| {k} | {s['n']} | {_pct(s['win_rate'])} | {_m(s['total_pnl'])} | {_m(s['avg_pnl'])} | {_m(s['median_pnl'])} |"
        )
    lines.append("")
    lines.append("### Entry price bands")
    lines.append("")
    lines.append("| Band | N | WR | Total PnL | Avg |")
    lines.append("|---|---:|---:|---:|---:|")
    for k, s in (perf.get("entry_price_band") or {}).items():
        if not s:
            continue
        lines.append(f"| {k} | {s['n']} | {_pct(s['win_rate'])} | {_m(s['total_pnl'])} | {_m(s['avg_pnl'])} |")
    lines.append("")
    lines.append("### Family")
    lines.append("")
    lines.append("| Family | N | WR | Total PnL | Avg |")
    lines.append("|---|---:|---:|---:|---:|")
    for k, s in (perf.get("family") or {}).items():
        lines.append(f"| {k} | {s['n']} | {_pct(s['win_rate'])} | {_m(s['total_pnl'])} | {_m(s['avg_pnl'])} |")
    lines.append("")

    lines.append("## 4. Equity curve (critical)")
    lines.append("")
    lines.append("### 4a. Cashflow activity equity")
    lines.append("")
    lines.append(f"- Final equity (cashflow): **{_m(eq['final'])}**")
    lines.append(f"- Max DD: **{_m(eq['max_drawdown'])}** ({_pct(eq['max_drawdown_pct_of_peak'])} of peak)")
    lines.append(f"- Longest DD: **{eq['longest_drawdown_days']} days**")
    lines.append(f"- Daily Sharpe (ann.): **{eq['daily_sharpe_ann']}**")
    lines.append(f"- Days: {eq['n_days']}")
    lines.append("")
    lines.append("Files: `equity_curve.csv` · `equity_curve.json` (source=`cashflow_activity`)")
    lines.append("")
    lines.append("<details><summary>Daily cashflow equity table (full)</summary>")
    lines.append("")
    lines.append("| Date | Equity | Daily PnL | Drawdown |")
    lines.append("|---|---:|---:|---:|")
    for row in curve:
        lines.append(f"| {row['date']} | {row['equity']:.2f} | {row['daily_pnl']:.2f} | {row['drawdown']:.2f} |")
    lines.append("")
    lines.append("</details>")
    lines.append("")
    ceq = master.get("equity_closed_summary") or {}
    ccurve = master.get("equity_curve_closed_daily") or []
    lines.append("### 4b. Closed-positions equity (alt — critical for buy-only books)")
    lines.append("")
    lines.append(f"- Final closed equity: **{_m(ceq.get('final'))}**")
    lines.append(f"- Max DD: **{_m(ceq.get('max_drawdown'))}**")
    lines.append(f"- Daily Sharpe (ann.): **{ceq.get('daily_sharpe_ann')}**")
    lines.append(f"- Days: {ceq.get('n_days')}")
    lines.append("")
    lines.append("Files: `equity_curve_closed.csv` · `equity_curve_closed.json` (source=`closed_positions`)")
    lines.append("")
    lines.append("<details><summary>Daily closed equity table (full)</summary>")
    lines.append("")
    lines.append("| Date | Equity | Daily PnL | Drawdown |")
    lines.append("|---|---:|---:|---:|")
    for row in ccurve:
        lines.append(f"| {row['date']} | {row['equity']:.2f} | {row['daily_pnl']:.2f} | {row['drawdown']:.2f} |")
    lines.append("")
    lines.append("</details>")
    lines.append("")
    lines.append("### Top winners / losers contribution")
    lines.append("")
    c = perf["contribution"]
    lines.append(
        f"Top10 winners {_m(c['top10_winners_pnl'])} ({c['top10_winners_share_of_wins_pct']}% of wins) · "
        f"Top10 losers {_m(c['top10_losers_pnl'])} ({c['top10_losers_share_of_losses_pct']}% of losses) · PF={c['profit_factor']}"
    )
    lines.append("")
    for w in c["top10_winners"]:
        lines.append(f"- WIN {_m(w['pnl'])} · {w['hold_s']}s · {w['title']}")
    lines.append("")
    for w in c["top10_losers"]:
        lines.append(f"- LOSS {_m(w['pnl'])} · {w['hold_s']}s · {w['title']}")
    lines.append("")

    lines.append("## 5. Trade management deep dive")
    lines.append("")
    lines.append(f"- Adverse early (>2¢): `{perf['adverse_management']}`")
    lines.append(f"- Favorable first-sell: `{perf['favorable_management']}`")
    lines.append(f"- Campaigns: `{perf['campaigns']}`")
    lines.append(f"- Avg-down: `{perf['avg_down']}`")
    lines.append(f"- Resolution behavior: `{perf['resolution_behavior']}`")
    lines.append(f"- Latency: `{perf['latency']}`")
    lines.append("")
    lines.append("### What works / fails")
    for x in master["deep_dive_highlights"].get("what_works") or []:
        lines.append(f"- WORKS: {x}")
    for x in master["deep_dive_highlights"].get("what_fails") or []:
        lines.append(f"- FAILS: {x}")
    lines.append("")

    lines.append("## 6. Strategy overview (in depth)")
    lines.append("")
    lines.append(strategy_md)
    lines.append("")
    lines.append("## 7. Bot / copy playbook")
    lines.append("")
    lines.append(f"- Difficulty: **{copy['difficulty_1_to_10']}/10** · Ease: **{copy['ease_of_copy_1_to_10']}/10**")
    lines.append(f"- Why: {copy['why']}")
    lines.append("")
    lines.append("### Build steps")
    for i, s in enumerate(copy["build_steps"], 1):
        lines.append(f"{i}. {s}")
    lines.append("")
    lines.append("### Steal")
    for s in copy["steal_from_them"]:
        lines.append(f"- {s}")
    lines.append("")
    lines.append("### Avoid")
    for s in copy["avoid"]:
        lines.append(f"- {s}")
    lines.append("")
    lines.append(f"Bot parameters: `{copy.get('bot_parameters')}`")
    lines.append("")
    lines.append(bot_md)
    lines.append("")

    lines.append("## 8. Structured autopsy (A–G)")
    lines.append("")
    lines.append(autopsy_md)
    lines.append("")

    lines.append("## 9. Hour / DOW volume (UTC)")
    lines.append("")
    lines.append("| Hour | USDC volume |")
    lines.append("|---:|---:|")
    for h, v in (extras.get("hour_volume_usdc_utc") or {}).items():
        lines.append(f"| {h} | {v} |")
    lines.append("")
    lines.append("| DOW (0=Mon) | USDC volume |")
    lines.append("|---:|---:|")
    for d, v in (extras.get("dow_volume_usdc_utc") or {}).items():
        lines.append(f"| {d} | {v} |")
    lines.append("")

    lines.append("## 10. Bot schema pointer")
    lines.append("")
    lines.append(
        "Parse `MASTER.json` keys: `reconciliation`, `identity`, `performance`, `extras`, "
        "`copyability`, `equity_curve_daily`, `deep_dive_highlights`."
    )
    lines.append("")
    return "\n".join(lines)
