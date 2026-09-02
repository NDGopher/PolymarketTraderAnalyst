"""Headless paper tape logger - same engine and lock as the GUI. No live bets."""

from __future__ import annotations

import signal
import time
from pathlib import Path

import typer

from suspension_lab.config import BOOK_SAMPLE_MS, LabConfig
from suspension_lab.env_loader import env_status_message, load_project_env, project_root
from suspension_lab.instance_lock import LabLockHeld, acquire_lab_lock
from suspension_lab.lab_runtime import LabRuntime
from suspension_lab.soccer_discovery import (
    discover_soccer_games,
    format_discovery_log,
    format_slate_digest,
    needs_auto_discover,
    parse_cli_tickers,
)

load_project_env()


def _resolve_tickers(
    tickers: str,
    *,
    demo: bool,
    auto_discover: bool,
    max_games: int,
    min_volume: float,
) -> tuple[list[str], list, str]:
    ticker_list = parse_cli_tickers(tickers)
    rest_base = (
        "https://demo-api.kalshi.co/trade-api/v2"
        if demo
        else "https://api.elections.kalshi.com/trade-api/v2"
    )
    games = []
    log = ""
    if auto_discover and needs_auto_discover(ticker_list):
        result = discover_soccer_games(
            rest_base=rest_base,
            min_volume=min_volume,
            max_games=max_games,
        )
        ticker_list = result.tickers
        games = result.games
        log = format_discovery_log(result) + "\n\n" + format_slate_digest(result)
    return ticker_list, games, log


def run_headless(runtime: LabRuntime, *, duration_seconds: float = 0) -> Path:
    """Run an already-built runtime without a second Kalshi client."""

    def _stop(_sig=None, _frame=None) -> None:
        runtime.stop()

    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)

    runtime.start()
    print(f"Paper logger session: {runtime.logger.session_dir}", flush=True)
    print("PAPER ONLY - live=False. Ctrl+C to stop.", flush=True)
    runtime.wait_until_stopped(duration_seconds=duration_seconds)
    runtime.stop()
    runtime.logger.finalize(saved=True)
    board = runtime.trader.scoreboard()
    session_dir = runtime.logger.session_dir
    print(
        f"Stopped. books_long={session_dir / 'books_long.csv'} "
        f"would-have={board['would_have_count']} burned={board['burned_count']}",
        flush=True,
    )
    if (session_dir / "goal_signals.csv").exists():
        try:
            from suspension_lab.fill_verifier import run_verify_fills

            signals = (session_dir / "goal_signals.csv").read_text(encoding="utf-8").strip().splitlines()
            if len(signals) > 1:
                path = run_verify_fills(session_dir)
                print(f"Fill-would-have: {path}", flush=True)
        except Exception as exc:  # noqa: BLE001
            print(f"Fill verifier skipped: {exc}", flush=True)
    return session_dir


def run_paper_logger(
    *,
    tickers: list[str],
    games: list,
    game_label: str,
    demo: bool,
    rest_only: bool,
    poll_ms: int,
    output_dir: Path,
    duration_seconds: float,
    rediscover_seconds: float = 60.0,
) -> Path:
    config = LabConfig.from_env(
        tickers,
        game_label=game_label,
        demo=demo,
        use_ws=not rest_only,
        poll_ms=poll_ms,
        output_dir=output_dir,
    )
    config.games = games
    config.paper_enabled = True

    runtime = LabRuntime(
        config,
        auto_discover=needs_auto_discover(tickers),
        max_games=8,
        min_volume=50,
        rediscover_seconds=max(rediscover_seconds, 60.0),  # empty-start only; seated never scans
        on_status=lambda msg: print(f"[feed] {msg}", flush=True),
    )
    return run_headless(runtime, duration_seconds=duration_seconds)


def main(
    tickers: str = typer.Option(
        "",
        "--tickers",
        "-t",
        help="Optional explicit KX pin. Empty = auto-discover. Does not read LAB_TICKERS.",
    ),
    game: str = typer.Option("", "--game", "-g", help="Match label. Does not read LAB_GAME."),
    demo: bool = typer.Option(False, "--demo"),
    rest_only: bool = typer.Option(False, "--rest-only"),
    poll_ms: int = typer.Option(BOOK_SAMPLE_MS, "--poll-ms"),
    output_dir: Path = typer.Option(Path("data/suspension_lab/sessions"), "--output-dir"),
    duration_minutes: float = typer.Option(0.0, "--duration-minutes", help="0 = until Ctrl+C"),
    max_games: int = typer.Option(5, "--max-games"),
    min_volume: float = typer.Option(50.0, "--min-volume"),
    digest_only: bool = typer.Option(False, "--digest-only", help="Print slate and exit"),
) -> None:
    """Unattended paper logger. Same lock as the GUI. No live bets."""
    load_project_env()

    if digest_only:
        try:
            acquire_lab_lock(mode="digest")
        except LabLockHeld as exc:
            typer.echo(str(exc), err=True)
            raise typer.Exit(2) from exc
        ticker_list, games, log = _resolve_tickers(
            tickers,
            demo=demo,
            auto_discover=True,
            max_games=max_games,
            min_volume=min_volume,
        )
        if log:
            typer.echo(log)
        raise typer.Exit(0)

    try:
        acquire_lab_lock(mode="headless")
    except LabLockHeld as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(2) from exc

    ticker_list = parse_cli_tickers(tickers)
    games: list = []
    if not needs_auto_discover(ticker_list):
        typer.echo("Using explicit CLI --tickers (real KX pin). No /series+/markets rediscover.")
    else:
        ticker_list = []
        typer.echo(
            "No live soccer yet - worker will discover once. "
            "No 60s /series+/markets rescan once a book seats."
        )

    game_label = (game or "").strip()
    typer.echo(env_status_message())
    typer.echo(f"Project: {project_root()}")
    typer.echo(f"Tickers: {', '.join(ticker_list) if ticker_list else '(discovering)'}")
    run_paper_logger(
        tickers=ticker_list,
        games=games,
        game_label=game_label,
        demo=demo,
        rest_only=rest_only,
        poll_ms=poll_ms,
        output_dir=output_dir,
        duration_seconds=duration_minutes * 60.0,
    )


if __name__ == "__main__":
    typer.run(main)
