#!/usr/bin/env bash
# Batch analyze new trader wallets + pending RN1/GamblingIsAllYouNeed
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
source .venv/bin/activate
LOGDIR="/tmp/trader_batch"
mkdir -p "$LOGDIR" samples

TRADERS=(
  "mysaria"
  "0xe549581668a5751c1972d3ad2d1991d900bd2d54"
  "0x2c335066fe58fe9237c3d3dc7b275c2a034a0563"
  "0x2a69660046d7acc4ab204d7cc5ba78b0776cd2f7"
  "0x14964aefa2cd7caff7878b3820a690a03c5aa429"
  "0xdbdd45150249e229eb4ca8aa48a30dca21faa5de"
  "RN1"
  "GamblingIsAllYouNeed"
)

for t in "${TRADERS[@]}"; do
  echo "=== START $t $(date -Iseconds) ===" | tee "$LOGDIR/$t.log"
  if polyanalyst analyze "$t" --full -v 2>&1 | tee -a "$LOGDIR/$t.log"; then
    # copy artifacts to samples/<username>
    USER=$(python3 -c "
import json,glob
from pathlib import Path
reports=Path('data/reports')
dirs=sorted(reports.glob('*'), key=lambda p: p.stat().st_mtime, reverse=True)
for d in dirs[:20]:
    s=d/'summary.json'
    if s.exists():
        j=json.loads(s.read_text())
        w=j.get('wallet','').lower()
        ident='$t'.lower().replace('@','')
        if ident in (j.get('username','').lower(), w, w[:10]):
            print(j['username']); break
" 2>/dev/null || echo "$t")
    DEST="samples/$USER"
    mkdir -p "$DEST"
    if [[ -d "data/reports/$USER" ]]; then
      cp -a "data/reports/$USER/"* "$DEST/" 2>/dev/null || true
    fi
    echo "=== DONE $t -> samples/$USER ===" | tee -a "$LOGDIR/$t.log"
  else
    echo "=== FAIL $t ===" | tee -a "$LOGDIR/$t.log"
  fi
done
echo "=== BATCH COMPLETE $(date -Iseconds) ===" | tee "$LOGDIR/runner.log"
