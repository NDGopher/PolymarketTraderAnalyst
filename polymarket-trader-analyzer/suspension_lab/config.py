from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from suspension_lab.env_loader import (
    load_project_env,
    resolve_api_key_id,
    resolve_private_key_path,
    resolve_private_key_pem,
)


WS_PATH = "/trade-api/ws/v2"
REST_BASE_PROD = "https://api.elections.kalshi.com/trade-api/v2"
REST_BASE_DEMO = "https://demo-api.kalshi.co/trade-api/v2"
WS_URL_PROD = "wss://api.elections.kalshi.com/trade-api/ws/v2"
WS_URL_PROD_ALT = "wss://external-api-ws.kalshi.com/trade-api/ws/v2"
WS_URL_DEMO = "wss://external-api-ws.demo.kalshi.co/trade-api/ws/v2"

BOND_MID_THRESHOLD = 0.90
TIGHT_SPREAD_CENTS = 3
WIDE_SPREAD_CENTS = 10
MARKOUT_SECONDS = (1, 3, 5, 10, 30)
BOOK_SAMPLE_MS = 200

# Live goal-signal detector (bid momentum, not ask-only scares)
GOAL_BID_JUMP_CENTS = 10
GOAL_MIN_BID_QTY = 100
GOAL_MIN_PREV_BID_CENTS = 15  # ignore startup / bond noise
GOAL_ASK_CONFIRM_CENTS = 3  # ask must step up with bid (full book reprice)
GOAL_SIGNAL_COOLDOWN_MS = 45_000
GOAL_HIGHLIGHT_SECONDS = 45
GOAL_ASK_LOOKBACK_MS = 2_500  # ask-led-bid: ask moved in prior ~2.5s
GOAL_ASK_LOOKBACK_MAX_BID_DRIFT_CENTS = 5  # allow small bid drift while ask leads
GOAL_SPREAD_BLOWOUT_CENTS = 12  # tight book -> wide = books pulled (goal/suspension)
GOAL_MIN_BLOWOUT_JUMP_CENTS = 6
# +10c within this window is a GOAL only if ask confirms (+3c) or spread blows.
GOAL_FAST_WINDOW_MS = 4_000
# delayed_grind only for walks that take longer than ~6-8s (or no ask/blowout).
GOAL_DELAYED_WINDOW_MS = 8_000
GOAL_DELAYED_MIN_MS = 6_500
BOND_HOLD_BID_CENTS = 88  # bid here -> hold to 99 / resolution, not +7 scalp
VAR_REVERT_CENTS = 10  # peak-to-trough drop triggers VAR/cancelled alert
VAR_REVERT_WINDOW_MS = 120_000

# Paper auto-trader (off by default — set LAB_TRADER_ENABLED=1 to paper-trade)
TRADER_DEFAULT_CONTRACTS = 50
TRADER_DEFAULT_BID_OFFSET_CENTS = 1


@dataclass
class LabConfig:
    tickers: list[str]
    game_label: str = ""
    demo: bool = False
    use_ws: bool = True
    poll_ms: int = BOOK_SAMPLE_MS
    output_dir: Path = Path("data/suspension_lab/sessions")
    api_key_id: str = ""
    private_key_path: str = ""
    private_key_pem: str = ""
    games: list[Any] = field(default_factory=list)
    paper_enabled: bool = False

    @classmethod
    def from_env(
        cls,
        tickers: list[str],
        *,
        game_label: str = "",
        demo: bool = False,
        use_ws: bool = True,
        poll_ms: int = BOOK_SAMPLE_MS,
        output_dir: str | Path | None = None,
    ) -> LabConfig:
        load_project_env()
        game = game_label
        demo_flag = demo or os.environ.get("KALSHI_DEMO", "").lower() in ("1", "true", "yes")
        pem = resolve_private_key_pem()
        key_path = resolve_private_key_path()
        return cls(
            tickers=tickers,
            game_label=game,
            demo=demo_flag,
            use_ws=use_ws,
            poll_ms=poll_ms,
            output_dir=Path(output_dir or os.environ.get("LAB_OUTPUT_DIR", "data/suspension_lab/sessions")),
            api_key_id=resolve_api_key_id(),
            private_key_path=key_path,
            private_key_pem=pem,
        )

    @property
    def ws_url(self) -> str:
        return WS_URL_DEMO if self.demo else WS_URL_PROD

    @property
    def rest_base(self) -> str:
        return REST_BASE_DEMO if self.demo else REST_BASE_PROD

    @property
    def has_ws_auth(self) -> bool:
        if not self.api_key_id:
            return False
        if self.private_key_pem:
            return True
        return bool(self.private_key_path and Path(self.private_key_path).exists())
