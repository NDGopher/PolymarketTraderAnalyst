#!/usr/bin/env bash
# One-click analyzer. Usage: ./run.sh polika72
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
if [[ ! -d .venv ]]; then
  python3 -m venv .venv
  .venv/bin/pip install -U pip
  .venv/bin/pip install -e .
fi
# shellcheck disable=SC1091
source .venv/bin/activate
exec polyanalyst analyze "$@"
