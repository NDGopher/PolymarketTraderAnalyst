#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
CLI=.venv/bin/polyanalyst
PY=.venv/bin/python
LOG=/tmp/mm_research
mkdir -p "$LOG"

run_one() {
  local id="$1"
  local log="$LOG/${id}.log"
  echo "=== START $id $(date -Is) ===" | tee "$log"
  $CLI autopsy "$id" --full -v 2>&1 | tee -a "$log" || echo "AUTOPSY FAILED $id" | tee -a "$log"
  $PY - <<PY 2>&1 | tee -a "$log"
from pathlib import Path
from polyanalyst.pipeline import AnalyzerApp
from polyanalyst.mega_report import generate_master
app = AnalyzerApp(Path("data"))
try:
    p = generate_master(app, "$id")
    print("MASTER:", p, p.stat().st_size)
except Exception as e:
    print("MASTER FAILED:", e)
PY
  echo "=== DONE $id $(date -Is) ===" | tee -a "$log"
}

# Smallest first
for t in DrPufferfish kch123 ImJustKen sovereign2013 GamblingIsAllYouNeed RN1; do
  run_one "$t"
done
