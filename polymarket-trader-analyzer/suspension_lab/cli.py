from __future__ import annotations

import os
from pathlib import Path

import typer

from suspension_lab.config import BOOK_SAMPLE_MS, LabConfig
from suspension_lab.env_loader import env_status_message, load_project_env, project_root
from suspension_lab.soccer_discovery import (
    discover_soccer_games,
    format_discovery_log,
    format_slate_digest,
    needs_auto_discover,
)

load_project_env()


def main(
    tickers: str = typer.Option(
        "",
        "--tickers",
        "-t",
        envvar="LAB_TICKERS",
        help="Optional pin. Empty / placeholder / 'auto' → discover today's soccer",
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
        help="Auto-discover today's soccer when LAB_TICKERS is empty or a placeholder",
    ),
    max_games: int = typer.Option(5, "--max-games", help="Max games to auto-fund"),
    min_volume: float = typer.Option(50.0, "--min-volume", help="Min volume for auto-pick"),
    headless: bool = typer.Option(False, "--headless", help="Unattended paper logger (no UI)"),
    digest_only: bool = typer.Option(False, "--digest-only", help="Print today's slate and exit"),
) -> None:
    """Soccer paper tape: auto-discover today, log books, scalp GOAL jumps. No live bets."""
    load_project_env()

    ticker_str = (tickers or os.environ.get("LAB_TICKERS", "")).strip()
    ticker_list = [t.strip() for t in ticker_str.split(",") if t.strip()] if ticker_str else []
    if ticker_str.lower() == "run":
        ticker_list = []

    rest_base = (
        "https://demo-api.kalshi.co/trade-api/v2"
        if demo
        else "https://api.elections.kalshi.com/trade-api/v2"
    )

    discovered_games = []
    discovery_result = None
    if auto_discover and needs_auto_discover(ticker_list):
        typer.echo("\n--- Auto-discovering today's soccer ---", err=True)
        discovery_result = discover_soccer_games(
            rest_base=rest_base,
            min_volume=min_volume,
            max_games=max_games,
        )
        ticker_list = discovery_result.tickers
        discovered_games = discovery_result.games
        typer.echo(format_discovery_log(discovery_result), err=True)
        typer.echo("---\n", err=True)
        if ticker_list:
            typer.echo(
                f"Auto-funded {len(ticker_list)} tickers from {len(discovered_games)} games (paper).",
                err=True,
            )
        else:
            typer.echo(
                "No today/tonight soccer tape. Auto-discover is ready for the next slate.",
                err=True,
            )
    elif not ticker_list:
        typer.echo("No tickers and auto-discover disabled — add books in the UI.", err=True)

    if digest_only:
        if discovery_result is None:
            discovery_result = discover_soccer_games(
                rest_base=rest_base, min_volume=min_volume, max_games=max_games
            )
        typer.echo(format_slate_digest(discovery_result))
        raise typer.Exit(0)

    if headless:
        from suspension_lab.paper_logger import run_paper_logger

        game_label = (game or os.environ.get("LAB_GAME", "")).strip()
        if not game_label and discovered_games:
            game_label = " | ".join(g.title[:28] for g in discovered_games[:2])
        if not ticker_list:
            raise typer.Exit(0)
        run_paper_logger(
            tickers=ticker_list,
            games=discovered_games,
            game_label=game_label,
            demo=demo,
            rest_only=rest_only,
            poll_ms=poll_ms,
            output_dir=output_dir,
            duration_seconds=0,
        )
        return

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
    config.games = discovered_games
    config.paper_enabled = True
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
    typer.echo("Mode: PAPER ONLY (live=False)")

    from suspension_lab.ui import run_app

    run_app(config)


if __name__ == "__main__":
    typer.run(main)
