"""Sync orchestration: full + incremental history pulls."""

from __future__ import annotations

import logging
import time
from typing import Any, Optional

from .client import PolymarketClient
from .store import Store

log = logging.getLogger(__name__)


class SyncService:
    def __init__(self, client: PolymarketClient, store: Store) -> None:
        self.client = client
        self.store = store

    def resolve_and_register(self, identifier: str) -> dict[str, Any]:
        resolved = self.client.resolve_trader(identifier)
        self.store.upsert_trader(resolved["wallet"], resolved["username"], resolved.get("profile") or {})
        return resolved

    def full_sync(self, wallet: str, username: str = "") -> dict[str, Any]:
        wallet = wallet.lower()
        log.info("Full sync starting for %s", wallet)
        t0 = time.time()

        activity = self.client.fetch_activity(wallet, start_ts=1)
        log.info("Fetched %s activity rows", len(activity))
        self.store.upsert_activity(wallet, activity)

        # Prefer deriving trades from activity TRADE rows for consistency,
        # but also pull /trades to capture maker fills activity may miss.
        trades = self.client.fetch_trades(wallet, start_ts=1)
        log.info("Fetched %s trade rows", len(trades))
        self.store.upsert_trades(wallet, trades)

        closed = self.client.fetch_closed_positions(wallet)
        log.info("Fetched %s closed positions", len(closed))
        self.store.replace_closed_positions(wallet, closed)

        opened = self.client.fetch_positions(wallet)
        log.info("Fetched %s open positions", len(opened))
        self.store.replace_open_positions(wallet, opened)

        last_act = max((int(r.get("timestamp") or 0) for r in activity), default=0)
        last_tr = max((int(r.get("timestamp") or 0) for r in trades), default=0)
        counts = self.store.counts(wallet)
        self.store.set_sync_state(
            wallet,
            last_activity_ts=last_act,
            last_trade_ts=last_tr,
            last_full_sync_at=time.time(),
            last_incremental_at=time.time(),
            activity_count=counts["activity"],
            trade_count=counts["trades"],
            notes=f"full_sync_seconds={time.time()-t0:.1f}",
        )
        return {
            "wallet": wallet,
            "username": username,
            "mode": "full",
            "duration_s": round(time.time() - t0, 2),
            "counts": counts,
            "last_activity_ts": last_act,
            "last_trade_ts": last_tr,
        }

    def incremental_sync(self, wallet: str, overlap_seconds: int = 3600) -> dict[str, Any]:
        wallet = wallet.lower()
        state = self.store.get_sync_state(wallet)
        if not state or not state.get("last_activity_ts"):
            return self.full_sync(wallet)

        t0 = time.time()
        start_act = max(1, int(state["last_activity_ts"]) - overlap_seconds)
        start_tr = max(1, int(state.get("last_trade_ts") or state["last_activity_ts"]) - overlap_seconds)
        log.info("Incremental sync for %s from activity_ts>=%s", wallet, start_act)

        activity = self.client.fetch_activity(wallet, start_ts=start_act)
        self.store.upsert_activity(wallet, activity)

        trades = self.client.fetch_trades(wallet, start_ts=start_tr)
        self.store.upsert_trades(wallet, trades)

        # Positions snapshots are small — always refresh
        closed = self.client.fetch_closed_positions(wallet)
        self.store.replace_closed_positions(wallet, closed)
        opened = self.client.fetch_positions(wallet)
        self.store.replace_open_positions(wallet, opened)

        last_act = max(
            int(state["last_activity_ts"]),
            max((int(r.get("timestamp") or 0) for r in activity), default=0),
        )
        last_tr = max(
            int(state.get("last_trade_ts") or 0),
            max((int(r.get("timestamp") or 0) for r in trades), default=0),
        )
        counts = self.store.counts(wallet)
        self.store.set_sync_state(
            wallet,
            last_activity_ts=last_act,
            last_trade_ts=last_tr,
            last_full_sync_at=state.get("last_full_sync_at"),
            last_incremental_at=time.time(),
            activity_count=counts["activity"],
            trade_count=counts["trades"],
            notes=f"incremental_sync_seconds={time.time()-t0:.1f}; new_activity={len(activity)}; new_trades={len(trades)}",
        )
        return {
            "wallet": wallet,
            "mode": "incremental",
            "duration_s": round(time.time() - t0, 2),
            "fetched_activity": len(activity),
            "fetched_trades": len(trades),
            "counts": counts,
            "last_activity_ts": last_act,
            "last_trade_ts": last_tr,
        }

    def sync(self, identifier: str, force_full: bool = False) -> dict[str, Any]:
        resolved = self.resolve_and_register(identifier)
        wallet = resolved["wallet"]
        state = self.store.get_sync_state(wallet)
        if force_full or not state or not state.get("last_activity_ts"):
            result = self.full_sync(wallet, resolved["username"])
        else:
            result = self.incremental_sync(wallet)
        result["username"] = resolved["username"]
        result["resolved"] = {
            "username": resolved["username"],
            "wallet": wallet,
        }
        return result
