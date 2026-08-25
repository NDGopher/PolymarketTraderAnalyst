"""Full trader autopsy report generator (polika72-depth or deeper)."""

from __future__ import annotations

import json
import math
import statistics
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from .analytics import analyze_trader, category_guess
from .bot_playbook import write_bot_playbook
from .client import PolymarketClient, _row_key
from .deep_dive import build_episodes, deep_analyze
from .strategy import write_strategy_report
from .validate import fetch_polydata_snapshot, validate_against_sources


HOLD_ORDER = ["<30s", "30s-2m", "2-5m", "5-15m", "15m+"]
BAND_ORDER = ["0-20¢", "20-40¢", "40-60¢", "60-80¢", "80-100¢"]


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
        return f"{s // 60}m{s % 60:02d}s"
    if s < 86400:
        return f"{s // 3600}h{(s % 3600) // 60:02d}m"
    return f"{s // 86400}d"


def _hold_bucket(s: int) -> str:
    if s < 30:
        return "<30s"
    if s < 120:
        return "30s-2m"
    if s < 300:
        return "2-5m"
    if s < 900:
        return "5-15m"
    return "15m+"


def _price_band(p: float | None) -> str:
    if p is None:
        return "n/a"
    c = p * 100
    if c < 20:
        return "0-20¢"
    if c < 40:
        return "20-40¢"
    if c < 60:
        return "40-60¢"
    if c < 80:
        return "60-80¢"
    return "80-100¢"


def _family(ep) -> str:
    oc = Counter()
    for f in ep.fills:
        oc[f.get("outcome") or "?"] += float(f.get("size") or 0) * float(f.get("price") or 0)
    if not oc:
        return "Other"
    top = oc.most_common(1)[0][0]
    if top in ("Over", "Under"):
        return "Over/Under"
    if top in ("Yes", "No"):
        return "Yes/No moneyline"
    return "Other"


def _sport_focus(eps) -> dict[str, Any]:
    cat_pnl: dict[str, float] = defaultdict(float)
    cat_n: Counter = Counter()
    title_tokens = Counter()
    for e in eps:
        cat = category_guess(e.title, e.event_slug)
        cat_pnl[cat] += e.realized_pnl
        cat_n[cat] += 1
        slug = (e.event_slug or "").lower()
        for tok in ("mlb", "nba", "nfl", "nhl", "ucl", "lal", "bun", "ten", "atp", "wta", "ufc", "mma"):
            if tok in slug or tok in (e.title or "").lower():
                title_tokens[tok] += 1
    return {
        "category_pnl": {k: round(v, 2) for k, v in sorted(cat_pnl.items(), key=lambda kv: -kv[1])},
        "category_counts": dict(cat_n),
        "slug_tokens": title_tokens.most_common(12),
        "primary": (max(cat_pnl.items(), key=lambda kv: kv[1])[0] if cat_pnl else "unknown"),
    }


def _bucket_stats(groups: dict) -> dict:
    out = {}
    for k, items in groups.items():
        pnls = [e.realized_pnl for e in items]
        wins = sum(1 for p in pnls if p > 1e-9)
        losses = sum(1 for p in pnls if p < -1e-9)
        decided = wins + losses
        out[k] = {
            "n": len(items),
            "wins": wins,
            "losses": losses,
            "win_rate": round(wins / decided, 4) if decided else None,
            "total_pnl": round(sum(pnls), 2),
            "avg_pnl": round(statistics.mean(pnls), 2) if pnls else None,
            "median_pnl": round(statistics.median(pnls), 2) if pnls else None,
        }
    return out


def _daily_equity(activity: list[dict]) -> list[dict]:
    by_day: dict[str, float] = defaultdict(float)
    for a in activity:
        typ = (a.get("type") or "").upper()
        usdc = float(a.get("usdcSize") or 0)
        side = (a.get("side") or "").upper()
        ts = int(a.get("timestamp") or 0)
        if not ts:
            continue
        day = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
        delta = 0.0
        if typ == "TRADE":
            delta = -usdc if side == "BUY" else usdc
        elif typ in ("REDEEM", "MAKER_REBATE", "TAKER_REBATE", "REWARD", "MERGE"):
            delta = usdc
        elif typ == "SPLIT":
            delta = -usdc
        by_day[day] += delta
    curve = []
    eq = 0.0
    peak = 0.0
    max_dd = 0.0
    max_dd_pct = 0.0
    dd_start = None
    longest_dd_days = 0
    cur_dd_start = None
    for day in sorted(by_day):
        eq += by_day[day]
        if eq > peak:
            peak = eq
            if cur_dd_start is not None:
                # end drawdown
                cur_dd_start = None
        dd = eq - peak
        if dd < max_dd:
            max_dd = dd
        if peak > 0:
            max_dd_pct = min(max_dd_pct, dd / peak)
        if dd < -1e-6:
            if cur_dd_start is None:
                cur_dd_start = day
        else:
            if cur_dd_start is not None:
                # compute days
                d0 = datetime.strptime(cur_dd_start, "%Y-%m-%d")
                d1 = datetime.strptime(day, "%Y-%m-%d")
                longest_dd_days = max(longest_dd_days, (d1 - d0).days)
                cur_dd_start = None
        curve.append({"date": day, "equity": round(eq, 4), "daily_pnl": round(by_day[day], 4), "drawdown": round(dd, 4)})
    if cur_dd_start is not None and curve:
        d0 = datetime.strptime(cur_dd_start, "%Y-%m-%d")
        d1 = datetime.strptime(curve[-1]["date"], "%Y-%m-%d")
        longest_dd_days = max(longest_dd_days, (d1 - d0).days)
    daily = [p["daily_pnl"] for p in curve]
    sharpe = None
    if len(daily) >= 5 and statistics.pstdev(daily) > 0:
        sharpe = (statistics.mean(daily) / statistics.pstdev(daily)) * math.sqrt(365)
    return {
        "curve": curve,
        "final": curve[-1]["equity"] if curve else 0.0,
        "max_drawdown": round(max_dd, 4),
        "max_drawdown_pct_of_peak": round(max_dd_pct, 4),
        "longest_drawdown_days": longest_dd_days,
        "daily_sharpe_ann": round(sharpe, 3) if sharpe is not None else None,
        "n_days": len(curve),
    }


def classify_roles(trades: list[dict], taker_keys: set[str]) -> None:
    for t in trades:
        t["_role"] = "taker" if _row_key(t) in taker_keys else "maker"


def fetch_taker_keys(client: PolymarketClient, wallet: str, start_ts: int, end_ts: int) -> set[str]:
    rows: list[dict] = []
    seen: set[str] = set()
    stack = [(start_ts, end_ts, 24 * 3600)]
    while stack:
        ws, range_end, win = stack.pop()
        if ws > range_end:
            continue
        we = min(ws + win - 1, range_end)
        off = 0
        overflow = False
        while True:
            batch = client.get_json(
                "https://data-api.polymarket.com",
                "/trades",
                {
                    "user": wallet,
                    "limit": 1000,
                    "offset": off,
                    "start": ws,
                    "end": we,
                    "takerOnly": "true",
                },
            ) or []
            if not batch:
                break
            for r in batch:
                k = _row_key(r)
                if k not in seen:
                    seen.add(k)
                    rows.append(r)
            if len(batch) < 1000:
                break
            nxt = off + 1000
            if nxt > 10000:
                overflow = True
                break
            off = nxt
        if overflow:
            mid = (ws + we) // 2
            if mid > ws:
                stack.append((mid + 1, range_end, max(1, win // 2)))
                stack.append((ws, mid, max(1, win // 2)))
            continue
        nxt = we + 1
        if nxt <= range_end:
            stack.append((nxt, range_end, win))
    return {_row_key(r) for r in rows}


def run_autopsy(
    *,
    username: str,
    wallet: str,
    activity: list[dict],
    trades: list[dict],
    closed: list[dict],
    open_positions: list[dict],
    leaderboard: Optional[dict],
    polydata: Optional[dict],
    taker_keys: Optional[set[str]] = None,
    polika_benchmark: Optional[dict] = None,
) -> dict[str, Any]:
    if taker_keys is not None:
        classify_roles(trades, taker_keys)

    summary = analyze_trader(
        username=username,
        wallet=wallet,
        activity=activity,
        trades=trades,
        closed=closed,
        open_positions=open_positions,
        leaderboard=leaderboard,
    )
    deep = deep_analyze(trades, closed, activity, open_positions)
    episode_stats = deep.pop("episode_stats", [])
    validation = validate_against_sources(summary, leaderboard=leaderboard, polydata=polydata)
    eps = build_episodes(trades, closed)

    # Role-aware fill helper
    role_map = {_row_key(t): t.get("_role", "unknown") for t in trades}

    def fill_role(f):
        return role_map.get(_row_key(f), "unknown")

    def usdc(f):
        return float(f.get("size") or 0) * float(f.get("price") or 0)

    # Hold / band / family
    by_hold, by_band, by_fam = defaultdict(list), defaultdict(list), defaultdict(list)
    for e in eps:
        by_hold[_hold_bucket(e.hold_seconds)].append(e)
        by_band[_price_band(e.avg_entry)].append(e)
        by_fam[_family(e)].append(e)
    hold_stats = {k: _bucket_stats(by_hold).get(k) for k in HOLD_ORDER if k in by_hold}
    band_stats = {k: _bucket_stats(by_band).get(k) for k in BAND_ORDER if k in by_band}
    fam_stats = _bucket_stats(by_fam)

    # Maker/taker volumes
    entry_m = entry_t = exit_m = exit_t = 0.0
    entry_m_n = entry_t_n = exit_m_n = exit_t_n = 0
    for t in trades:
        u = float(t.get("size") or 0) * float(t.get("price") or 0)
        role = t.get("_role", "unknown")
        if (t.get("side") or "").upper() == "BUY":
            if role == "maker":
                entry_m += u
                entry_m_n += 1
            elif role == "taker":
                entry_t += u
                entry_t_n += 1
        else:
            if role == "maker":
                exit_m += u
                exit_m_n += 1
            elif role == "taker":
                exit_t += u
                exit_t_n += 1
    entry_tot = entry_m + entry_t
    exit_tot = exit_m + exit_t
    pat = Counter()
    for e in eps:
        buy_m = sum(usdc(f) for f in e.fills if (f.get("side") or "").upper() == "BUY" and fill_role(f) == "maker")
        buy_t = sum(usdc(f) for f in e.fills if (f.get("side") or "").upper() == "BUY" and fill_role(f) == "taker")
        sell_m = sum(usdc(f) for f in e.fills if (f.get("side") or "").upper() == "SELL" and fill_role(f) == "maker")
        sell_t = sum(usdc(f) for f in e.fills if (f.get("side") or "").upper() == "SELL" and fill_role(f) == "taker")
        if e.n_buys and e.n_sells:
            ein = "maker" if buy_m >= buy_t else "taker"
            eout = "maker" if sell_m >= sell_t else "taker"
            pat[f"enter_{ein}_exit_{eout}"] += 1

    # Campaigns
    for e in eps:
        net = 0.0
        state = "flat"
        n_entries = 0
        for f in e.fills:
            side = (f.get("side") or "").upper()
            sz = float(f.get("size") or 0)
            net += sz if side == "BUY" else -sz
            if state == "flat" and net >= 1:
                state = "long"
                n_entries += 1
            elif state == "long" and abs(net) < 1:
                state = "flat"
        e._n_entries = n_entries
        e._is_campaign = n_entries >= 2
    camp = [e for e in eps if e._is_campaign]
    single = [e for e in eps if not e._is_campaign]

    # Both-sides
    both = sum(1 for e in eps if e.both_sides)

    # Flatten before resolution
    flat_before = [e for e in eps if e.flattened_before_resolution]
    hold_res = [e for e in eps if e.exit_style == "hold_to_resolution_or_redeem"]

    # Equity
    equity = _daily_equity(activity)

    # Top winners/losers contribution
    ranked = sorted(eps, key=lambda e: e.realized_pnl, reverse=True)
    top10w = ranked[:10]
    top10l = ranked[-10:]
    total_pnl = sum(e.realized_pnl for e in eps)
    win_pnl = sum(e.realized_pnl for e in eps if e.realized_pnl > 0)
    loss_pnl = sum(e.realized_pnl for e in eps if e.realized_pnl < 0)

    # Adverse / favorable management
    against_stats = []
    favor_stats = []
    mfe_capture = []
    mfe_times = []
    for e in eps:
        buys = [f for f in e.fills if (f.get("side") or "").upper() == "BUY"]
        sells = [f for f in e.fills if (f.get("side") or "").upper() == "SELL"]
        if not buys or not sells:
            continue
        t0 = int(buys[0]["timestamp"])
        p0 = float(buys[0]["price"])
        after_sells = [f for f in sells if int(f["timestamp"]) >= t0]
        if not after_sells:
            continue
        first_sell = float(after_sells[0]["price"])
        dt = int(after_sells[0]["timestamp"]) - t0
        max_sell = max(float(f["price"]) for f in after_sells)
        last_sell = float(after_sells[-1]["price"])
        mfe = max_sell - p0
        early = [f for f in after_sells if int(f["timestamp"]) - t0 <= 120]
        min_early = min((float(f["price"]) for f in early), default=None)
        row = {
            "pnl": e.realized_pnl,
            "hold": e.hold_seconds,
            "first_delta": first_sell - p0,
            "t_first_sell": dt,
            "mfe": mfe,
            "capture": ((last_sell - p0) / mfe) if mfe > 1e-9 else None,
        }
        if min_early is not None and min_early < p0 - 0.02:
            against_stats.append(row)
        if first_sell >= p0 + 0.02:
            favor_stats.append(row)
        if e.realized_pnl > 0 and mfe > 0:
            mfe_capture.append(row["capture"])
            # time to MFE
            t_mfe = 0
            max_px = p0
            for f in e.fills:
                if int(f["timestamp"]) < t0:
                    continue
                px = float(f.get("price") or 0)
                if px > max_px:
                    max_px = px
                    t_mfe = int(f["timestamp"]) - t0
            mfe_times.append({"mfe": max_px - p0, "t_mfe": t_mfe})

    # Avg-down MTM red
    def sim(fills, skip_red=False):
        lots = []
        realized = 0.0
        last_px = None
        red_buys = 0
        for f in fills:
            side = (f.get("side") or "").upper()
            sz = float(f.get("size") or 0)
            px = float(f.get("price") or 0)
            shares = sum(l[0] for l in lots)
            vwap = (sum(l[0] * l[1] for l in lots) / shares) if shares else None
            mtm_red = shares >= 1 and last_px is not None and vwap is not None and last_px < vwap - 0.005
            if side == "BUY":
                if mtm_red:
                    red_buys += 1
                    if skip_red:
                        last_px = px
                        continue
                lots.append([sz, px])
                last_px = px
            else:
                rem = sz
                proceeds = cost = 0.0
                while rem > 1e-12 and lots:
                    take = min(lots[0][0], rem)
                    cost += take * lots[0][1]
                    proceeds += take * px
                    lots[0][0] -= take
                    rem -= take
                    if lots[0][0] <= 1e-12:
                        lots.pop(0)
                if sz - rem > 0:
                    realized += proceeds - cost
                last_px = px
        return realized, red_buys

    losers = [e for e in eps if e.realized_pnl < -1e-9]
    loser_red = []
    for e in losers:
        a, n = sim(e.fills)
        b, _ = sim(e.fills, True)
        if n > 0:
            loser_red.append({"pnl": e.realized_pnl, "delta": b - a, "red_buys": n})

    base_s = sum(sim(e.fills)[0] for e in eps)
    cf_s = sum(sim(e.fills, True)[0] for e in eps)

    # Clip sizes
    clips = [float(t.get("size") or 0) * float(t.get("price") or 0) for t in trades if float(t.get("size") or 0) > 0]
    clips = [c for c in clips if c > 0]
    clips_s = sorted(clips)

    def pct(p):
        if not clips_s:
            return None
        return round(clips_s[min(len(clips_s) - 1, int(p * (len(clips_s) - 1)))], 4)

    sport = _sport_focus(eps)

    # Classification
    both_rate = both / max(1, len(eps))
    mm_score = summary["market_making"]["score"]
    entry_taker_pct = (100 * entry_t / entry_tot) if entry_tot else 0
    if both_rate >= 0.25 and mm_score >= 45:
        identity = "two_sided_inventory_mm"
    elif entry_taker_pct >= 55 and mm_score >= 40:
        identity = "one_sided_informed_scalper"
    elif both_rate < 0.05 and summary["pnl"]["cashflow_detail"]["redeems_usdc"] > abs(summary["pnl"]["cashflow_core"]) * 0.3:
        identity = "directional_hold_to_resolution"
    elif mm_score >= 45:
        identity = "hybrid_liquidity_scalper"
    else:
        identity = "directional_or_unclear"

    # Latency summary
    tm = [x["t_mfe"] for x in mfe_times if x["mfe"] > 0]
    tm10 = [x["t_mfe"] for x in mfe_times if x["mfe"] >= 0.10]
    big = [x for x in mfe_times if x["mfe"] >= 0.10]
    big30 = sum(1 for x in mfe_times if x["mfe"] >= 0.10 and x["t_mfe"] <= 30)
    big60 = sum(1 for x in mfe_times if x["mfe"] >= 0.10 and x["t_mfe"] <= 60)

    stats = {
        "username": username,
        "wallet": wallet,
        "identity": identity,
        "market_making": summary["market_making"],
        "sport_focus": sport,
        "counts": summary["counts"],
        "span": summary["span"],
        "pnl": summary["pnl"],
        "validation": validation,
        "polydata": polydata,
        "leaderboard": leaderboard,
        "hold_time": hold_stats,
        "entry_price_band": band_stats,
        "family": fam_stats,
        "maker_taker": {
            "entry": {
                "maker_usdc": round(entry_m, 2),
                "taker_usdc": round(entry_t, 2),
                "maker_pct": round(100 * entry_m / entry_tot, 2) if entry_tot else None,
                "taker_pct": round(100 * entry_t / entry_tot, 2) if entry_tot else None,
                "maker_fills": entry_m_n,
                "taker_fills": entry_t_n,
            },
            "exit": {
                "maker_usdc": round(exit_m, 2),
                "taker_usdc": round(exit_t, 2),
                "maker_pct": round(100 * exit_m / exit_tot, 2) if exit_tot else None,
                "taker_pct": round(100 * exit_t / exit_tot, 2) if exit_tot else None,
                "maker_fills": exit_m_n,
                "taker_fills": exit_t_n,
            },
            "patterns": dict(pat),
            "classified": taker_keys is not None,
        },
        "both_sides": {"n": both, "rate": round(both_rate, 4)},
        "clip_size_usdc": {
            "median": pct(0.5),
            "mean": round(statistics.mean(clips), 4) if clips else None,
            "p90": pct(0.9),
            "p99": pct(0.99),
            "max": round(max(clips), 4) if clips else None,
        },
        "campaigns": {
            "n": len(camp),
            "pct": round(100 * len(camp) / max(1, len(eps)), 2),
            "avg_entries": round(statistics.mean(e._n_entries for e in camp), 2) if camp else None,
            "pnl": round(sum(e.realized_pnl for e in camp), 2),
            "avg_pnl": round(statistics.mean(e.realized_pnl for e in camp), 2) if camp else None,
            "win_rate": round(sum(1 for e in camp if e.realized_pnl > 0) / len(camp), 4) if camp else None,
            "single_n": len(single),
            "single_pnl": round(sum(e.realized_pnl for e in single), 2),
            "single_avg_pnl": round(statistics.mean(e.realized_pnl for e in single), 2) if single else None,
        },
        "resolution_behavior": {
            "flattened_before_flag_rate": round(len(flat_before) / max(1, len(eps)), 4),
            "hold_to_resolution_style_n": len(hold_res),
            "redeems_usdc": summary["pnl"]["cashflow_detail"]["redeems_usdc"],
            "merges_usdc": summary["pnl"]["cashflow_detail"]["merges_usdc"],
        },
        "equity": {k: v for k, v in equity.items() if k != "curve"},
        "equity_curve_daily": equity["curve"],
        "contribution": {
            "top10_winners_pnl": round(sum(e.realized_pnl for e in top10w), 2),
            "top10_winners_share_of_wins_pct": round(100 * sum(e.realized_pnl for e in top10w) / win_pnl, 2) if win_pnl else None,
            "top10_losers_pnl": round(sum(e.realized_pnl for e in top10l), 2),
            "top10_losers_share_of_losses_pct": round(100 * sum(e.realized_pnl for e in top10l) / loss_pnl, 2) if loss_pnl else None,
            "top10_winners": [{"title": e.title, "pnl": round(e.realized_pnl, 2), "hold_s": e.hold_seconds} for e in top10w],
            "top10_losers": [{"title": e.title, "pnl": round(e.realized_pnl, 2), "hold_s": e.hold_seconds} for e in top10l],
            "profit_factor": summary["pnl"]["profit_factor"],
        },
        "adverse_management": {
            "n_early_adverse": len(against_stats),
            "avg_pnl": round(statistics.mean(r["pnl"] for r in against_stats), 2) if against_stats else None,
            "median_t_first_sell": int(statistics.median(r["t_first_sell"] for r in against_stats)) if against_stats else None,
            "median_hold": int(statistics.median(r["hold"] for r in against_stats)) if against_stats else None,
        },
        "favorable_management": {
            "n_first_sell_up_2c": len(favor_stats),
            "avg_pnl": round(statistics.mean(r["pnl"] for r in favor_stats), 2) if favor_stats else None,
            "median_mfe_capture": round(statistics.median(mfe_capture), 4) if mfe_capture else None,
            "mean_mfe_capture": round(statistics.mean(mfe_capture), 4) if mfe_capture else None,
        },
        "avg_down": {
            "n_losers": len(losers),
            "n_losers_with_red_buys": len(loser_red),
            "pct_losers": round(100 * len(loser_red) / max(1, len(losers)), 2),
            "total_delta_if_skipped_on_losers": round(sum(x["delta"] for x in loser_red), 2) if loser_red else 0,
            "global_fifo_sim": round(base_s, 2),
            "global_fifo_never_red_buy": round(cf_s, 2),
            "global_delta": round(cf_s - base_s, 2),
        },
        "latency": {
            "time_to_mfe_median": int(statistics.median(tm)) if tm else None,
            "time_to_mfe_p25": int(statistics.quantiles(tm, n=4)[0]) if len(tm) >= 4 else None,
            "time_to_mfe_p75": int(statistics.quantiles(tm, n=4)[2]) if len(tm) >= 4 else None,
            "time_to_mfe_p90": int(sorted(tm)[int(0.9 * (len(tm) - 1))]) if tm else None,
            "mfe_ge_10c_n": len(big),
            "mfe_ge_10c_within_30s": big30,
            "mfe_ge_10c_within_60s": big60,
            "pct_big_within_60s": round(100 * big60 / max(1, len(big)), 2),
        },
        "risk": {
            "max_inventory_shares": round(max(e.max_inventory_shares for e in eps), 2) if eps else 0,
            "max_dd": equity["max_drawdown"],
            "max_dd_pct": equity["max_drawdown_pct_of_peak"],
            "longest_dd_days": equity["longest_drawdown_days"],
        },
        "deep": deep,
        "polika_benchmark": polika_benchmark,
    }

    # Build markdown
    md = _render_markdown(stats, summary, validation)
    strategy_md = write_strategy_report(summary, validation)
    bot_md = write_bot_playbook(username, wallet, summary, deep, validation)

    return {
        "stats": stats,
        "summary": summary,
        "deep": deep,
        "validation": validation,
        "autopsy_md": md,
        "strategy_md": strategy_md,
        "bot_md": bot_md,
        "episode_stats_count": len(episode_stats),
    }


def _render_markdown(stats: dict, summary: dict, validation: dict) -> str:
    u = stats["username"]
    lines: list[str] = []
    lines.append(f"# Deep Trader Autopsy — {u}")
    lines.append("")
    lines.append(f"- Wallet: `{stats['wallet']}`")
    lines.append(f"- Identity: **`{stats['identity']}`**")
    lines.append(f"- Primary focus: **{stats['sport_focus']['primary']}**")
    lines.append(f"- Span: {summary['span'].get('first_iso')} → {summary['span'].get('last_iso')} ({summary['span'].get('days_active_span')} days)")
    lines.append(f"- Generated: {datetime.now(timezone.utc).isoformat()}")
    lines.append("")

    lines.append("## A. Data integrity / reconciliation")
    lines.append("")
    lines.append("| Source | PnL | Trades / notes |")
    lines.append("|---|---:|---|")
    lines.append(f"| Our cashflow realized | {_m(summary['pnl']['cashflow_realized'])} | trades={summary['counts']['trades']:,} |")
    lines.append(f"| Our core cashflow | {_m(summary['pnl']['cashflow_core'])} | buys={summary['counts']['buys']:,} sells={summary['counts']['sells']:,} |")
    lines.append(f"| Our closed-legs sum | {_m(summary['pnl']['closed_positions_sum'])} | closed={summary['counts']['closed_positions']:,} WR={summary['pnl']['win_rate']*100:.1f}% |")
    lb = stats.get("leaderboard") or {}
    if lb:
        lines.append(f"| Polymarket leaderboard ALL | {_m(float(lb.get('pnl') or 0))} | vol={_m(float(lb.get('vol') or 0))} rank={lb.get('rank')} |")
    pd = stats.get("polydata") or {}
    if pd:
        ref = pd.get("realized_pnl") or pd.get("headline_pnl")
        lines.append(f"| PolyData | {_m(float(ref) if ref else 0)} | trades={pd.get('n_trades') or (pd.get('raw_meta') or {}).get('n_trades')} WR={pd.get('raw_meta',{}).get('win_rate') or pd.get('win_rate_pct')} |")
    lines.append("")
    for c in validation.get("checks", []):
        flag = "MATCH" if c.get("match") else "DRIFT"
        lines.append(f"- **{flag}** `{c['source']}` {c['metric']}: ours={c.get('ours')} ref={c.get('reference')} diff={c.get('diff')}")
    lines.append("")

    lines.append("## B. Core identity")
    lines.append("")
    lines.append(f"- Scanner MM label: `{stats['market_making']['label']}` (score {stats['market_making']['score']})")
    for s in stats["market_making"].get("signals") or []:
        lines.append(f"- {s}")
    lines.append(f"- Both-sides inventory: {stats['both_sides']['n']} markets ({stats['both_sides']['rate']*100:.2f}%)")
    lines.append(f"- Clip USDC median/p90/max: {_m(stats['clip_size_usdc']['median'])} / {_m(stats['clip_size_usdc']['p90'])} / {_m(stats['clip_size_usdc']['max'])}")
    lines.append(f"- Sport categories: `{stats['sport_focus']['category_pnl']}`")
    lines.append(f"- Slug tokens: {stats['sport_focus']['slug_tokens']}")
    lines.append("")
    mt = stats["maker_taker"]
    if mt.get("classified"):
        lines.append("### Maker vs Taker")
        lines.append("")
        lines.append("| Leg | Maker % | Taker % | Maker fills | Taker fills |")
        lines.append("|---|---:|---:|---:|---:|")
        lines.append(
            f"| Entry | {mt['entry']['maker_pct']}% | {mt['entry']['taker_pct']}% | {mt['entry']['maker_fills']:,} | {mt['entry']['taker_fills']:,} |"
        )
        lines.append(
            f"| Exit | {mt['exit']['maker_pct']}% | {mt['exit']['taker_pct']}% | {mt['exit']['maker_fills']:,} | {mt['exit']['taker_fills']:,} |"
        )
        lines.append("")
        for k, v in sorted(mt["patterns"].items(), key=lambda kv: -kv[1]):
            lines.append(f"- `{k}`: {v}")
    else:
        lines.append("_Maker/taker not classified for this run._")
    lines.append("")

    lines.append("### Price bands")
    lines.append("")
    lines.append("| Band | N | WR | Total PnL | Avg |")
    lines.append("|---|---:|---:|---:|---:|")
    for k, s in (stats["entry_price_band"] or {}).items():
        if not s:
            continue
        wr = f"{100*s['win_rate']:.1f}%" if s.get("win_rate") is not None else "n/a"
        lines.append(f"| {k} | {s['n']} | {wr} | {_m(s['total_pnl'])} | {_m(s['avg_pnl'])} |")
    lines.append("")

    lines.append("## C. Equity & risk")
    lines.append("")
    eq = stats["equity"]
    lines.append(f"- Final cashflow equity: {_m(eq['final'])}")
    lines.append(f"- Max drawdown: {_m(eq['max_drawdown'])} ({eq['max_drawdown_pct_of_peak']*100:.1f}% of peak)")
    lines.append(f"- Longest drawdown: {eq['longest_drawdown_days']} days")
    lines.append(f"- Daily Sharpe (ann.): {eq['daily_sharpe_ann']}")
    lines.append(f"- Profit factor: {stats['contribution']['profit_factor']}")
    lines.append(
        f"- Top 10 winners: {_m(stats['contribution']['top10_winners_pnl'])} "
        f"({stats['contribution']['top10_winners_share_of_wins_pct']}% of win PnL)"
    )
    lines.append(
        f"- Top 10 losers: {_m(stats['contribution']['top10_losers_pnl'])} "
        f"({stats['contribution']['top10_losers_share_of_losses_pct']}% of loss PnL)"
    )
    lines.append(f"- Max inventory shares: {stats['risk']['max_inventory_shares']}")
    lines.append("")
    lines.append("### Top winners")
    for w in stats["contribution"]["top10_winners"]:
        lines.append(f"- {_m(w['pnl'])} · {_s(w['hold_s'])} · {w['title']}")
    lines.append("")
    lines.append("### Top losers")
    for w in stats["contribution"]["top10_losers"]:
        lines.append(f"- {_m(w['pnl'])} · {_s(w['hold_s'])} · {w['title']}")
    lines.append("")

    lines.append("## D. Trade management")
    lines.append("")
    lines.append("### Hold-time buckets")
    lines.append("")
    lines.append("| Bucket | N | WR | Total PnL | Avg |")
    lines.append("|---|---:|---:|---:|---:|")
    for k, s in (stats["hold_time"] or {}).items():
        if not s:
            continue
        wr = f"{100*s['win_rate']:.1f}%" if s.get("win_rate") is not None else "n/a"
        lines.append(f"| {k} | {s['n']} | {wr} | {_m(s['total_pnl'])} | {_m(s['avg_pnl'])} |")
    lines.append("")
    adv = stats["adverse_management"]
    fav = stats["favorable_management"]
    lines.append(
        f"- After early adverse (>2¢ vs entry within 2m): n={adv['n_early_adverse']}, "
        f"avg PnL {_m(adv['avg_pnl'])}, median first-sell {_s(adv['median_t_first_sell'])}, median hold {_s(adv['median_hold'])}"
    )
    lines.append(
        f"- After favorable first sell (+2¢): n={fav['n_first_sell_up_2c']}, avg PnL {_m(fav['avg_pnl'])}, "
        f"median MFE capture {fav['median_mfe_capture']}"
    )
    c = stats["campaigns"]
    lines.append(
        f"- Campaigns (re-entry after flat): {c['n']} ({c['pct']}%), avg entries {c['avg_entries']}, "
        f"PnL {_m(c['pnl'])}, avg {_m(c['avg_pnl'])}, WR {None if c['win_rate'] is None else round(100*c['win_rate'],1)}%"
    )
    lines.append(
        f"- Single-entry: n={c['single_n']}, PnL {_m(c['single_pnl'])}, avg {_m(c['single_avg_pnl'])}"
    )
    rb = stats["resolution_behavior"]
    lines.append(
        f"- Flatten-before-resolution flag rate: {rb['flattened_before_flag_rate']}; "
        f"hold-to-resolution style n={rb['hold_to_resolution_style_n']}; "
        f"redeems {_m(rb['redeems_usdc'])}; merges {_m(rb['merges_usdc'])}"
    )
    ad = stats["avg_down"]
    lines.append(
        f"- Avg-down while MTM-red on losers: {ad['n_losers_with_red_buys']}/{ad['n_losers']} ({ad['pct_losers']}%); "
        f"Δ if skipped on those {_m(ad['total_delta_if_skipped_on_losers'])}; "
        f"global never-red-buy Δ {_m(ad['global_delta'])}"
    )
    lines.append("")

    lines.append("### Family mix")
    lines.append("")
    lines.append("| Family | N | WR | Total PnL | Avg |")
    lines.append("|---|---:|---:|---:|---:|")
    for k, s in (stats["family"] or {}).items():
        wr = f"{100*s['win_rate']:.1f}%" if s.get("win_rate") is not None else "n/a"
        lines.append(f"| {k} | {s['n']} | {wr} | {_m(s['total_pnl'])} | {_m(s['avg_pnl'])} |")
    lines.append("")

    lines.append("## E. Edge diagnosis")
    lines.append("")
    lat = stats["latency"]
    lines.append(
        f"- Time to MFE (winners): median {_s(lat['time_to_mfe_median'])}, "
        f"p25 {_s(lat['time_to_mfe_p25'])}, p75 {_s(lat['time_to_mfe_p75'])}, p90 {_s(lat['time_to_mfe_p90'])}"
    )
    lines.append(
        f"- Big MFE ≥10¢: n={lat['mfe_ge_10c_n']}; within 30s={lat['mfe_ge_10c_within_30s']}; "
        f"within 60s={lat['mfe_ge_10c_within_60s']} ({lat['pct_big_within_60s']}% of big moves)"
    )
    lines.append("")
    # Edge narrative
    if stats["identity"] == "one_sided_informed_scalper":
        lines.append(
            "**Edge thesis:** Joins short-horizon informed / impulse flow — taker-heavy entries, "
            "exits into strength. Money from markout seconds–minutes after entry, not two-sided spreads."
        )
    elif stats["identity"] == "two_sided_inventory_mm":
        lines.append(
            "**Edge thesis:** Classic inventory MM — both-sides presence with spread capture; "
            "edge from quoting and inventory skew, not event sniping alone."
        )
    elif stats["identity"] == "directional_hold_to_resolution":
        lines.append(
            "**Edge thesis:** Directional positioning with significant redeem/merge cashflows — "
            "holds risk into resolution more than pure scalpers."
        )
    else:
        lines.append(
            "**Edge thesis:** Hybrid / mixed — inspect maker-taker mix, hold buckets, and redeem share above."
        )
    lines.append("")

    lines.append("## F. vs polika72")
    lines.append("")
    bench = stats.get("polika_benchmark")
    if bench:
        lines.append("| Metric | This trader | polika72 |")
        lines.append("|---|---:|---:|")
        rows = [
            ("identity", stats["identity"], bench.get("identity")),
            ("trades", summary["counts"]["trades"], bench.get("trades")),
            ("cashflow_pnl", summary["pnl"]["cashflow_realized"], bench.get("cashflow_pnl")),
            ("win_rate", summary["pnl"]["win_rate"], bench.get("win_rate")),
            ("entry_taker_pct", mt["entry"].get("taker_pct") if mt.get("classified") else None, bench.get("entry_taker_pct")),
            ("both_sides_rate", stats["both_sides"]["rate"], bench.get("both_sides_rate")),
            ("median_clip", stats["clip_size_usdc"]["median"], bench.get("median_clip")),
            ("campaign_pct", stats["campaigns"]["pct"], bench.get("campaign_pct")),
            ("max_dd", stats["equity"]["max_drawdown"], bench.get("max_dd")),
            ("time_to_mfe_med", lat["time_to_mfe_median"], bench.get("time_to_mfe_med")),
        ]
        for name, a, b in rows:
            lines.append(f"| {name} | {a} | {b} |")
        lines.append("")
        lines.append("### Steal / avoid")
        lines.append("")
        lines.append(_steal_avoid(stats, bench))
    else:
        lines.append("_polika72 benchmark not provided in this run._")
    lines.append("")

    lines.append("## G. Kalshi two-sided informed MM relevance")
    lines.append("")
    lines.append(_kalshi_relevance(stats))
    lines.append("")
    return "\n".join(lines)


def _steal_avoid(stats: dict, bench: dict) -> str:
    lines = []
    if stats["both_sides"]["rate"] > 0.15:
        lines.append("- **Steal:** both-sides inventory discipline (closer to true MM than polika72).")
    if (stats["maker_taker"].get("entry") or {}).get("maker_pct", 0) and stats["maker_taker"]["entry"]["maker_pct"] > 50:
        lines.append("- **Steal:** maker-led entries (better for quoting stack on Kalshi).")
    if stats["identity"] == "one_sided_informed_scalper":
        lines.append("- **Steal:** impulse entry timing / live-event reaction if transferable.")
        lines.append("- **Avoid:** copying one-sided Over bias blindly onto Kalshi without feed parity.")
    if stats["campaigns"]["pct"] > 10:
        lines.append("- **Steal:** same-market campaign re-entry after flat.")
    if abs(stats["equity"]["max_drawdown"]) > abs(float(bench.get("max_dd") or 0)) * 2:
        lines.append("- **Avoid:** their drawdown profile — size down vs polika72 risk.")
    if stats["avg_down"]["pct_losers"] > 10:
        lines.append("- **Avoid:** averaging down while red.")
    if not lines:
        lines.append("- Mixed profile — cherry-pick hold-bucket edges and maker/taker pattern only after paper trading.")
    return "\n".join(lines)


def _kalshi_relevance(stats: dict) -> str:
    if stats["identity"] == "two_sided_inventory_mm":
        return (
            "High relevance to a Kalshi two-sided informed MM: both-sides + quoting DNA. "
            "Port inventory caps, skew rules, and maker exit logic; replace Polymarket sports feed with Kalshi event feeds."
        )
    if stats["identity"] == "one_sided_informed_scalper":
        return (
            "Partial relevance: the *informed impulse* leg maps to an aggressive/taker overlay on Kalshi, "
            "but this is NOT the core two-sided MM. Use as a signal/overlay module, not the whole bot."
        )
    return (
        "Moderate relevance — extract risk limits and hold-time discipline; "
        "do not assume their edge transfers without Kalshi-specific microstructure testing."
    )
