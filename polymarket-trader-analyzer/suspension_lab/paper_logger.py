"""Headless paper tape logger — auto-discover today's soccer, no live bets."""

from __future__ import annotations

import os
import signal
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

import typer

from suspension_lab.config import BOOK_SAMPLE_MS, LabConfig
from suspension_lab.env_loader import env_status_message, load_project_env, project_root
from suspension_lab.kalshi_client import KalshiBookFeed
from suspension_lab.soccer_discovery import (
    discover_soccer_games,
    format_discovery_log,
    format_slate_digest,
    needs_auto_discover,
)
from suspension_lab.tape_engine import TapeEngine

load_project_env()


def _resolve_tickers(
    tickers: str,
    *,
    demo: bool,
    auto_discover: bool,
    max_games: int,
    min_volume: float,
) -> tuple[list[str], list, str]:
    ticker_str = (tickers or os.environ.get("LAB_TICKERS", "")).strip()
    ticker_list = [t.strip() for t in ticker_str.split(",") if t.strip()] if ticker_str else []
    if ticker_str.lower() == "run":
        ticker_list = []
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
    rediscover_seconds: float = 300.0,
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
    if not config.has_ws_auth:
        config.use_ws = False

    ts = datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S")
    slug = (config.game_label or "soccer-paper").replace(" ", "_")[:40]
    session_dir = config.output_dir / f"{ts}_{slug}"
    engine = TapeEngine.create(
        session_dir,
        tickers,
        game_label=config.game_label,
        games=games,
        rest_base=config.rest_base,
        paper_enabled=True,
    )

    def on_status(msg: str) -> None:
        print(f"[feed] {msg}", flush=True)

    def _books() -> dict:
        out = {}
        for t, book in feed.books.items():
            lv = book.top_levels()
            lv["book_json"] = book.full_json()
            out[t] = lv
        return out

    feed = KalshiBookFeed(config, on_book=engine.handle_book, on_status=on_status)
    engine.logger.bind_book_provider(_books)

    stop = threading.Event()

    def _stop(_sig=None, _frame=None) -> None:
        stop.set()

    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)

    feed.start()
    started = time.time()
    last_rediscover = started
    print(f"Paper logger session: {session_dir}", flush=True)
    print("PAPER ONLY — live=False. Ctrl+C to stop.", flush=True)

    interval = max(poll_ms, 100) / 1000.0
    while not stop.is_set():
        books = {}
        for t, book in feed.books.items():
            lv = book.top_levels()
            lv["book_json"] = book.full_json()
            books[t] = lv
        if books:
            engine.logger.log_book_sample(books)
        if duration_seconds > 0 and (time.time() - started) >= duration_seconds:
            break
        if rediscover_seconds > 0 and (time.time() - last_rediscover) >= rediscover_seconds:
            last_rediscover = time.time()
            extra, extra_games, extra_log = _resolve_tickers(
                "",
                demo=demo,
                auto_discover=True,
                max_games=8,
                min_volume=50,
            )
            added = 0
            for ticker in extra:
                if feed.add_ticker(ticker):
                    engine.logger.register_ticker(ticker)
                    engine.labels.register_ticker(ticker)
                    added += 1
            if added:
                engine.games.extend(extra_games)
                print(f"[discover] added {added} tickers\n{extra_log}", flush=True)
        time.sleep(interval)

    feed.stop()
    engine.logger.finalize(saved=True)
    board = engine.trader.scoreboard()
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


def main(
    tickers: str = typer.Option("", "--tickers", "-t", help="Optional pin; empty = auto-discover today"),
    game: str = typer.Option("", "--game", "-g"),
    demo: bool = typer.Option(False, "--demo"),
    rest_only: bool = typer.Option(False, "--rest-only"),
    poll_ms: int = typer.Option(BOOK_SAMPLE_MS, "--poll-ms"),
    output_dir: Path = typer.Option(Path("data/suspension_lab/sessions"), "--output-dir"),
    duration_minutes: float = typer.Option(0.0, "--duration-minutes", help="0 = until Ctrl+C"),
    max_games: int = typer.Option(5, "--max-games"),
    min_volume: float = typer.Option(50.0, "--min-volume"),
    digest_only: bool = typer.Option(False, "--digest-only", help="Print slate and exit"),
) -> None:
    """Unattended paper logger. Auto-discovers today's soccer. No live bets."""
    load_project_env()
    ticker_list, games, log = _resolve_tickers(
        tickers,
        demo=demo,
        auto_discover=True,
        max_games=max_games,
        min_volume=min_volume,
    )
    if log:
        typer.echo(log)
    if digest_only:
        raise typer.Exit(0)
    if not ticker_list:
        typer.echo("No today/tonight soccer tape to fund. Auto-discover is ready for the next slate.")
        raise typer.Exit(0)

    game_label = (game or os.environ.get("LAB_GAME", "")).strip()
    if not game_label and games:
        game_label = " | ".join(g.title[:28] for g in games[:2])
        if len(games) > 2:
            game_label += f" +{len(games) - 2}"

    typer.echo(env_status_message())
    typer.echo(f"Project: {project_root()}")
    typer.echo(f"Tickers: {', '.join(ticker_list)}")
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
