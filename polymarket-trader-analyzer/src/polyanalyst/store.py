"""SQLite persistence for trader histories and analysis runs."""

from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path
from typing import Any, Optional


SCHEMA = """
CREATE TABLE IF NOT EXISTS traders (
    wallet TEXT PRIMARY KEY,
    username TEXT,
    profile_json TEXT,
    created_at REAL,
    updated_at REAL
);

CREATE TABLE IF NOT EXISTS activity (
    wallet TEXT NOT NULL,
    row_key TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    type TEXT,
    side TEXT,
    asset TEXT,
    condition_id TEXT,
    size REAL,
    usdc_size REAL,
    price REAL,
    outcome TEXT,
    outcome_index INTEGER,
    title TEXT,
    slug TEXT,
    event_slug TEXT,
    transaction_hash TEXT,
    payload_json TEXT NOT NULL,
    PRIMARY KEY (wallet, row_key)
);
CREATE INDEX IF NOT EXISTS idx_activity_ts ON activity(wallet, timestamp);
CREATE INDEX IF NOT EXISTS idx_activity_type ON activity(wallet, type);

CREATE TABLE IF NOT EXISTS trades (
    wallet TEXT NOT NULL,
    row_key TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    side TEXT,
    asset TEXT,
    condition_id TEXT,
    size REAL,
    price REAL,
    outcome TEXT,
    outcome_index INTEGER,
    title TEXT,
    slug TEXT,
    event_slug TEXT,
    transaction_hash TEXT,
    payload_json TEXT NOT NULL,
    PRIMARY KEY (wallet, row_key)
);
CREATE INDEX IF NOT EXISTS idx_trades_ts ON trades(wallet, timestamp);
CREATE INDEX IF NOT EXISTS idx_trades_market ON trades(wallet, condition_id);

CREATE TABLE IF NOT EXISTS closed_positions (
    wallet TEXT NOT NULL,
    asset TEXT NOT NULL,
    condition_id TEXT,
    timestamp INTEGER,
    realized_pnl REAL,
    avg_price REAL,
    total_bought REAL,
    title TEXT,
    outcome TEXT,
    event_slug TEXT,
    payload_json TEXT NOT NULL,
    PRIMARY KEY (wallet, asset)
);

CREATE TABLE IF NOT EXISTS open_positions (
    wallet TEXT NOT NULL,
    asset TEXT NOT NULL,
    condition_id TEXT,
    size REAL,
    avg_price REAL,
    current_value REAL,
    cash_pnl REAL,
    realized_pnl REAL,
    title TEXT,
    outcome TEXT,
    event_slug TEXT,
    payload_json TEXT NOT NULL,
    PRIMARY KEY (wallet, asset)
);

CREATE TABLE IF NOT EXISTS sync_state (
    wallet TEXT PRIMARY KEY,
    last_activity_ts INTEGER,
    last_trade_ts INTEGER,
    last_full_sync_at REAL,
    last_incremental_at REAL,
    activity_count INTEGER,
    trade_count INTEGER,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS analysis_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    wallet TEXT NOT NULL,
    username TEXT,
    created_at REAL NOT NULL,
    summary_json TEXT NOT NULL,
    strategy_md TEXT,
    validation_json TEXT
);
CREATE INDEX IF NOT EXISTS idx_runs_wallet ON analysis_runs(wallet, created_at DESC);
"""


class Store:
    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    def upsert_trader(self, wallet: str, username: str, profile: dict) -> None:
        now = time.time()
        self.conn.execute(
            """
            INSERT INTO traders(wallet, username, profile_json, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(wallet) DO UPDATE SET
              username=excluded.username,
              profile_json=excluded.profile_json,
              updated_at=excluded.updated_at
            """,
            (wallet.lower(), username, json.dumps(profile), now, now),
        )
        self.conn.commit()

    def list_traders(self) -> list[dict]:
        rows = self.conn.execute(
            "SELECT wallet, username, updated_at FROM traders ORDER BY updated_at DESC"
        ).fetchall()
        return [dict(r) for r in rows]

    def get_sync_state(self, wallet: str) -> Optional[dict]:
        row = self.conn.execute(
            "SELECT * FROM sync_state WHERE wallet=?", (wallet.lower(),)
        ).fetchone()
        return dict(row) if row else None

    def set_sync_state(self, wallet: str, **fields: Any) -> None:
        existing = self.get_sync_state(wallet) or {
            "wallet": wallet.lower(),
            "last_activity_ts": 0,
            "last_trade_ts": 0,
            "last_full_sync_at": None,
            "last_incremental_at": None,
            "activity_count": 0,
            "trade_count": 0,
            "notes": None,
        }
        existing.update(fields)
        existing["wallet"] = wallet.lower()
        self.conn.execute(
            """
            INSERT INTO sync_state(
              wallet, last_activity_ts, last_trade_ts, last_full_sync_at,
              last_incremental_at, activity_count, trade_count, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(wallet) DO UPDATE SET
              last_activity_ts=excluded.last_activity_ts,
              last_trade_ts=excluded.last_trade_ts,
              last_full_sync_at=excluded.last_full_sync_at,
              last_incremental_at=excluded.last_incremental_at,
              activity_count=excluded.activity_count,
              trade_count=excluded.trade_count,
              notes=excluded.notes
            """,
            (
                existing["wallet"],
                existing.get("last_activity_ts") or 0,
                existing.get("last_trade_ts") or 0,
                existing.get("last_full_sync_at"),
                existing.get("last_incremental_at"),
                existing.get("activity_count") or 0,
                existing.get("trade_count") or 0,
                existing.get("notes"),
            ),
        )
        self.conn.commit()

    def upsert_activity(self, wallet: str, rows: list[dict]) -> int:
        from .client import _row_key

        cur = self.conn.cursor()
        n = 0
        for r in rows:
            key = _row_key(r)
            cur.execute(
                """
                INSERT INTO activity(
                  wallet, row_key, timestamp, type, side, asset, condition_id,
                  size, usdc_size, price, outcome, outcome_index, title, slug,
                  event_slug, transaction_hash, payload_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(wallet, row_key) DO UPDATE SET
                  payload_json=excluded.payload_json
                """,
                (
                    wallet.lower(),
                    key,
                    int(r.get("timestamp") or 0),
                    r.get("type"),
                    r.get("side"),
                    r.get("asset"),
                    r.get("conditionId"),
                    float(r.get("size") or 0),
                    float(r.get("usdcSize") or 0),
                    float(r.get("price") or 0) if r.get("price") is not None else None,
                    r.get("outcome"),
                    r.get("outcomeIndex"),
                    r.get("title"),
                    r.get("slug"),
                    r.get("eventSlug"),
                    r.get("transactionHash"),
                    json.dumps(r),
                ),
            )
            n += cur.rowcount
        self.conn.commit()
        return n

    def upsert_trades(self, wallet: str, rows: list[dict]) -> int:
        from .client import _row_key

        cur = self.conn.cursor()
        n = 0
        for r in rows:
            key = _row_key(r)
            cur.execute(
                """
                INSERT INTO trades(
                  wallet, row_key, timestamp, side, asset, condition_id, size, price,
                  outcome, outcome_index, title, slug, event_slug, transaction_hash,
                  payload_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(wallet, row_key) DO UPDATE SET
                  payload_json=excluded.payload_json
                """,
                (
                    wallet.lower(),
                    key,
                    int(r.get("timestamp") or 0),
                    r.get("side"),
                    r.get("asset"),
                    r.get("conditionId"),
                    float(r.get("size") or 0),
                    float(r.get("price") or 0),
                    r.get("outcome"),
                    r.get("outcomeIndex"),
                    r.get("title"),
                    r.get("slug"),
                    r.get("eventSlug"),
                    r.get("transactionHash"),
                    json.dumps(r),
                ),
            )
            n += cur.rowcount
        self.conn.commit()
        return n

    def replace_closed_positions(self, wallet: str, rows: list[dict]) -> None:
        w = wallet.lower()
        self.conn.execute("DELETE FROM closed_positions WHERE wallet=?", (w,))
        cur = self.conn.cursor()
        for r in rows:
            cur.execute(
                """
                INSERT INTO closed_positions(
                  wallet, asset, condition_id, timestamp, realized_pnl, avg_price,
                  total_bought, title, outcome, event_slug, payload_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    w,
                    r.get("asset") or "",
                    r.get("conditionId"),
                    int(r.get("timestamp") or 0),
                    float(r.get("realizedPnl") or 0),
                    float(r.get("avgPrice") or 0),
                    float(r.get("totalBought") or 0),
                    r.get("title"),
                    r.get("outcome"),
                    r.get("eventSlug"),
                    json.dumps(r),
                ),
            )
        self.conn.commit()

    def replace_open_positions(self, wallet: str, rows: list[dict]) -> None:
        w = wallet.lower()
        self.conn.execute("DELETE FROM open_positions WHERE wallet=?", (w,))
        cur = self.conn.cursor()
        for r in rows:
            cur.execute(
                """
                INSERT INTO open_positions(
                  wallet, asset, condition_id, size, avg_price, current_value,
                  cash_pnl, realized_pnl, title, outcome, event_slug, payload_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    w,
                    r.get("asset") or "",
                    r.get("conditionId"),
                    float(r.get("size") or 0),
                    float(r.get("avgPrice") or 0),
                    float(r.get("currentValue") or 0),
                    float(r.get("cashPnl") or 0),
                    float(r.get("realizedPnl") or 0),
                    r.get("title"),
                    r.get("outcome"),
                    r.get("eventSlug"),
                    json.dumps(r),
                ),
            )
        self.conn.commit()

    def load_activity(self, wallet: str) -> list[dict]:
        rows = self.conn.execute(
            "SELECT payload_json FROM activity WHERE wallet=? ORDER BY timestamp ASC",
            (wallet.lower(),),
        ).fetchall()
        return [json.loads(r["payload_json"]) for r in rows]

    def load_trades(self, wallet: str) -> list[dict]:
        rows = self.conn.execute(
            "SELECT payload_json FROM trades WHERE wallet=? ORDER BY timestamp ASC",
            (wallet.lower(),),
        ).fetchall()
        return [json.loads(r["payload_json"]) for r in rows]

    def load_closed_positions(self, wallet: str) -> list[dict]:
        rows = self.conn.execute(
            "SELECT payload_json FROM closed_positions WHERE wallet=? ORDER BY timestamp ASC",
            (wallet.lower(),),
        ).fetchall()
        return [json.loads(r["payload_json"]) for r in rows]

    def load_open_positions(self, wallet: str) -> list[dict]:
        rows = self.conn.execute(
            "SELECT payload_json FROM open_positions WHERE wallet=?",
            (wallet.lower(),),
        ).fetchall()
        return [json.loads(r["payload_json"]) for r in rows]

    def counts(self, wallet: str) -> dict[str, int]:
        w = wallet.lower()
        return {
            "activity": self.conn.execute(
                "SELECT COUNT(*) c FROM activity WHERE wallet=?", (w,)
            ).fetchone()["c"],
            "trades": self.conn.execute(
                "SELECT COUNT(*) c FROM trades WHERE wallet=?", (w,)
            ).fetchone()["c"],
            "closed_positions": self.conn.execute(
                "SELECT COUNT(*) c FROM closed_positions WHERE wallet=?", (w,)
            ).fetchone()["c"],
            "open_positions": self.conn.execute(
                "SELECT COUNT(*) c FROM open_positions WHERE wallet=?", (w,)
            ).fetchone()["c"],
        }

    def save_analysis(
        self,
        wallet: str,
        username: str,
        summary: dict,
        strategy_md: str,
        validation: dict,
    ) -> int:
        cur = self.conn.execute(
            """
            INSERT INTO analysis_runs(wallet, username, created_at, summary_json, strategy_md, validation_json)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                wallet.lower(),
                username,
                time.time(),
                json.dumps(summary),
                strategy_md,
                json.dumps(validation),
            ),
        )
        self.conn.commit()
        return int(cur.lastrowid)

    def latest_analysis(self, wallet: str) -> Optional[dict]:
        row = self.conn.execute(
            """
            SELECT * FROM analysis_runs WHERE wallet=? ORDER BY created_at DESC LIMIT 1
            """,
            (wallet.lower(),),
        ).fetchone()
        if not row:
            return None
        d = dict(row)
        d["summary"] = json.loads(d.pop("summary_json"))
        d["validation"] = json.loads(d.pop("validation_json") or "{}")
        return d

    def list_analyses(self, wallet: Optional[str] = None, limit: int = 20) -> list[dict]:
        if wallet:
            rows = self.conn.execute(
                """
                SELECT id, wallet, username, created_at FROM analysis_runs
                WHERE wallet=? ORDER BY created_at DESC LIMIT ?
                """,
                (wallet.lower(), limit),
            ).fetchall()
        else:
            rows = self.conn.execute(
                """
                SELECT id, wallet, username, created_at FROM analysis_runs
                ORDER BY created_at DESC LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(r) for r in rows]
