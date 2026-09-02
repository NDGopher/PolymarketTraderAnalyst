"""Paper make quotes around a goal jump — never mid-only.

PR #6 scalp: enter bid+1 after a book-detected GOAL, target +7.
Fee is reported for the tape; it is not a default deny.
"""

from __future__ import annotations

from dataclasses import dataclass


FEE_RATE = 0.07


@dataclass(frozen=True)
class MakeQuote:
    entry_cents: int | None
    reason: str
    fee_cents: float
    skipped: bool
    skip_reason: str = ""

    @property
    def used_mid(self) -> bool:
        return False


def kalshi_fee_cents(price_cents: int) -> float:
    """Per-contract fee in cents. Peaks at 50¢ (~1.75¢)."""
    p = max(0.01, min(0.99, price_cents / 100.0))
    return 100.0 * FEE_RATE * p * (1.0 - p)


def make_around_jump(
    bid_cents: int,
    ask_cents: int | None = None,
    *,
    bid_offset: int = 1,
) -> MakeQuote:
    """Paper make quote after a bid-jump GOAL. Never returns mid. Never fee-skip deny."""
    if bid_cents <= 0:
        return MakeQuote(None, "no_bid", 0.0, True, "no_bid")

    entry = min(bid_cents + bid_offset, 99)
    if ask_cents is not None and ask_cents > 0:
        entry = min(entry, max(ask_cents - 1, bid_cents))

    fee = kalshi_fee_cents(entry)
    return MakeQuote(entry, "make_bid_plus_1", fee, False)
