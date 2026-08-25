#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
CLI=.venv/bin/polyanalyst
PY=.venv/bin/python
LOG_DIR=/tmp/polyanalyst_new
mkdir -p "$LOG_DIR"

run_one() {
  local id="$1"
  local log="$LOG_DIR/${id}.log"
  echo "=== START $id $(date -Is) ===" | tee "$log"
  $CLI autopsy "$id" --full -v 2>&1 | tee -a "$log"
  $PY - <<PY 2>&1 | tee -a "$log"
from pathlib import Path
from polyanalyst.pipeline import AnalyzerApp
from polyanalyst.mega_report import generate_master
app = AnalyzerApp(Path("data"))
p = generate_master(app, "$id")
print("MASTER:", p, p.stat().st_size)
PY
  echo "=== DONE $id $(date -Is) ===" | tee -a "$log"
}

# Smaller book first
run_one SineNooneEI
run_one Anjun
