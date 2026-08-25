"""PnL and behavioral analytics over synced trader history."""

from __future__ import annotations

import math
import statistics
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


@dataclass
class CashflowPnL:
    buys_usdc: float = 0.0
    sells_usdc: float = 0.0
    redeems_usdc: float = 0.0
    merges_usdc: float = 0.0
    splits_usdc: float = 0.0
    maker_rebates_usdc: float = 0.0
    taker_rebates_usdc: float = 0.0
    rewards_usdc: float = 0.0
    conversions_usdc: float = 0.0

    @property
    def realized_cashflow(self) -> float:
        """PolyData-style: sells - buys + redeems (+ rebates/rewards)."""
        return (
            self.sells_usdc
            - self.buys_usdc
            + self.redeems_usdc
            + self.maker_rebates_usdc
            + self.taker_rebates_usdc
            + self.rewards_usdc
        )

    @property
    def realized_core(self) -> float:
        """Core trading cashflow without rebates."""
        return self.sells_usdc - self.buys_usdc + self.redeems_usdc


@dataclass
class ClosedPnL:
    n_positions: int = 0
    realized_sum: float = 0.0
    wins: int = 0
    losses: int = 0
    flat: int = 0
    win_pnl: float = 0.0
    loss_pnl: float = 0.0
    total_bought: float = 0.0

    @property
    def win_rate(self) -> float:
        decided = self.wins + self.losses
        return (self.wins / decided) if decided else 0.0

    @property
    def profit_factor(self) -> float:
        if self.loss_pnl >= 0:
            return float("inf") if self.win_pnl > 0 else 0.0
        return abs(self.win_pnl / self.loss_pnl)


def _ts_to_dt(ts: int) -> datetime:
    return datetime.fromtimestamp(ts, tz=timezone.utc)


def compute_cashflow(activity: list[dict]) -> CashflowPnL:
    cf = CashflowPnL()
    for a in activity:
        typ = (a.get("type") or "").upper()
        usdc = float(a.get("usdcSize") or 0)
        side = (a.get("side") or "").upper()
        if typ == "TRADE":
            if side == "BUY":
                cf.buys_usdc += usdc
            elif side == "SELL":
                cf.sells_usdc += usdc
        elif typ == "REDEEM":
            cf.redeems_usdc += usdc
        elif typ == "MERGE":
            cf.merges_usdc += usdc
        elif typ == "SPLIT":
            cf.splits_usdc += usdc
        elif typ == "MAKER_REBATE":
            cf.maker_rebates_usdc += usdc
        elif typ == "TAKER_REBATE":
            cf.taker_rebates_usdc += usdc
        elif typ == "REWARD":
            cf.rewards_usdc += usdc
        elif typ == "CONVERSION":
            cf.conversions_usdc += usdc
    return cf


def compute_closed_pnl(closed: list[dict]) -> ClosedPnL:
    out = ClosedPnL(n_positions=len(closed))
    for c in closed:
        pnl = float(c.get("realizedPnl") or 0)
        out.realized_sum += pnl
        out.total_bought += float(c.get("totalBought") or 0)
        if pnl > 1e-9:
            out.wins += 1
            out.win_pnl += pnl
        elif pnl < -1e-9:
            out.losses += 1
            out.loss_pnl += pnl
        else:
            out.flat += 1
    return out


def build_equity_curve(activity: list[dict]) -> list[dict]:
    """Running realized cashflow equity curve from activity (trade/redeem/rebate)."""
    curve: list[dict] = []
    equity = 0.0
    for a in sorted(activity, key=lambda x: x.get("timestamp") or 0):
        typ = (a.get("type") or "").upper()
        usdc = float(a.get("usdcSize") or 0)
        side = (a.get("side") or "").upper()
        delta = 0.0
        if typ == "TRADE":
            if side == "BUY":
                delta = -usdc
            elif side == "SELL":
                delta = usdc
        elif typ in ("REDEEM", "MAKER_REBATE", "TAKER_REBATE", "REWARD"):
            delta = usdc
        elif typ == "MERGE":
            delta = usdc  # merge returns collateral
        elif typ == "SPLIT":
            delta = -usdc
        if delta == 0 and typ not in ("TRADE", "REDEEM", "MAKER_REBATE", "TAKER_REBATE", "REWARD", "MERGE", "SPLIT"):
            continue
        equity += delta
        curve.append(
            {
                "timestamp": int(a.get("timestamp") or 0),
                "equity": round(equity, 6),
                "delta": round(delta, 6),
                "type": typ,
                "side": side or None,
                "title": a.get("title"),
                "usdc": usdc,
            }
        )
    return curve


def market_round_trips(trades: list[dict], closed: list[dict]) -> list[dict]:
    """Per-condition aggregates: entries, exits, sizing, hold proxies."""
    by_cond: dict[str, dict] = defaultdict(
        lambda: {
            "condition_id": "",
            "title": "",
            "event_slug": "",
            "buys": [],
            "sells": [],
            "buy_usdc": 0.0,
            "sell_usdc": 0.0,
            "buy_shares": 0.0,
            "sell_shares": 0.0,
            "n_buys": 0,
            "n_sells": 0,
            "first_ts": None,
            "last_ts": None,
            "outcomes": Counter(),
        }
    )
    for t in trades:
        cid = t.get("conditionId") or ""
        m = by_cond[cid]
        m["condition_id"] = cid
        m["title"] = t.get("title") or m["title"]
        m["event_slug"] = t.get("eventSlug") or m["event_slug"]
        ts = int(t.get("timestamp") or 0)
        size = float(t.get("size") or 0)
        price = float(t.get("price") or 0)
        usdc = size * price
        side = (t.get("side") or "").upper()
        outcome = t.get("outcome") or ""
        m["outcomes"][outcome] += 1
        m["first_ts"] = ts if m["first_ts"] is None else min(m["first_ts"], ts)
        m["last_ts"] = ts if m["last_ts"] is None else max(m["last_ts"], ts)
        if side == "BUY":
            m["buys"].append({"ts": ts, "size": size, "price": price, "usdc": usdc, "outcome": outcome})
            m["buy_usdc"] += usdc
            m["buy_shares"] += size
            m["n_buys"] += 1
        elif side == "SELL":
            m["sells"].append({"ts": ts, "size": size, "price": price, "usdc": usdc, "outcome": outcome})
            m["sell_usdc"] += usdc
            m["sell_shares"] += size
            m["n_sells"] += 1

    closed_by_cond: dict[str, float] = defaultdict(float)
    closed_bought: dict[str, float] = defaultdict(float)
    for c in closed:
        cid = c.get("conditionId") or ""
        closed_by_cond[cid] += float(c.get("realizedPnl") or 0)
        closed_bought[cid] += float(c.get("totalBought") or 0)

    results = []
    for cid, m in by_cond.items():
        hold = None
        if m["first_ts"] is not None and m["last_ts"] is not None:
            hold = m["last_ts"] - m["first_ts"]
        avg_buy = (m["buy_usdc"] / m["buy_shares"]) if m["buy_shares"] else None
        avg_sell = (m["sell_usdc"] / m["sell_shares"]) if m["sell_shares"] else None
        # Gross trading edge ignoring residual inventory / redeems
        trade_edge = m["sell_usdc"] - m["buy_usdc"]
        results.append(
            {
                "condition_id": cid,
                "title": m["title"],
                "event_slug": m["event_slug"],
                "n_buys": m["n_buys"],
                "n_sells": m["n_sells"],
                "buy_usdc": round(m["buy_usdc"], 4),
                "sell_usdc": round(m["sell_usdc"], 4),
                "buy_shares": round(m["buy_shares"], 4),
                "sell_shares": round(m["sell_shares"], 4),
                "avg_buy_price": round(avg_buy, 4) if avg_buy is not None else None,
                "avg_sell_price": round(avg_sell, 4) if avg_sell is not None else None,
                "trade_edge_usdc": round(trade_edge, 4),
                "closed_realized_pnl": round(closed_by_cond.get(cid, 0.0), 4),
                "closed_total_bought": round(closed_bought.get(cid, 0.0), 4),
                "hold_seconds": hold,
                "first_ts": m["first_ts"],
                "last_ts": m["last_ts"],
                "dominant_outcome": (m["outcomes"].most_common(1)[0][0] if m["outcomes"] else None),
                "both_sides": len([o for o in m["outcomes"] if o]) >= 2,
            }
        )
    results.sort(key=lambda x: x["closed_realized_pnl"], reverse=True)
    return results


def detect_market_making(trades: list[dict], markets: list[dict]) -> dict[str, Any]:
    """Heuristics for MM / spread capture vs directional betting."""
    if not trades:
        return {"score": 0, "label": "insufficient_data", "signals": []}

    both_sides = sum(1 for m in markets if m.get("both_sides"))
    both_sides_rate = both_sides / max(1, len(markets))

    # Round-trip speed: markets with buy+sell where hold < 2h
    fast_rt = 0
    rt_with_both = 0
    for m in markets:
        if m["n_buys"] and m["n_sells"] and m.get("hold_seconds") is not None:
            rt_with_both += 1
            if m["hold_seconds"] <= 2 * 3600:
                fast_rt += 1
    fast_rt_rate = fast_rt / max(1, rt_with_both)

    # Price improvement: avg sell > avg buy on same market (spread capture)
    spread_pos = 0
    spread_n = 0
    for m in markets:
        if m.get("avg_buy_price") is not None and m.get("avg_sell_price") is not None:
            spread_n += 1
            if m["avg_sell_price"] > m["avg_buy_price"]:
                spread_pos += 1
    spread_rate = spread_pos / max(1, spread_n)

    # Trade size consistency (bots/MM often size-stable)
    sizes = [float(t.get("size") or 0) for t in trades if float(t.get("size") or 0) > 0]
    size_cv = None
    if len(sizes) >= 10:
        mean = statistics.mean(sizes)
        size_cv = (statistics.pstdev(sizes) / mean) if mean else None

    # Inter-trade gaps
    ts = sorted(int(t.get("timestamp") or 0) for t in trades)
    gaps = [b - a for a, b in zip(ts, ts[1:]) if b > a]
    median_gap = statistics.median(gaps) if gaps else None

    # Outcome mix Over/Under / Yes/No balance
    outcomes = Counter((t.get("outcome") or "") for t in trades)
    ou = outcomes.get("Over", 0) + outcomes.get("Under", 0)
    yn = outcomes.get("Yes", 0) + outcomes.get("No", 0)

    signals = []
    score = 0
    if both_sides_rate >= 0.35:
        score += 25
        signals.append(f"Trades both outcomes in {both_sides_rate:.0%} of markets (inventory/MM signature)")
    if fast_rt_rate >= 0.25:
        score += 20
        signals.append(f"Fast round-trips (<2h) in {fast_rt_rate:.0%} of two-sided markets")
    if spread_rate >= 0.55:
        score += 25
        signals.append(f"Avg sell > avg buy in {spread_rate:.0%} of markets (spread capture)")
    if size_cv is not None and size_cv < 1.2:
        score += 10
        signals.append(f"Relatively consistent size (CV={size_cv:.2f})")
    if median_gap is not None and median_gap < 120:
        score += 10
        signals.append(f"High-frequency cadence (median gap {median_gap:.0f}s)")
    if ou > yn * 1.5 and ou > 100:
        score += 10
        signals.append("Heavy concentration in Over/Under sports totals (sports MM niche)")

    if score >= 70:
        label = "strong_market_maker"
    elif score >= 45:
        label = "likely_market_maker"
    elif score >= 25:
        label = "hybrid_mm_directional"
    else:
        label = "directional_or_unclear"

    return {
        "score": score,
        "label": label,
        "signals": signals,
        "metrics": {
            "both_sides_rate": round(both_sides_rate, 4),
            "fast_roundtrip_rate": round(fast_rt_rate, 4),
            "spread_capture_rate": round(spread_rate, 4),
            "size_cv": round(size_cv, 4) if size_cv is not None else None,
            "median_gap_seconds": median_gap,
            "outcome_counts": dict(outcomes),
        },
    }


def timing_profiles(trades: list[dict]) -> dict[str, Any]:
    hours = Counter()
    dows = Counter()
    for t in trades:
        ts = int(t.get("timestamp") or 0)
        if not ts:
            continue
        dt = _ts_to_dt(ts)
        hours[dt.hour] += 1
        dows[dt.weekday()] += 1
    return {
        "hour_utc": {str(k): hours[k] for k in range(24)},
        "dow_utc": {str(k): dows[k] for k in range(7)},
        "peak_hours": [h for h, _ in hours.most_common(5)],
        "peak_dows": [d for d, _ in dows.most_common(3)],
    }


def sizing_profile(trades: list[dict]) -> dict[str, Any]:
    notionals = [float(t.get("size") or 0) * float(t.get("price") or 0) for t in trades]
    sizes = [float(t.get("size") or 0) for t in trades]
    notionals = [n for n in notionals if n > 0]
    if not notionals:
        return {}
    notionals_sorted = sorted(notionals)
    def pct(p: float) -> float:
        idx = min(len(notionals_sorted) - 1, max(0, int(p * (len(notionals_sorted) - 1))))
        return notionals_sorted[idx]
    return {
        "n": len(notionals),
        "mean_usdc": round(statistics.mean(notionals), 4),
        "median_usdc": round(statistics.median(notionals), 4),
        "p10_usdc": round(pct(0.10), 4),
        "p90_usdc": round(pct(0.90), 4),
        "max_usdc": round(max(notionals), 4),
        "mean_shares": round(statistics.mean(sizes), 4) if sizes else None,
        "median_shares": round(statistics.median(sizes), 4) if sizes else None,
    }


def category_guess(title: str, event_slug: str = "") -> str:
    t = f"{title} {event_slug}".lower()
    if "o/u" in t or "total" in t or "over" in title.lower() or "under" in title.lower():
        return "sports_totals"
    if any(x in t for x in (" vs", "vs.", "fc ", "nba", "nfl", "mlb", "nhl", "ucl", "lal", "bun", "pre")):
        return "sports_match"
    if any(x in t for x in ("btc", "eth", "bitcoin", "ethereum", "crypto", "solana")):
        return "crypto"
    if any(x in t for x in ("trump", "election", "president", "senate", "democrat", "republican")):
        return "politics"
    return "other"


def analyze_trader(
    *,
    username: str,
    wallet: str,
    activity: list[dict],
    trades: list[dict],
    closed: list[dict],
    open_positions: list[dict],
    leaderboard: Optional[dict] = None,
) -> dict[str, Any]:
    cf = compute_cashflow(activity)
    cp = compute_closed_pnl(closed)
    curve = build_equity_curve(activity)
    markets = market_round_trips(trades, closed)
    mm = detect_market_making(trades, markets)
    timing = timing_profiles(trades)
    sizing = sizing_profile(trades)

    # Equity stats
    equities = [p["equity"] for p in curve]
    peak = -math.inf
    max_dd = 0.0
    for e in equities:
        peak = max(peak, e)
        max_dd = min(max_dd, e - peak)
    final_equity = equities[-1] if equities else 0.0

    # Category breakdown via closed PnL
    cat_pnl: dict[str, float] = defaultdict(float)
    cat_n: dict[str, int] = defaultdict(int)
    for c in closed:
        cat = category_guess(c.get("title") or "", c.get("eventSlug") or "")
        cat_pnl[cat] += float(c.get("realizedPnl") or 0)
        cat_n[cat] += 1

    trade_types = Counter((a.get("type") or "") for a in activity)
    buy_n = sum(1 for t in trades if (t.get("side") or "").upper() == "BUY")
    sell_n = sum(1 for t in trades if (t.get("side") or "").upper() == "SELL")

    top_wins = [
        {
            "title": m["title"],
            "pnl": m["closed_realized_pnl"],
            "buy_usdc": m["buy_usdc"],
            "sell_usdc": m["sell_usdc"],
            "n_buys": m["n_buys"],
            "n_sells": m["n_sells"],
            "hold_seconds": m["hold_seconds"],
            "avg_buy": m["avg_buy_price"],
            "avg_sell": m["avg_sell_price"],
        }
        for m in markets[:15]
        if m["closed_realized_pnl"] > 0
    ]
    top_losses = [
        {
            "title": m["title"],
            "pnl": m["closed_realized_pnl"],
            "buy_usdc": m["buy_usdc"],
            "sell_usdc": m["sell_usdc"],
            "n_buys": m["n_buys"],
            "n_sells": m["n_sells"],
            "hold_seconds": m["hold_seconds"],
        }
        for m in sorted(markets, key=lambda x: x["closed_realized_pnl"])[:15]
        if m["closed_realized_pnl"] < 0
    ]

    # Entry/exit vignettes: pick clearest spread-capture markets
    vignettes = []
    for m in markets:
        if (
            m.get("avg_buy_price") is not None
            and m.get("avg_sell_price") is not None
            and m["n_buys"] >= 2
            and m["n_sells"] >= 2
            and m["avg_sell_price"] > m["avg_buy_price"]
            and m["closed_realized_pnl"] > 50
        ):
            vignettes.append(m)
        if len(vignettes) >= 12:
            break

    first_ts = min((int(t.get("timestamp") or 0) for t in trades), default=0)
    last_ts = max((int(t.get("timestamp") or 0) for t in trades), default=0)
    days = max(1, (last_ts - first_ts) / 86400) if first_ts and last_ts else 0

    open_cash = sum(float(p.get("cashPnl") or 0) for p in open_positions)
    open_value = sum(float(p.get("currentValue") or 0) for p in open_positions)
    open_realized = sum(float(p.get("realizedPnl") or 0) for p in open_positions)

    summary = {
        "username": username,
        "wallet": wallet,
        "counts": {
            "activity": len(activity),
            "trades": len(trades),
            "buys": buy_n,
            "sells": sell_n,
            "closed_positions": len(closed),
            "open_positions": len(open_positions),
            "markets_traded": len(markets),
            "activity_types": dict(trade_types),
        },
        "span": {
            "first_ts": first_ts,
            "last_ts": last_ts,
            "first_iso": _ts_to_dt(first_ts).isoformat() if first_ts else None,
            "last_iso": _ts_to_dt(last_ts).isoformat() if last_ts else None,
            "days_active_span": round(days, 2),
        },
        "pnl": {
            "cashflow_realized": round(cf.realized_cashflow, 4),
            "cashflow_core": round(cf.realized_core, 4),
            "cashflow_detail": asdict(cf),
            "closed_positions_sum": round(cp.realized_sum, 4),
            "closed_wins": cp.wins,
            "closed_losses": cp.losses,
            "closed_flat": cp.flat,
            "win_rate": round(cp.win_rate, 4),
            "profit_factor": round(cp.profit_factor, 4) if math.isfinite(cp.profit_factor) else None,
            "win_pnl": round(cp.win_pnl, 4),
            "loss_pnl": round(cp.loss_pnl, 4),
            "total_bought": round(cp.total_bought, 4),
            "open_cash_pnl": round(open_cash, 4),
            "open_current_value": round(open_value, 4),
            "open_realized_pnl": round(open_realized, 4),
            "leaderboard_all": leaderboard,
        },
        "equity": {
            "final": round(final_equity, 4),
            "max_drawdown": round(max_dd, 4),
            "points": len(curve),
            # downsample for storage
            "curve_sample": _downsample(curve, 400),
        },
        "market_making": mm,
        "timing": timing,
        "sizing": sizing,
        "categories": {
            "pnl": {k: round(v, 4) for k, v in sorted(cat_pnl.items(), key=lambda kv: -kv[1])},
            "counts": dict(cat_n),
        },
        "top_wins": top_wins[:10],
        "top_losses": top_losses[:10],
        "strategy_vignettes": [
            {
                "title": v["title"],
                "avg_buy": v["avg_buy_price"],
                "avg_sell": v["avg_sell_price"],
                "spread": round((v["avg_sell_price"] or 0) - (v["avg_buy_price"] or 0), 4),
                "pnl": v["closed_realized_pnl"],
                "n_buys": v["n_buys"],
                "n_sells": v["n_sells"],
                "hold_seconds": v["hold_seconds"],
                "both_sides": v["both_sides"],
            }
            for v in vignettes[:10]
        ],
        "markets": markets,  # full detail for strategy writer / exports
    }
    return summary


def _downsample(curve: list[dict], n: int) -> list[dict]:
    if len(curve) <= n:
        return curve
    step = len(curve) / n
    out = [curve[int(i * step)] for i in range(n - 1)]
    out.append(curve[-1])
    return out
