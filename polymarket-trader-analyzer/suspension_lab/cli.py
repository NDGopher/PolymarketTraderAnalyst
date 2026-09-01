from __future__ import annotations

from pathlib import Path

import typer

from suspension_lab.config import BOOK_SAMPLE_MS, LabConfig
from suspension_lab.ui import run_app

app = typer.Typer(add_completion=False, no_args_is_help=True, help="Manual suspension edge lab")


@app.command("run")
def run_lab(
    tickers: str = typer.Argument(..., help="Comma-separated Kalshi tickers (O/U 2.5, 3.5, 4.5, …)"),
    game: str = typer.Option("", "--game", "-g", help="Label for this match, e.g. Parma-Cremonese"),
    demo: bool = typer.Option(False, "--demo", help="Use Kalshi demo environment"),
    rest_only: bool = typer.Option(False, "--rest-only", help="Skip WS; poll REST orderbook (no auth needed)"),
    poll_ms: int = typer.Option(BOOK_SAMPLE_MS, "--poll-ms", help="Book sample interval in ms"),
    output_dir: Path = typer.Option(
        Path("data/suspension_lab/sessions"),
        "--output-dir",
        help="Where session CSVs are written",
    ),
) -> None:
    """Launch the manual B/F click logger with live Kalshi orderbooks."""
    ticker_list = [t.strip() for t in tickers.split(",") if t.strip()]
    config = LabConfig.from_env(
        ticker_list,
        game_label=game,
        demo=demo,
        use_ws=not rest_only,
        poll_ms=poll_ms,
        output_dir=output_dir,
    )
    if not config.has_ws_auth and not rest_only:
        typer.echo(
            "No KALSHI_API_KEY_ID + KALSHI_PRIVATE_KEY_PATH — using REST polling (200ms). "
            "Set env vars for WebSocket deltas.",
            err=True,
        )
        config.use_ws = False
    typer.echo(f"Tickers: {', '.join(ticker_list)}")
    typer.echo(f"Output: {config.output_dir}")
    run_app(config)


if __name__ == "__main__":
    app()
