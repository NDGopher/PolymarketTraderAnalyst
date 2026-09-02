from __future__ import annotations

from pathlib import Path

import typer

from suspension_lab.config import BOOK_SAMPLE_MS, LabConfig
from suspension_lab.env_loader import env_status_message, load_project_env, project_root
from suspension_lab.instance_lock import LabLockHeld, acquire_lab_lock
from suspension_lab.soccer_discovery import (
    discover_soccer_games,
    format_slate_digest,
    needs_auto_discover,
    parse_cli_tickers,
)

load_project_env()


def main(
    tickers: str = typer.Option(
        "",
        "--tickers",
        "-t",
        help="Optional explicit KX… pin. Empty / placeholder / yesterday → discover. "
        "Does not read LAB_TICKERS from .env.",
    ),
    game: str = typer.Option(
        "",
        "--game",
        "-g",
        help="Match label. Does not read LAB_GAME from .env.",
    ),
    demo: bool = typer.Option(False, "--demo", help="Use Kalshi demo environment"),
    rest_only: bool = typer.Option(
        False, "--rest-only", help="Explicit REST only. Live L2 is WS; this is not a fallback."
    ),
    poll_ms: int = typer.Option(BOOK_SAMPLE_MS, "--poll-ms", help="Tape sample interval in ms"),
    output_dir: Path = typer.Option(
        Path("data/suspension_lab/sessions"),
        "--output-dir",
        help="Where session CSVs are written",
    ),
    auto_discover: bool = typer.Option(
        True,
        "--auto-discover/--no-auto-discover",
        help="Empty start may discover once. Real KX --tickers never rediscover.",
    ),
    max_games: int = typer.Option(5, "--max-games", help="Max games to auto-fund"),
    min_volume: float = typer.Option(50.0, "--min-volume", help="Min volume for auto-pick"),
    headless: bool = typer.Option(False, "--headless", help="Unattended paper logger (no UI)"),
    digest_only: bool = typer.Option(False, "--digest-only", help="Print today's slate and exit"),
) -> None:
    """Soccer paper tape: auto-discover live soccer. Empty start waits. No live bets."""
    load_project_env()

    ticker_list = parse_cli_tickers(tickers)
    rest_base = (
        "https://demo-api.kalshi.co/trade-api/v2"
        if demo
        else "https://api.elections.kalshi.com/trade-api/v2"
    )

    discovered_games = []
    discovery_result = None

    if digest_only:
        try:
            acquire_lab_lock(mode="digest")
        except LabLockHeld as exc:
            typer.echo(str(exc), err=True)
            raise typer.Exit(2) from exc
        discovery_result = discover_soccer_games(
            rest_base=rest_base, min_volume=min_volume, max_games=max_games
        )
        typer.echo(format_slate_digest(discovery_result))
        raise typer.Exit(0)

    mode = "headless" if headless else "gui"
    try:
        acquire_lab_lock(mode=mode)
    except LabLockHeld as exc:
        typer.echo(str(exc), err=True)
        if exc.mode == "headless" and not headless:
            typer.echo(
                "Headless paper logger already holds the engine. "
                "Refuse GUI rather than open a second Kalshi WS.",
                err=True,
            )
        raise typer.Exit(2) from exc

    pinned = bool(ticker_list) and not needs_auto_discover(ticker_list)
    if pinned:
        auto_discover = False
        typer.echo(
            "Using explicit CLI --tickers (real KX pin). No /series+/markets rediscover.",
            err=True,
        )
    elif auto_discover:
        typer.echo(
            "\n--- Empty launch may discover until a book seats. "
            "Once seated, no 60s /series+/markets rescan ---",
            err=True,
        )
        ticker_list = []
        discovered_games = []
    elif not ticker_list:
        typer.echo("No tickers and auto-discover disabled - waiting for live soccer.", err=True)

    game_label = (game or "").strip()
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
            "No Kalshi credentials in .env - WS-only L2 will stay idle (no REST poll).\n"
            "Add KALSHI_KEY_ID + KALSHI_PRIVATE_KEY to .env for WebSocket.",
            err=True,
        )

    typer.echo(env_status_message())
    typer.echo(f"Project: {project_root()}")
    typer.echo(f"Tickers: {', '.join(ticker_list) if ticker_list else '(waiting for live soccer)'}")
    typer.echo(f"Game: {config.game_label or '(unnamed)'}")
    typer.echo(f"Output: {config.output_dir}")
    typer.echo(f"Feed: {'WebSocket' if config.use_ws else 'slow REST (explicit --rest-only)'}")
    typer.echo("Mode: PAPER ONLY (live=False)")

    from suspension_lab.lab_runtime import LabRuntime

    runtime = LabRuntime(
        config,
        auto_discover=auto_discover,
        max_games=max_games,
        min_volume=min_volume,
    )

    if headless:
        from suspension_lab.paper_logger import run_headless

        run_headless(runtime, duration_seconds=0)
        return

    from suspension_lab.ui import run_app

    run_app(runtime=runtime)


if __name__ == "__main__":
    typer.run(main)
