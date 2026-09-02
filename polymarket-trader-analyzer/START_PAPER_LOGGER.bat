@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  python -m venv .venv
  ".venv\Scripts\python.exe" -m pip install -U pip -q
  ".venv\Scripts\python.exe" -m pip install -e . -q
)
set "PYTHONPATH=%CD%"
set "LAB_TRADER_ENABLED=1"
".venv\Scripts\python.exe" -m suspension_lab.paper_logger
exit /b %ERRORLEVEL%
