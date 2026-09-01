from __future__ import annotations

from pathlib import Path

import typer

from suspension_lab.analyze_session import analyze_session, run_analysis

app = typer.Typer(add_completion=False, help="Analyze a suspension lab session")


@app.command()
def session(
    path: Path = typer.Argument(..., help="Path to session folder"),
) -> None:
    """Print analysis report for a saved session."""
    path = path.resolve()
    if not (path / "events.csv").exists():
        typer.echo(f"Not a session folder (missing events.csv): {path}", err=True)
        raise typer.Exit(1)
    report = analyze_session(path)
    out = run_analysis(path)
    typer.echo(report)
    typer.echo(f"\nSaved: {out}")


if __name__ == "__main__":
    app()
