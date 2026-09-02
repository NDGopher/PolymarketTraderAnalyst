# Unattended soccer paper logger (no UI, no live bets)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    python -m venv .venv
    & .\.venv\Scripts\python.exe -m pip install -U pip -q
    & .\.venv\Scripts\python.exe -m pip install -e . -q
}

$env:PYTHONPATH = $PWD.Path
$env:LAB_TRADER_ENABLED = "1"
& .\.venv\Scripts\python.exe -m suspension_lab.paper_logger
exit $LASTEXITCODE
