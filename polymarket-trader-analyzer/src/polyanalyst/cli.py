"""One-click CLI for Polymarket trader analysis."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

from .pipeline import AnalyzerApp

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help="PolyAnalyst — deep Polymarket trader history, strategy, and comparison.",
)
console = Console()

DEFAULT_DATA = Path(__file__).resolve().parents[2] / "data"


def _app(data_dir: Optional[Path]) -> AnalyzerApp:
    return AnalyzerApp(data_dir or DEFAULT_DATA)


def _setup_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


@app.command("analyze")
def analyze_cmd(
    trader: str = typer.Argument(..., help="Username, @username, or 0x wallet"),
    full: bool = typer.Option(False, "--full", help="Force full history re-pull"),
    data_dir: Optional[Path] = typer.Option(None, "--data-dir", help="Storage directory"),
    skip_polydata: bool = typer.Option(False, "--skip-polydata"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    """Sync history (incremental by default), analyze, validate PnL, write strategy dossier."""
    _setup_logging(verbose)
    result = _app(data_dir).run(trader, force_full=full, skip_polydata=skip_polydata)
    s = result["summary"]
    v = result["validation"]

    table = Table(title=f"{s['username']} — analysis complete")
    table.add_column("Metric")
    table.add_column("Value", justify="right")
    table.add_row("Wallet", s["wallet"])
    table.add_row("Trades", f"{s['counts']['trades']:,}")
    table.add_row("Markets", f"{s['counts']['markets_traded']:,}")
    table.add_row("Cashflow realized", f"${s['pnl']['cashflow_realized']:,.2f}")
    table.add_row("Closed PnL sum", f"${s['pnl']['closed_positions_sum']:,.2f}")
    table.add_row("Win rate", f"{s['pnl']['win_rate']*100:.2f}%")
    table.add_row("MM label", s["market_making"]["label"])
    table.add_row("Validation OK", "yes" if v.get("ok") else "review")
    console.print(table)

    console.print("\n[bold]Validation checks[/bold]")
    for c in v.get("checks", []):
        flag = "[green]MATCH[/green]" if c.get("match") else "[yellow]DRIFT[/yellow]"
        console.print(
            f" {flag} {c['source']} {c['metric']}: ours={c.get('ours')} ref={c.get('reference')} diff={c.get('diff')}"
        )

    console.print(f"\nStrategy report: {result['paths']['strategy']}")
    console.print(f"Summary JSON:    {result['paths']['summary']}")


@app.command("update")
def update_cmd(
    trader: str = typer.Argument(...),
    data_dir: Optional[Path] = typer.Option(None, "--data-dir"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    """Incremental sync + refresh analysis (only pulls new activity since last run)."""
    _setup_logging(verbose)
    result = _app(data_dir).run(trader, force_full=False, skip_polydata=False)
    s = result["summary"]
    v = result["validation"]
    console.print(
        f"[bold]{s['username']}[/bold] updated — trades={s['counts']['trades']:,} "
        f"cashflow=${s['pnl']['cashflow_realized']:,.2f} validation={'OK' if v.get('ok') else 'REVIEW'}"
    )
    console.print(f"Strategy: {result['paths']['strategy']}")


@app.command("show")
def show_cmd(
    trader: str = typer.Argument(...),
    data_dir: Optional[Path] = typer.Option(None, "--data-dir"),
    strategy: bool = typer.Option(True, "--strategy/--no-strategy"),
) -> None:
    """Show the latest saved analysis for a trader."""
    latest = _app(data_dir).show(trader)
    console.print(f"Run #{latest['id']} at {latest['created_at']}")
    console.print(json.dumps({k: latest['summary'].get(k) for k in ('username','wallet','pnl','counts','market_making')}, indent=2))
    if strategy and latest.get("strategy_md"):
        console.print(Markdown(latest["strategy_md"][:12000]))


@app.command("list")
def list_cmd(data_dir: Optional[Path] = typer.Option(None, "--data-dir")) -> None:
    """List cached traders and recent analysis runs."""
    application = _app(data_dir)
    traders = application.store.list_traders()
    table = Table(title="Cached traders")
    table.add_column("Username")
    table.add_column("Wallet")
    table.add_column("Trades")
    table.add_column("Last sync notes")
    for t in traders:
        st = application.store.get_sync_state(t["wallet"]) or {}
        table.add_row(
            t.get("username") or "",
            t["wallet"],
            str(st.get("trade_count") or ""),
            (st.get("notes") or "")[:60],
        )
    console.print(table)
    runs = application.store.list_analyses(limit=15)
    console.print("\nRecent runs:")
    for r in runs:
        console.print(f"  #{r['id']} {r['username']} ({r['wallet'][:10]}…) @ {r['created_at']}")


@app.command("compare")
def compare_cmd(
    traders: list[str] = typer.Argument(..., help="Two or more usernames/wallets"),
    data_dir: Optional[Path] = typer.Option(None, "--data-dir"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    """Compare multiple traders (auto-analyzes any that are missing)."""
    _setup_logging(verbose)
    if len(traders) < 2:
        raise typer.BadParameter("Provide at least two traders")
    result = _app(data_dir).compare(traders)
    console.print(Markdown(result["markdown"]))
    console.print(f"\nSaved: {result['path']}")


@app.command("autopsy")
def autopsy_cmd(
    trader: str = typer.Argument(...),
    full: bool = typer.Option(False, "--full"),
    data_dir: Optional[Path] = typer.Option(None, "--data-dir"),
    skip_maker_taker: bool = typer.Option(False, "--skip-maker-taker"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    """Full-depth autopsy (polika72 standard): sync, validate, reports, samples."""
    _setup_logging(verbose)
    from .autopsy_runner import run_full_autopsy

    result = run_full_autopsy(
        _app(data_dir),
        trader,
        force_full=full,
        classify_maker_taker=not skip_maker_taker,
    )
    s = result["stats"]
    v = result["validation"]
    console.print(
        f"[bold]{result['username']}[/bold] autopsy complete — "
        f"identity={s.get('identity')} trades={s['counts']['trades']:,} "
        f"cashflow=${s['pnl']['cashflow_realized']:,.2f} validation={'OK' if v.get('ok') else 'REVIEW'}"
    )
    console.print(f"Reports: {result['paths']['samples']}")


@app.command("ui")
def ui_cmd(port: int = typer.Option(8787, "--port")) -> None:
    """Launch local research UI."""
    from .ui import app as flask_app

    flask_app.run(host="127.0.0.1", port=port, debug=False)


if __name__ == "__main__":
    app()
