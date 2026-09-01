from __future__ import annotations

import json
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any


def _d(value: str | int | float | Decimal) -> Decimal:
    return Decimal(str(value))


def _price_key(price: str | int | float | Decimal) -> str:
    return format(_d(price), "f")


@dataclass
class OrderBook:
    ticker: str
    yes_bids: dict[str, Decimal] = field(default_factory=dict)
    no_bids: dict[str, Decimal] = field(default_factory=dict)
    last_seq: int | None = None
    updated_ms: int = 0

    def load_snapshot(self, msg: dict[str, Any], *, updated_ms: int) -> None:
        self.yes_bids.clear()
        self.no_bids.clear()
        self._load_levels(self.yes_bids, msg.get("yes_dollars") or msg.get("yes") or [])
        self._load_levels(self.no_bids, msg.get("no_dollars") or msg.get("no") or [])
        self.updated_ms = updated_ms

    def apply_delta(self, msg: dict[str, Any], *, updated_ms: int) -> None:
        side = str(msg.get("side", "")).lower()
        book = self.yes_bids if side == "yes" else self.no_bids if side == "no" else None
        if book is None:
            return

        price_raw = msg.get("price_dollars")
        if price_raw is None and msg.get("price") is not None:
            price_raw = format(_d(msg["price"]) / Decimal(100), "f")
        if price_raw is None:
            return

        price = _price_key(price_raw)
        delta_raw = msg.get("delta_fp", msg.get("delta", "0"))
        delta = _d(delta_raw)
        new_qty = book.get(price, Decimal(0)) + delta
        if new_qty <= 0:
            book.pop(price, None)
        else:
            book[price] = new_qty
        self.updated_ms = updated_ms

    def _load_levels(self, book: dict[str, Decimal], levels: list) -> None:
        for level in levels:
            if not level or len(level) < 2:
                continue
            price_raw, qty_raw = level[0], level[1]
            if isinstance(price_raw, (int, float)) and price_raw > 1:
                price = _price_key(_d(price_raw) / Decimal(100))
            else:
                price = _price_key(price_raw)
            qty = _d(qty_raw)
            if qty > 0:
                book[price] = qty

    def best_yes_bid(self) -> tuple[Decimal | None, Decimal]:
        if not self.yes_bids:
            return None, Decimal(0)
        price = max(self.yes_bids, key=lambda p: _d(p))
        return _d(price), self.yes_bids[price]

    def best_yes_ask(self) -> tuple[Decimal | None, Decimal]:
        if not self.no_bids:
            return None, Decimal(0)
        no_bid_price = max(self.no_bids, key=lambda p: _d(p))
        yes_ask = Decimal(1) - _d(no_bid_price)
        return yes_ask, self.no_bids[no_bid_price]

    def yes_mid(self) -> Decimal | None:
        bid, _ = self.best_yes_bid()
        ask, _ = self.best_yes_ask()
        if bid is None and ask is None:
            return None
        if bid is None:
            return ask
        if ask is None:
            return bid
        return (bid + ask) / 2

    def spread(self) -> Decimal | None:
        bid, _ = self.best_yes_bid()
        ask, _ = self.best_yes_ask()
        if bid is None or ask is None:
            return None
        return ask - bid

    def is_bond(self, threshold: Decimal = Decimal("0.90")) -> bool:
        mid = self.yes_mid()
        if mid is None:
            return False
        return mid >= threshold or mid <= (Decimal(1) - threshold)

    def top_levels(self, depth: int = 10) -> dict[str, Any]:
        yes_sorted = sorted(self.yes_bids.items(), key=lambda x: _d(x[0]), reverse=True)[:depth]
        no_sorted = sorted(self.no_bids.items(), key=lambda x: _d(x[0]), reverse=True)[:depth]
        bid, bid_qty = self.best_yes_bid()
        ask, ask_qty = self.best_yes_ask()
        return {
            "ticker": self.ticker,
            "yes_bid": str(bid) if bid is not None else "",
            "yes_ask": str(ask) if ask is not None else "",
            "yes_mid": str(self.yes_mid()) if self.yes_mid() is not None else "",
            "spread": str(self.spread()) if self.spread() is not None else "",
            "yes_bid_qty": str(bid_qty),
            "yes_ask_qty": str(ask_qty),
            "is_bond": self.is_bond(),
            "yes_bids": [[p, str(q)] for p, q in yes_sorted],
            "no_bids": [[p, str(q)] for p, q in no_sorted],
            "updated_ms": self.updated_ms,
        }

    def full_json(self, depth: int = 20) -> str:
        return json.dumps(self.top_levels(depth), separators=(",", ":"))
