"""Mode-aware exit rules shared by backtest and paper auto-trader."""

from __future__ import annotations

import re
from dataclasses import dataclass

from suspension_lab.config import SCALP_TARGET_CENTS


@dataclass(frozen=True)
class ExitDecision:
    action: str  # "hold" | "exit"
    reason: str
    limit_cents: int | None = None


def scalp_target_cents(entry_cents: int, plus: int = SCALP_TARGET_CENTS) -> int:
    return min(entry_cents + plus, 99)


def is_total_05_ticker(ticker: str) -> bool:
    """Check if ticker is a totals O0.5 line (e.g. KXPERLIGA1TOTAL-...-1).
    
    O0.5 = strike 1, O1.5 = strike 2, O2.5 = strike 3, etc.
    This function returns True for O0.5 (strike 1) which should hold_bond after bonding.
    """
    if "TOTAL" not in ticker.upper():
        return False
    match = re.search(r"-(\d+)$", ticker)
    if match:
        strike_num = int(match.group(1))
        return strike_num == 1
    return False


def get_per_line_exit_mode(ticker: str, base_exit_mode: str, is_bonded: bool) -> str:
    """Determine exit mode based on per-line policy.
    
    Rules:
    - Totals with strike 0.5 (O0.5) that have already bonded → hold_bond, never scalp +7
    - ML (moneyline) and O1.5+ keep their base exit mode (scalp / var_watch)
    """
    if is_total_05_ticker(ticker) and is_bonded:
        return "hold_bond"
    return base_exit_mode


def is_bond_spoof_bid(
    *,
    peak_cents: int,
    current_bid_cents: int,
    current_ask_cents: int | None,
    bid_qty: float,
    peak_bond_cents: int = 95,
    max_spoof_qty: float = 100,
    min_spread_cents: int = 10,
) -> bool:
    """
    Lowball bid on a bonded market while ask stays high — not a real VAR.
    Example: bid 75¢ x 7.6, ask 99¢ x 105 on O0.5 after goal confirmed.
    """
    if peak_cents < peak_bond_cents:
        return False
    if current_ask_cents is None or current_ask_cents < peak_bond_cents:
        return False
    if current_bid_cents >= current_ask_cents - min_spread_cents:
        return False
    return bid_qty <= max_spoof_qty


def check_var_protection(
    *,
    exit_mode: str,
    entry_cents: int,
    peak_cents: int,
    current_bid_cents: int,
    seconds_held: float,
    current_ask_cents: int | None = None,
    bid_qty: float = 0,
    peak_drop_cents: int = 10,
    limbo_sec: float = 25.0,
    limbo_max_gain: int = 3,
    limbo_peak_cap: int = 88,
) -> ExitDecision | None:
    """VAR / cancelled-goal protection — exit fast, accept small scratch."""
    if is_bond_spoof_bid(
        peak_cents=peak_cents,
        current_bid_cents=current_bid_cents,
        current_ask_cents=current_ask_cents,
        bid_qty=bid_qty,
    ):
        return None

    drop = peak_cents - current_bid_cents
    if drop >= peak_drop_cents and seconds_held >= 2:
        return ExitDecision("exit", f"VAR revert -{drop}c from peak {peak_cents}c")

    if exit_mode == "var_watch" and seconds_held >= limbo_sec:
        if peak_cents < limbo_peak_cap and current_bid_cents <= entry_cents + limbo_max_gain:
            return ExitDecision(
                "exit",
                f"VAR limbo @ {int(limbo_sec)}s (peak {peak_cents}c, bid {current_bid_cents}c)",
            )
        if peak_cents - current_bid_cents >= 8:
            return ExitDecision("exit", f"trailing stop from peak {peak_cents}c")

    return None


def check_exit(
    *,
    exit_mode: str,
    entry_cents: int,
    current_bid_cents: int,
    peak_cents: int,
    seconds_held: float,
    current_ask_cents: int | None = None,
    bid_qty: float = 0,
    scalp_plus: int = SCALP_TARGET_CENTS,
    bond_cents: int = 95,
    stall_sec: float = 20.0,
) -> ExitDecision:
    """Live/paper exit check on each book update."""
    var = check_var_protection(
        exit_mode=exit_mode,
        entry_cents=entry_cents,
        peak_cents=peak_cents,
        current_bid_cents=current_bid_cents,
        seconds_held=seconds_held,
        current_ask_cents=current_ask_cents,
        bid_qty=bid_qty,
    )
    if var:
        return var

    target = scalp_target_cents(entry_cents, scalp_plus)
    if current_bid_cents >= target and exit_mode != "hold_bond":
        return ExitDecision("exit", f"scalp target {target}c", limit_cents=target)

    if exit_mode == "hold_bond" and current_bid_cents >= bond_cents:
        return ExitDecision("exit", f"bond {current_bid_cents}c", limit_cents=current_bid_cents)

    if exit_mode == "scalp" and seconds_held >= stall_sec:
        gained = current_bid_cents - entry_cents
        if peak_cents <= entry_cents or gained < 3:
            return ExitDecision("exit", f"stall @ {int(stall_sec)}s", limit_cents=current_bid_cents)

    if seconds_held >= 45 and exit_mode != "hold_bond":
        return ExitDecision("exit", "time stop 45s", limit_cents=current_bid_cents)

    return ExitDecision("hold", "monitoring")
