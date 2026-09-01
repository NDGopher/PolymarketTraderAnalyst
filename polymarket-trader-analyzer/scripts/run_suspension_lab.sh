#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
# Usage: ./scripts/run_suspension_lab.sh "TICKER1,TICKER2" --game "Parma-Cremonese"
exec python -m suspension_lab.cli run "$@"
