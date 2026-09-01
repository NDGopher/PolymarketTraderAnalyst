from __future__ import annotations

import os
from pathlib import Path

import typer

from suspension_lab.config import BOOK_SAMPLE_MS, LabConfig
from suspension_lab.env_loader import env_status_message, load_project_env, project_root

load_project_env()


def main(
    tickers: str = typer.Option(
        "",
        "--tickers",
        "-t",
        envvar="LAB_TICKERS",
        help="Comma-separated Kalshi tickers (or set LAB_TICKERS in .env)",
    ),
    game: str = typer.Option("", "--game", "-g", envvar="LAB_GAME", help="Match label"),
    demo: bool = typer.Option(False, "--demo", help="Use Kalshi demo environment"),
    rest_only: bool = typer.Option(False, "--rest-only", help="Skip WS; poll REST orderbook"),
    poll_ms: int = typer.Option(BOOK_SAMPLE_MS, "--poll-ms", help="Book sample interval in ms"),
    output_dir: Path = typer.Option(
        Path("data/suspension_lab/sessions"),
        "--output-dir",
        help="Where session CSVs are written",
    ),
) -> None:
    """Launch the manual B/F click logger with live Kalshi orderbooks."""
    load_project_env()

    ticker_str = (tickers or os.environ.get("LAB_TICKERS", "")).strip()
    ticker_list = [t.strip() for t in ticker_str.split(",") if t.strip()] if ticker_str else []

    if ticker_str.lower() == "run":
        typer.echo("LAB_TICKERS must be Kalshi tickers, not the word 'run'.", err=True)
        raise typer.Exit(1)

    if not ticker_list:
        typer.echo(
            "No LAB_TICKERS in .env — starting with empty list. "
            "Add tickers in the UI while the session runs.",
            err=True,
        )

    game_label = (game or os.environ.get("LAB_GAME", "")).strip()

    config = LabConfig.from_env(
        ticker_list,
        game_label=game_label,
        demo=demo,
        use_ws=not rest_only,
        poll_ms=poll_ms,
        output_dir=output_dir,
    )
    if not config.has_ws_auth and not rest_only:
        typer.echo(
            "No Kalshi credentials in .env — using REST polling (~200ms).\n"
            "Add KALSHI_KEY_ID + KALSHI_PRIVATE_KEY to .env for WebSocket.",
            err=True,
        )
        config.use_ws = False

    typer.echo(env_status_message())
    typer.echo(f"Project: {project_root()}")
    typer.echo(f"Tickers: {', '.join(ticker_list) if ticker_list else '(add in UI)'}")
    typer.echo(f"Game: {config.game_label or '(unnamed)'}")
    typer.echo(f"Output: {config.output_dir}")
    typer.echo(f"Feed: {'WebSocket' if config.use_ws else 'REST polling'}")

    from suspension_lab.ui import run_app

    run_app(config)


if __name__ == "__main__":
    typer.run(main)
