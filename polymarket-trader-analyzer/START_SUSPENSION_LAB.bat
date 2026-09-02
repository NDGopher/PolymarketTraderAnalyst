@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo.
echo  Suspension Edge Lab - setup + launch
echo  ===================================
echo.

where python >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Python not found.
  echo Install Python 3.11+ from https://www.python.org/downloads/
  echo Check "Add python.exe to PATH" during install.
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo [1/3] Creating virtual environment...
  python -m venv .venv
  if errorlevel 1 (
    echo [ERROR] Failed to create venv.
    pause
    exit /b 1
  )
) else (
  echo [1/3] Virtual environment OK
)

echo [2/3] Installing dependencies...
".venv\Scripts\python.exe" -m pip install -U pip -q
".venv\Scripts\python.exe" -m pip install -e . -q
if errorlevel 1 (
  echo [ERROR] pip install failed.
  pause
  exit /b 1
)

if not exist ".env" (
  echo.
  echo [ERROR] No .env file found in this folder.
  echo.
  echo   1. Copy .env.example to .env
  echo   2. Paste your KALSHI_KEY_ID and KALSHI_PRIVATE_KEY
  echo   3. Do not pin LAB_TICKERS — auto-discover funds live soccer
  echo   4. Double-click this bat again
  echo.
  if exist ".env.example" copy /Y ".env.example" ".env" >nul
  if exist ".env" (
    echo Created .env from .env.example - edit it, then re-run.
  )
  pause
  exit /b 1
)

echo [3/3] Launching Suspension Edge Lab (GUI on the shared paper engine)...
echo      One lab process only. If paper_logger already holds data\suspension_lab\lab.lock,
echo      this exits instead of opening a second Kalshi client.
echo.
set "PYTHONPATH=%CD%"
".venv\Scripts\python.exe" -m suspension_lab.cli
set EXITCODE=%ERRORLEVEL%
if not %EXITCODE%==0 (
  echo.
  echo Lab exited with code %EXITCODE%
  pause
)
exit /b %EXITCODE%
