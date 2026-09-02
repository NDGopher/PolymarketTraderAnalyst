"""Fee-aware make quotes around a goal jump — never mid-only.

Kalshi-style fees peak at 50¢ (∝ p·(1-p)). After a book-detected GOAL we
make on the new bid (bid+1¢ queue), not the mid. Near 50¢ we skip unless
the post-jump spread still pays the fee.
"""

from __future__ import annotations

from dataclasses import dataclass


FEE_RATE = 0.07
FEE_PEAK_LOW = 45
FEE_PEAK_HIGH = 55
MIN_SPREAD_AWAY_FROM_FIFTY = 3
MIN_SPREAD_NEAR_FIFTY = 6


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
    """Paper make quote after a bid-jump GOAL. Never returns mid."""
    if bid_cents <= 0:
        return MakeQuote(None, "no_bid", 0.0, True, "no_bid")

    entry = min(bid_cents + bid_offset, 99)
    if ask_cents is not None and ask_cents > 0:
        entry = min(entry, max(ask_cents - 1, bid_cents))

    fee = kalshi_fee_cents(entry)
    spread = (ask_cents - bid_cents) if ask_cents is not None else None
    near_fifty = FEE_PEAK_LOW <= entry <= FEE_PEAK_HIGH
    min_spread = MIN_SPREAD_NEAR_FIFTY if near_fifty else MIN_SPREAD_AWAY_FROM_FIFTY

    if spread is not None and spread < min_spread:
        why = "skip_fee_peak_50c" if near_fifty else "skip_tight_spread"
        return MakeQuote(None, why, fee, True, why)

    if near_fifty and fee >= 1.5 and (spread is None or spread < MIN_SPREAD_NEAR_FIFTY + 2):
        return MakeQuote(None, "skip_fee_peak_50c", fee, True, "skip_fee_peak_50c")

    reason = "make_bid_plus_1_near_50c" if near_fifty else "make_bid_plus_1"
    return MakeQuote(entry, reason, fee, False)
