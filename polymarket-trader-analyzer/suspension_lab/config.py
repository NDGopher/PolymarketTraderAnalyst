from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

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
        game = game_label or os.environ.get("LAB_GAME", "")
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
