"""Run full autopsy for a trader and persist sample reports."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Optional

from .autopsy import fetch_taker_keys, run_autopsy
from .pipeline import AnalyzerApp

log = logging.getLogger(__name__)

POLIKA_BENCH = {
    "identity": "one_sided_informed_scalper",
    "trades": 19978,
    "cashflow_pnl": 58204.98,
    "win_rate": 0.8008,
    "entry_taker_pct": 61.6,
    "both_sides_rate": 0.008,
    "median_clip": 11.29,
    "campaign_pct": 5.85,
    "max_dd": -5000,  # approximate placeholder updated from equity if available
    "time_to_mfe_med": 64,
}


def run_full_autopsy(
    app: AnalyzerApp,
    identifier: str,
    *,
    force_full: bool = False,
    classify_maker_taker: bool = True,
) -> dict[str, Any]:
    sync_result = app.sync.sync(identifier, force_full=force_full)
    wallet = sync_result["wallet"]
    username = sync_result["username"]

    activity = app.store.load_activity(wallet)
    trades = app.store.load_trades(wallet)
    closed = app.store.load_closed_positions(wallet)
    opened = app.store.load_open_positions(wallet)
    leaderboard = app.client.leaderboard_entry(wallet, "ALL")

    from .validate import fetch_polydata_snapshot

    polydata = fetch_polydata_snapshot(username)

    taker_keys = None
    if classify_maker_taker and trades:
        start_ts = min(int(t.get("timestamp") or 0) for t in trades)
        end_ts = max(int(t.get("timestamp") or 0) for t in trades) + 1
        cache = app.data_dir / "reports" / username / "taker_keys.json"
        cache.parent.mkdir(parents=True, exist_ok=True)
        if cache.exists() and not force_full:
            taker_keys = set(json.loads(cache.read_text()))
            log.info("Loaded cached taker keys: %s", len(taker_keys))
        else:
            log.info("Fetching taker-only fills for maker/taker classification...")
            taker_keys = fetch_taker_keys(app.client, wallet, start_ts, end_ts)
            cache.write_text(json.dumps(list(taker_keys)))
            log.info("Classified taker fills: %s / %s", len(taker_keys), len(trades))

    # Refresh polika benchmark from sample if present
    bench = dict(POLIKA_BENCH)
    polika_summary = app.reports_dir / "polika72" / "summary.json"
    if polika_summary.exists():
        s = json.loads(polika_summary.read_text())
        bench["trades"] = s.get("counts", {}).get("trades", bench["trades"])
        bench["cashflow_pnl"] = s.get("pnl", {}).get("cashflow_realized", bench["cashflow_pnl"])
        bench["win_rate"] = s.get("pnl", {}).get("win_rate", bench["win_rate"])
        bench["max_dd"] = s.get("equity", {}).get("max_drawdown", bench["max_dd"])

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

    # Persist under data/reports and samples/
    trader_dir = app.reports_dir / username
    trader_dir.mkdir(parents=True, exist_ok=True)
    samples = Path(__file__).resolve().parents[2] / "samples" / username
    samples.mkdir(parents=True, exist_ok=True)

    slim = dict(result["summary"])
    markets = slim.pop("markets", [])
    files = {
        "autopsy.md": result["autopsy_md"],
        "strategy.md": result["strategy_md"],
        "bot_playbook.md": result["bot_md"],
        "summary.json": json.dumps(slim, indent=2),
        "stats.json": json.dumps({k: v for k, v in result["stats"].items() if k not in ("equity_curve_daily", "deep")}, indent=2),
        "equity_curve.json": json.dumps(result["stats"]["equity_curve_daily"], indent=2),
        "validation.json": json.dumps(result["validation"], indent=2),
        "deep_dive.json": json.dumps(result["deep"], indent=2),
        "sync.json": json.dumps(sync_result, indent=2),
    }
    # markets can be huge — still store in data, skip samples if enormous
    (trader_dir / "markets.json").write_text(json.dumps(markets))
    for name, content in files.items():
        (trader_dir / name).write_text(content)
        if name != "deep_dive.json" or len(content) < 5_000_000:
            (samples / name).write_text(content)
    if len(json.dumps(markets)) < 8_000_000:
        (samples / "markets.json").write_text(json.dumps(markets))

    app.store.save_analysis(
        wallet,
        username,
        slim,
        result["autopsy_md"],
        result["validation"],
    )

    return {
        "username": username,
        "wallet": wallet,
        "sync": sync_result,
        "validation": result["validation"],
        "stats": result["stats"],
        "paths": {"data": str(trader_dir), "samples": str(samples)},
    }
