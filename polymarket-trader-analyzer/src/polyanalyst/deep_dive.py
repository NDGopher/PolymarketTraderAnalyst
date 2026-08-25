"""Ultra-deep trade management reconstruction for MM / scalper reverse-engineering."""

from __future__ import annotations

import math
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


def _dt(ts: int) -> datetime:
    return datetime.fromtimestamp(ts, tz=timezone.utc)


@dataclass
class InventoryPoint:
    ts: int
    side: str
    outcome: str
    size: float
    price: float
    usdc: float
    position_after: float  # net shares for this outcome token
    inventory_usdc_after: float


@dataclass
class MarketEpisode:
    condition_id: str
    title: str
    event_slug: str
    end_date: Optional[str]
    fills: list[dict] = field(default_factory=list)
    outcomes: dict[str, list[dict]] = field(default_factory=lambda: defaultdict(list))
    closed_legs: list[dict] = field(default_factory=list)

    # derived
    realized_pnl: float = 0.0
    total_bought: float = 0.0
    first_ts: int = 0
    last_ts: int = 0
    hold_seconds: int = 0
    n_buys: int = 0
    n_sells: int = 0
    buy_usdc: float = 0.0
    sell_usdc: float = 0.0
    both_sides: bool = False
    entry_style: str = ""
    exit_style: str = ""
    management_style: str = ""
    scale_ins: int = 0
    scale_outs: int = 0
    max_inventory_shares: float = 0.0
    avg_entry: Optional[float] = None
    avg_exit: Optional[float] = None
    spread_captured: Optional[float] = None
    first_fill_price: Optional[float] = None
    last_fill_price: Optional[float] = None
    seconds_to_resolution: Optional[int] = None
    flattened_before_resolution: Optional[bool] = None
    inventory_timeline: list[dict] = field(default_factory=list)
    phases: dict[str, Any] = field(default_factory=dict)


def _parse_end_ts(end_date: Optional[str]) -> Optional[int]:
    if not end_date:
        return None
    try:
        # endDate often YYYY-MM-DD — treat as UTC end of day
        dt = datetime.strptime(end_date[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        return int(dt.timestamp()) + 86400 - 1
    except Exception:
        return None


def build_episodes(trades: list[dict], closed: list[dict]) -> list[MarketEpisode]:
    by_cid: dict[str, MarketEpisode] = {}
    for t in sorted(trades, key=lambda x: int(x.get("timestamp") or 0)):
        cid = t.get("conditionId") or ""
        ep = by_cid.get(cid)
        if ep is None:
            ep = MarketEpisode(
                condition_id=cid,
                title=t.get("title") or "",
                event_slug=t.get("eventSlug") or "",
                end_date=None,
            )
            by_cid[cid] = ep
        ep.fills.append(t)
        outcome = t.get("outcome") or "?"
        ep.outcomes[outcome].append(t)

    closed_by_cid: dict[str, list[dict]] = defaultdict(list)
    for c in closed:
        closed_by_cid[c.get("conditionId") or ""].append(c)

    episodes = []
    for cid, ep in by_cid.items():
        ep.closed_legs = closed_by_cid.get(cid, [])
        if ep.closed_legs:
            ep.end_date = ep.closed_legs[0].get("endDate") or ep.end_date
            ep.realized_pnl = sum(float(c.get("realizedPnl") or 0) for c in ep.closed_legs)
            ep.total_bought = sum(float(c.get("totalBought") or 0) for c in ep.closed_legs)
        _enrich_episode(ep)
        episodes.append(ep)
    episodes.sort(key=lambda e: e.realized_pnl, reverse=True)
    return episodes


def _enrich_episode(ep: MarketEpisode) -> None:
    if not ep.fills:
        return
    ts_list = [int(f.get("timestamp") or 0) for f in ep.fills]
    ep.first_ts = min(ts_list)
    ep.last_ts = max(ts_list)
    ep.hold_seconds = ep.last_ts - ep.first_ts
    ep.both_sides = len([o for o, fills in ep.outcomes.items() if fills and o != "?"]) >= 2

    buy_usdc = sell_usdc = buy_sh = sell_sh = 0.0
    n_buys = n_sells = 0
    # Per-outcome inventory reconstruction
    pos: dict[str, float] = defaultdict(float)
    cost: dict[str, float] = defaultdict(float)  # usdc invested net
    max_inv = 0.0
    timeline = []
    prev_side = None
    scale_ins = scale_outs = 0
    buy_streak = sell_streak = 0

    for f in ep.fills:
        side = (f.get("side") or "").upper()
        outcome = f.get("outcome") or "?"
        size = float(f.get("size") or 0)
        price = float(f.get("price") or 0)
        usdc = size * price
        ts = int(f.get("timestamp") or 0)
        if side == "BUY":
            pos[outcome] += size
            cost[outcome] += usdc
            buy_usdc += usdc
            buy_sh += size
            n_buys += 1
            buy_streak += 1
            sell_streak = 0
            if buy_streak >= 2:
                scale_ins += 1
        elif side == "SELL":
            pos[outcome] -= size
            cost[outcome] -= usdc
            sell_usdc += usdc
            sell_sh += size
            n_sells += 1
            sell_streak += 1
            buy_streak = 0
            if sell_streak >= 2:
                scale_outs += 1
        inv = sum(abs(v) for v in pos.values())
        max_inv = max(max_inv, inv)
        timeline.append(
            {
                "ts": ts,
                "side": side,
                "outcome": outcome,
                "size": round(size, 4),
                "price": round(price, 4),
                "usdc": round(usdc, 4),
                "pos": {k: round(v, 4) for k, v in pos.items() if abs(v) > 1e-9},
                "net_shares": round(sum(pos.values()), 4),
                "gross_inventory": round(inv, 4),
            }
        )
        prev_side = side

    ep.n_buys = n_buys
    ep.n_sells = n_sells
    ep.buy_usdc = buy_usdc
    ep.sell_usdc = sell_usdc
    ep.scale_ins = scale_ins
    ep.scale_outs = scale_outs
    ep.max_inventory_shares = max_inv
    ep.avg_entry = (buy_usdc / buy_sh) if buy_sh else None
    ep.avg_exit = (sell_usdc / sell_sh) if sell_sh else None
    if ep.avg_entry is not None and ep.avg_exit is not None:
        ep.spread_captured = ep.avg_exit - ep.avg_entry
    ep.first_fill_price = float(ep.fills[0].get("price") or 0)
    ep.last_fill_price = float(ep.fills[-1].get("price") or 0)
    ep.inventory_timeline = timeline

    end_ts = _parse_end_ts(ep.end_date)
    if end_ts:
        ep.seconds_to_resolution = end_ts - ep.last_ts
        # Flattened if final gross inventory near 0 OR last activity well before end
        final_inv = timeline[-1]["gross_inventory"] if timeline else 0
        ep.flattened_before_resolution = final_inv < 1.0 or (ep.seconds_to_resolution > 3600)

    # Classify entry / exit / management
    first = ep.fills[0]
    first_side = (first.get("side") or "").upper()
    first_px = float(first.get("price") or 0)
    if first_px <= 0.25:
        cheap = "cheap_tail"
    elif first_px <= 0.45:
        cheap = "sub_mid"
    elif first_px <= 0.55:
        cheap = "near_mid"
    elif first_px <= 0.75:
        cheap = "above_mid"
    else:
        cheap = "expensive_favorite"

    if ep.both_sides:
        ep.entry_style = f"two_sided_inventory_{cheap}"
    elif first_side == "BUY":
        ep.entry_style = f"directional_buy_{cheap}"
    else:
        ep.entry_style = f"sell_first_{cheap}"

    if n_buys and n_sells and ep.spread_captured is not None and ep.spread_captured > 0.01:
        ep.exit_style = "spread_harvest_sell_above_buy"
    elif n_buys and n_sells and ep.spread_captured is not None and ep.spread_captured < -0.01:
        ep.exit_style = "adverse_exit_sell_below_buy"
    elif n_sells == 0 and n_buys > 0:
        ep.exit_style = "hold_to_resolution_or_redeem"
    elif n_buys == 0 and n_sells > 0:
        ep.exit_style = "sell_inventory_only"
    else:
        ep.exit_style = "mixed_roundtrip"

    # Management style
    if ep.both_sides and n_buys >= 2 and n_sells >= 2:
        ep.management_style = "market_make_both_outcomes"
    elif scale_ins >= 2 and scale_outs >= 2:
        ep.management_style = "scale_in_scale_out"
    elif n_buys + n_sells <= 2:
        ep.management_style = "single_clip"
    elif ep.hold_seconds <= 900:
        ep.management_style = "scalp_sub_15m"
    elif ep.hold_seconds <= 7200:
        ep.management_style = "intraday_swing"
    else:
        ep.management_style = "multi_hour_position"

    # Phases: opening / middle / closing thirds of fills
    n = len(ep.fills)
    if n >= 3:
        a, b = max(1, n // 3), max(1, (2 * n) // 3)
        phases = {
            "open": ep.fills[:a],
            "middle": ep.fills[a:b],
            "close": ep.fills[b:],
        }
        def avg_px(fills, side=None):
            xs = [
                float(f.get("price") or 0)
                for f in fills
                if side is None or (f.get("side") or "").upper() == side
            ]
            return statistics.mean(xs) if xs else None
        ep.phases = {
            "open_avg_buy": avg_px(phases["open"], "BUY"),
            "open_avg_sell": avg_px(phases["open"], "SELL"),
            "close_avg_buy": avg_px(phases["close"], "BUY"),
            "close_avg_sell": avg_px(phases["close"], "SELL"),
            "open_n": len(phases["open"]),
            "middle_n": len(phases["middle"]),
            "close_n": len(phases["close"]),
        }


def deep_analyze(
    trades: list[dict],
    closed: list[dict],
    activity: list[dict],
    open_positions: list[dict],
) -> dict[str, Any]:
    episodes = build_episodes(trades, closed)

    # Global style histograms
    entry_styles = Counter(e.entry_style for e in episodes)
    exit_styles = Counter(e.exit_style for e in episodes)
    mgmt_styles = Counter(e.management_style for e in episodes)

    winners = [e for e in episodes if e.realized_pnl > 1e-6]
    losers = [e for e in episodes if e.realized_pnl < -1e-6]
    flats = [e for e in episodes if abs(e.realized_pnl) <= 1e-6]

    def summarize_cohort(eps: list[MarketEpisode]) -> dict[str, Any]:
        if not eps:
            return {}
        holds = [e.hold_seconds for e in eps]
        spreads = [e.spread_captured for e in eps if e.spread_captured is not None]
        tickets = []
        for e in eps:
            for f in e.fills:
                tickets.append(float(f.get("size") or 0) * float(f.get("price") or 0))
        both = sum(1 for e in eps if e.both_sides)
        flat_before = [e for e in eps if e.flattened_before_resolution]
        return {
            "n": len(eps),
            "pnl": round(sum(e.realized_pnl for e in eps), 4),
            "avg_pnl": round(statistics.mean(e.realized_pnl for e in eps), 4),
            "median_hold_s": int(statistics.median(holds)) if holds else None,
            "mean_hold_s": int(statistics.mean(holds)) if holds else None,
            "median_spread": round(statistics.median(spreads), 4) if spreads else None,
            "mean_spread": round(statistics.mean(spreads), 4) if spreads else None,
            "both_sides_rate": round(both / len(eps), 4),
            "median_ticket_usdc": round(statistics.median(tickets), 4) if tickets else None,
            "avg_fills": round(statistics.mean(len(e.fills) for e in eps), 2),
            "scale_in_rate": round(sum(1 for e in eps if e.scale_ins > 0) / len(eps), 4),
            "scale_out_rate": round(sum(1 for e in eps if e.scale_outs > 0) / len(eps), 4),
            "flatten_before_res_rate": round(len(flat_before) / len(eps), 4) if eps else None,
            "top_entry_styles": entry_styles_for(eps),
            "top_mgmt_styles": Counter(e.management_style for e in eps).most_common(5),
            "top_exit_styles": Counter(e.exit_style for e in eps).most_common(5),
        }

    def entry_styles_for(eps):
        return Counter(e.entry_style for e in eps).most_common(8)

    # Price band edge
    band_stats = defaultdict(lambda: {"n": 0, "pnl": 0.0, "buys": 0})
    for e in episodes:
        if e.avg_entry is None:
            continue
        p = e.avg_entry
        if p < 0.2:
            band = "0.00-0.20"
        elif p < 0.4:
            band = "0.20-0.40"
        elif p < 0.6:
            band = "0.40-0.60"
        elif p < 0.8:
            band = "0.60-0.80"
        else:
            band = "0.80-1.00"
        band_stats[band]["n"] += 1
        band_stats[band]["pnl"] += e.realized_pnl

    # Hold-time buckets vs PnL
    hold_buckets = {
        "<5m": [],
        "5-30m": [],
        "30m-2h": [],
        "2-12h": [],
        "12h+": [],
    }
    for e in episodes:
        h = e.hold_seconds
        if h < 300:
            hold_buckets["<5m"].append(e.realized_pnl)
        elif h < 1800:
            hold_buckets["5-30m"].append(e.realized_pnl)
        elif h < 7200:
            hold_buckets["30m-2h"].append(e.realized_pnl)
        elif h < 43200:
            hold_buckets["2-12h"].append(e.realized_pnl)
        else:
            hold_buckets["12h+"].append(e.realized_pnl)
    hold_edge = {
        k: {
            "n": len(v),
            "pnl": round(sum(v), 4),
            "avg": round(statistics.mean(v), 4) if v else 0,
            "win_rate": round(sum(1 for x in v if x > 0) / len(v), 4) if v else 0,
        }
        for k, v in hold_buckets.items()
    }

    # Fill sequencing: buy-then-sell vs sell-then-buy first pair
    seq = Counter()
    for e in episodes:
        if len(e.fills) < 2:
            seq["single_fill"] += 1
            continue
        a = (e.fills[0].get("side") or "").upper()
        b = (e.fills[1].get("side") or "").upper()
        seq[f"{a}->{b}"] += 1

    # Inter-fill aggression proxy: consecutive same-outcome buys climbing price = chase
    chase_markets = 0
    fade_markets = 0
    for e in episodes:
        buys = [f for f in e.fills if (f.get("side") or "").upper() == "BUY"]
        if len(buys) < 3:
            continue
        px = [float(f.get("price") or 0) for f in buys]
        # slope
        slope = px[-1] - px[0]
        if slope > 0.03:
            chase_markets += 1
        elif slope < -0.03:
            fade_markets += 1

    # Maker rebate contribution
    rebates = [
        a for a in activity if (a.get("type") or "") in ("MAKER_REBATE", "TAKER_REBATE")
    ]
    maker_rebate = sum(float(a.get("usdcSize") or 0) for a in rebates if a.get("type") == "MAKER_REBATE")
    taker_rebate = sum(float(a.get("usdcSize") or 0) for a in rebates if a.get("type") == "TAKER_REBATE")

    # Outcome preference
    outcome_pnl = defaultdict(float)
    outcome_n = Counter()
    for e in episodes:
        for leg in e.closed_legs:
            oc = leg.get("outcome") or "?"
            outcome_pnl[oc] += float(leg.get("realizedPnl") or 0)
            outcome_n[oc] += 1

    # Title keyword edge (O/U lines)
    ou_eps = [e for e in episodes if "o/u" in (e.title or "").lower() or "total" in (e.event_slug or "").lower()]
    match_eps = [e for e in episodes if e not in ou_eps and ("win" in (e.title or "").lower() or "vs" in (e.title or "").lower())]

    # Representative playbooks with full timelines (best MM examples)
    mm_examples = [
        e
        for e in episodes
        if e.management_style == "market_make_both_outcomes"
        and e.realized_pnl > 80
        and len(e.fills) >= 4
    ][:8]
    scalp_examples = [
        e
        for e in episodes
        if e.management_style in ("scalp_sub_15m", "scale_in_scale_out")
        and e.spread_captured
        and e.spread_captured > 0.02
        and e.realized_pnl > 40
    ][:8]
    failure_examples = [
        e for e in sorted(episodes, key=lambda x: x.realized_pnl)[:10]
    ]

    def ep_brief(e: MarketEpisode, include_timeline: bool = True) -> dict:
        d = {
            "title": e.title,
            "condition_id": e.condition_id,
            "realized_pnl": round(e.realized_pnl, 4),
            "hold_seconds": e.hold_seconds,
            "n_fills": len(e.fills),
            "n_buys": e.n_buys,
            "n_sells": e.n_sells,
            "buy_usdc": round(e.buy_usdc, 4),
            "sell_usdc": round(e.sell_usdc, 4),
            "avg_entry": round(e.avg_entry, 4) if e.avg_entry is not None else None,
            "avg_exit": round(e.avg_exit, 4) if e.avg_exit is not None else None,
            "spread_captured": round(e.spread_captured, 4) if e.spread_captured is not None else None,
            "both_sides": e.both_sides,
            "entry_style": e.entry_style,
            "exit_style": e.exit_style,
            "management_style": e.management_style,
            "scale_ins": e.scale_ins,
            "scale_outs": e.scale_outs,
            "max_inventory_shares": round(e.max_inventory_shares, 2),
            "first_iso": _dt(e.first_ts).isoformat() if e.first_ts else None,
            "last_iso": _dt(e.last_ts).isoformat() if e.last_ts else None,
            "end_date": e.end_date,
            "seconds_to_resolution": e.seconds_to_resolution,
            "flattened_before_resolution": e.flattened_before_resolution,
            "phases": e.phases,
            "outcomes_traded": list(e.outcomes.keys()),
        }
        if include_timeline:
            # downsample timeline if huge
            tl = e.inventory_timeline
            if len(tl) > 40:
                step = len(tl) / 40
                tl = [tl[int(i * step)] for i in range(40)]
            d["inventory_timeline"] = tl
            d["fills"] = [
                {
                    "ts": int(f.get("timestamp") or 0),
                    "iso": _dt(int(f.get("timestamp") or 0)).isoformat(),
                    "side": f.get("side"),
                    "outcome": f.get("outcome"),
                    "size": float(f.get("size") or 0),
                    "price": float(f.get("price") or 0),
                    "usdc": round(float(f.get("size") or 0) * float(f.get("price") or 0), 4),
                }
                for f in (e.fills if len(e.fills) <= 30 else e.fills[:15] + e.fills[-15:])
            ]
        return d

    # Bot parameter recommendations derived from winners
    w = winners
    param_suggestions = {}
    if w:
        entry_px = [e.avg_entry for e in w if e.avg_entry is not None]
        exit_px = [e.avg_exit for e in w if e.avg_exit is not None]
        spreads = [e.spread_captured for e in w if e.spread_captured is not None]
        holds = [e.hold_seconds for e in w]
        tickets = []
        for e in w:
            for f in e.fills:
                tickets.append(float(f.get("size") or 0) * float(f.get("price") or 0))
        param_suggestions = {
            "preferred_entry_price_median": round(statistics.median(entry_px), 4) if entry_px else None,
            "preferred_entry_price_p25_p75": (
                round(statistics.quantiles(entry_px, n=4)[0], 4),
                round(statistics.quantiles(entry_px, n=4)[2], 4),
            )
            if len(entry_px) >= 4
            else None,
            "target_spread_median": round(statistics.median(spreads), 4) if spreads else None,
            "target_spread_p75": round(statistics.quantiles(spreads, n=4)[2], 4) if len(spreads) >= 4 else None,
            "max_hold_seconds_p75": int(statistics.quantiles(holds, n=4)[2]) if len(holds) >= 4 else None,
            "median_hold_seconds": int(statistics.median(holds)) if holds else None,
            "clip_size_usdc_median": round(statistics.median(tickets), 4) if tickets else None,
            "clip_size_usdc_p90": round(sorted(tickets)[int(0.9 * (len(tickets) - 1))], 4) if tickets else None,
            "both_sides_on_winners_rate": round(sum(1 for e in w if e.both_sides) / len(w), 4),
            "require_exit_above_entry": True,
            "flatten_before_resolution": True,
            "maker_bias": maker_rebate > taker_rebate,
        }

    # What works / doesn't
    what_works = []
    what_fails = []
    wc = summarize_cohort(winners)
    lc = summarize_cohort(losers)
    if wc.get("median_spread") is not None and lc.get("median_spread") is not None:
        what_works.append(
            f"Winners capture median spread {wc['median_spread']} vs losers {lc['median_spread']}"
        )
    if wc.get("both_sides_rate") is not None:
        what_works.append(
            f"Both-sides inventory on {wc['both_sides_rate']*100:.1f}% of winning markets "
            f"(losers {lc.get('both_sides_rate', 0)*100:.1f}%)"
        )
    # hold comparison
    for bucket, st in hold_edge.items():
        if st["n"] >= 20 and st["avg"] > 5:
            what_works.append(f"Hold bucket {bucket}: avg PnL ${st['avg']:.2f} on {st['n']} markets (WR {st['win_rate']*100:.0f}%)")
        if st["n"] >= 20 and st["avg"] < -5:
            what_fails.append(f"Hold bucket {bucket}: avg PnL ${st['avg']:.2f} on {st['n']} markets")

    for band, st in sorted(band_stats.items()):
        avg = st["pnl"] / st["n"] if st["n"] else 0
        if st["n"] >= 30 and avg > 10:
            what_works.append(f"Entry band {band}: avg ${avg:.2f} across {st['n']} markets")
        if st["n"] >= 30 and avg < -5:
            what_fails.append(f"Entry band {band}: avg ${avg:.2f} across {st['n']} markets — avoid or tighten risk")

    if chase_markets or fade_markets:
        what_works.append(
            f"Buy-ladder behavior: fade-into-weakness markets={fade_markets}, chase-up markets={chase_markets}"
        )

    # Open book residue risk
    open_risk = {
        "n": len(open_positions),
        "cash_pnl": round(sum(float(p.get("cashPnl") or 0) for p in open_positions), 4),
        "current_value": round(sum(float(p.get("currentValue") or 0) for p in open_positions), 4),
        "redeemable": sum(1 for p in open_positions if p.get("redeemable")),
    }

    return {
        "n_episodes": len(episodes),
        "n_winners": len(winners),
        "n_losers": len(losers),
        "n_flats": len(flats),
        "entry_styles": entry_styles.most_common(15),
        "exit_styles": exit_styles.most_common(10),
        "management_styles": mgmt_styles.most_common(10),
        "sequence_patterns": seq.most_common(),
        "winners": wc,
        "losers": lc,
        "hold_edge": hold_edge,
        "entry_price_bands": {
            k: {"n": v["n"], "pnl": round(v["pnl"], 4), "avg": round(v["pnl"] / v["n"], 4) if v["n"] else 0}
            for k, v in sorted(band_stats.items())
        },
        "outcome_pnl": {k: round(v, 4) for k, v in sorted(outcome_pnl.items(), key=lambda kv: -kv[1])},
        "outcome_counts": dict(outcome_n),
        "ou_markets": summarize_cohort(ou_eps),
        "match_markets": summarize_cohort(match_eps),
        "rebates": {
            "maker": round(maker_rebate, 4),
            "taker": round(taker_rebate, 4),
            "maker_events": sum(1 for a in rebates if a.get("type") == "MAKER_REBATE"),
            "taker_events": sum(1 for a in rebates if a.get("type") == "TAKER_REBATE"),
        },
        "chase_vs_fade": {"chase_up": chase_markets, "fade_down": fade_markets},
        "what_works": what_works,
        "what_fails": what_fails,
        "bot_parameters": param_suggestions,
        "open_risk": open_risk,
        "mm_examples": [ep_brief(e) for e in mm_examples],
        "scalp_examples": [ep_brief(e) for e in scalp_examples],
        "failure_examples": [ep_brief(e) for e in failure_examples],
        # keep compact episode stats for further tooling (no full timelines)
        "episode_stats": [
            {
                "title": e.title,
                "pnl": round(e.realized_pnl, 4),
                "hold": e.hold_seconds,
                "fills": len(e.fills),
                "entry": e.entry_style,
                "exit": e.exit_style,
                "mgmt": e.management_style,
                "spread": round(e.spread_captured, 4) if e.spread_captured is not None else None,
                "both_sides": e.both_sides,
                "avg_entry": round(e.avg_entry, 4) if e.avg_entry is not None else None,
                "avg_exit": round(e.avg_exit, 4) if e.avg_exit is not None else None,
            }
            for e in episodes
        ],
    }
