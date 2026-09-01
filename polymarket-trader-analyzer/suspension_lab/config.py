from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


WS_PATH = "/trade-api/ws/v2"
REST_BASE_PROD = "https://api.elections.kalshi.com/trade-api/v2"
REST_BASE_DEMO = "https://demo-api.kalshi.co/trade-api/v2"
WS_URL_PROD = "wss://external-api-ws.kalshi.com/trade-api/ws/v2"
WS_URL_DEMO = "wss://external-api-ws.demo.kalshi.co/trade-api/ws/v2"

BOND_MID_THRESHOLD = 0.90
MARKOUT_SECONDS = (1, 3, 5, 10, 30)
BOOK_SAMPLE_MS = 200


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
        return cls(
            tickers=tickers,
            game_label=game_label,
            demo=demo,
            use_ws=use_ws,
            poll_ms=poll_ms,
            output_dir=Path(output_dir or "data/suspension_lab/sessions"),
            api_key_id=os.environ.get("KALSHI_API_KEY_ID", os.environ.get("KALSHI_API_KEY", "")),
            private_key_path=os.environ.get(
                "KALSHI_PRIVATE_KEY_PATH",
                os.environ.get("KALSHI_PRIVATE_KEY_FILE", ""),
            ),
        )

    @property
    def ws_url(self) -> str:
        return WS_URL_DEMO if self.demo else WS_URL_PROD

    @property
    def rest_base(self) -> str:
        return REST_BASE_DEMO if self.demo else REST_BASE_PROD

    @property
    def has_ws_auth(self) -> bool:
        return bool(self.api_key_id and self.private_key_path and Path(self.private_key_path).exists())
