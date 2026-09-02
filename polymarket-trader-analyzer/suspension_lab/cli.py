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
    auto_discover: bool = typer.Option(
        True,
        "--auto-discover/--no-auto-discover",
        help="Auto-discover soccer games when no tickers provided",
    ),
    max_games: int = typer.Option(
        5,
        "--max-games",
        help="Max number of games to auto-discover",
    ),
    min_volume: float = typer.Option(
        50.0,
        "--min-volume",
        help="Min volume threshold for auto-discovery",
    ),
) -> None:
    """Launch the manual B/F click logger with live Kalshi orderbooks."""
    load_project_env()

    ticker_str = (tickers or os.environ.get("LAB_TICKERS", "")).strip()
    ticker_list = [t.strip() for t in ticker_str.split(",") if t.strip()] if ticker_str else []

    if ticker_str.lower() == "run":
        typer.echo("LAB_TICKERS must be Kalshi tickers, not the word 'run'.", err=True)
        raise typer.Exit(1)

    discovered_games = []
    if not ticker_list and auto_discover:
        from suspension_lab.soccer_discovery import discover_tickers_for_lab

        rest_base = (
            "https://demo-api.kalshi.co/trade-api/v2"
            if demo
            else "https://api.elections.kalshi.com/trade-api/v2"
        )
        typer.echo("\n--- Auto-discovering soccer games ---", err=True)
        ticker_list, discovery_log, discovered_games = discover_tickers_for_lab(
            rest_base=rest_base,
            min_volume=min_volume,
            max_games=max_games,
        )
        typer.echo(discovery_log, err=True)
        typer.echo("---\n", err=True)

        if ticker_list:
            typer.echo(
                f"Auto-discovered {len(ticker_list)} tickers from {len(discovered_games)} games.",
                err=True,
            )
        else:
            typer.echo(
                "No soccer games with sufficient volume found. "
                "Add tickers in the UI while the session runs.",
                err=True,
            )
    elif not ticker_list:
        typer.echo(
            "No LAB_TICKERS in .env and auto-discover disabled — starting with empty list. "
            "Add tickers in the UI while the session runs.",
            err=True,
        )

    game_label = (game or os.environ.get("LAB_GAME", "")).strip()
    if not game_label and discovered_games:
        game_label = " | ".join(g.title[:30] for g in discovered_games[:2])
        if len(discovered_games) > 2:
            game_label += f" +{len(discovered_games) - 2}"

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
