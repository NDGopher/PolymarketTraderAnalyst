"""Pipeline: sync → analyze → validate → strategy report."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Optional

from .analytics import analyze_trader
from .client import PolymarketClient
from .compare import compare_traders, format_comparison
from .store import Store
from .strategy import write_strategy_report
from .sync import SyncService
from .validate import fetch_polydata_snapshot, validate_against_sources

log = logging.getLogger(__name__)


class AnalyzerApp:
    def __init__(self, data_dir: Path | str) -> None:
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir = self.data_dir / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.store = Store(self.data_dir / "polyanalyst.db")
        self.client = PolymarketClient()
        self.sync = SyncService(self.client, self.store)

    def run(
        self,
        identifier: str,
        *,
        force_full: bool = False,
        skip_polydata: bool = False,
    ) -> dict[str, Any]:
        sync_result = self.sync.sync(identifier, force_full=force_full)
        wallet = sync_result["wallet"]
        username = sync_result["username"]

        activity = self.store.load_activity(wallet)
        trades = self.store.load_trades(wallet)
        closed = self.store.load_closed_positions(wallet)
        opened = self.store.load_open_positions(wallet)
        leaderboard = self.client.leaderboard_entry(wallet, "ALL")

        summary = analyze_trader(
            username=username,
            wallet=wallet,
            activity=activity,
            trades=trades,
            closed=closed,
            open_positions=opened,
            leaderboard=leaderboard,
        )

        polydata = None if skip_polydata else fetch_polydata_snapshot(username)
        validation = validate_against_sources(summary, leaderboard=leaderboard, polydata=polydata)
        strategy_md = write_strategy_report(summary, validation)

        run_id = self.store.save_analysis(wallet, username, summary, strategy_md, validation)

        # Persist artifacts (summary without full markets dump for readability + full json)
        trader_dir = self.reports_dir / username
        trader_dir.mkdir(parents=True, exist_ok=True)
        slim = dict(summary)
        markets = slim.pop("markets", [])
        (trader_dir / "summary.json").write_text(json.dumps(slim, indent=2))
        (trader_dir / "markets.json").write_text(json.dumps(markets, indent=2))
        (trader_dir / "validation.json").write_text(json.dumps(validation, indent=2))
        (trader_dir / "strategy.md").write_text(strategy_md)
        (trader_dir / "sync.json").write_text(json.dumps(sync_result, indent=2))

        return {
            "run_id": run_id,
            "sync": sync_result,
            "summary": slim,
            "validation": validation,
            "strategy_md": strategy_md,
            "paths": {
                "summary": str(trader_dir / "summary.json"),
                "markets": str(trader_dir / "markets.json"),
                "strategy": str(trader_dir / "strategy.md"),
                "validation": str(trader_dir / "validation.json"),
            },
        }

    def show(self, identifier: str) -> dict[str, Any]:
        resolved = self.sync.resolve_and_register(identifier)
        latest = self.store.latest_analysis(resolved["wallet"])
        if not latest:
            raise FileNotFoundError(
                f"No saved analysis for {resolved['username']}. Run `analyze` first."
            )
        return latest

    def compare(self, identifiers: list[str]) -> dict[str, Any]:
        summaries = []
        for ident in identifiers:
            resolved = self.sync.resolve_and_register(ident)
            latest = self.store.latest_analysis(resolved["wallet"])
            if not latest:
                # Auto-run if missing
                log.info("No cached analysis for %s — running now", ident)
                result = self.run(ident)
                summaries.append(
                    json.loads((self.reports_dir / result["summary"]["username"] / "summary.json").read_text())
                    if "username" in result["summary"]
                    else result["summary"]
                )
                # re-attach markets from file if needed — summary slim already ok for compare
                continue
            # Prefer on-disk slim summary (has categories etc.)
            uname = latest.get("username") or resolved["username"]
            path = self.reports_dir / uname / "summary.json"
            if path.exists():
                summaries.append(json.loads(path.read_text()))
            else:
                summaries.append(latest["summary"])
        report = compare_traders(summaries)
        md = format_comparison(report)
        out = self.reports_dir / "comparisons"
        out.mkdir(parents=True, exist_ok=True)
        slug = "_vs_".join(s.get("username") or "trader" for s in summaries)
        (out / f"{slug}.json").write_text(json.dumps(report, indent=2))
        (out / f"{slug}.md").write_text(md)
        return {"report": report, "markdown": md, "path": str(out / f"{slug}.md")}
