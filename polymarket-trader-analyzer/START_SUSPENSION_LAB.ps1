# Suspension Edge Lab - PowerShell launcher
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host ""
Write-Host " Suspension Edge Lab - setup + launch" -ForegroundColor Cyan
Write-Host " ===================================" -ForegroundColor Cyan
Write-Host ""

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "[ERROR] Python not found. Install from https://www.python.org/downloads/" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "[1/3] Creating virtual environment..."
    python -m venv .venv
} else {
    Write-Host "[1/3] Virtual environment OK"
}

Write-Host "[2/3] Installing dependencies..."
& .\.venv\Scripts\python.exe -m pip install -U pip -q
& .\.venv\Scripts\python.exe -m pip install -e . -q

if (-not (Test-Path ".env")) {
    Write-Host ""
    Write-Host "[ERROR] No .env file in this folder." -ForegroundColor Red
    Write-Host "Copy .env.example to .env and add your Kalshi credentials + LAB_TICKERS."
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "Created .env from .env.example - edit it, then run this script again."
    }
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[3/3] Launching Suspension Edge Lab..."
Write-Host ""
$env:PYTHONPATH = $PWD.Path
& .\.venv\Scripts\python.exe -m suspension_lab.cli
$exitCode = $LASTEXITCODE
if ($exitCode -ne 0) {
    Write-Host ""
    Write-Host "Lab exited with code $exitCode" -ForegroundColor Red
    Read-Host "Press Enter to exit"
}
exit $exitCode
