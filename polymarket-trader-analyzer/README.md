# PolyAnalyst — Polymarket Trader Deep Dive

One-click tool to pull a Polymarket trader's **entire** history, validate PnL against public sources, reverse-engineer how they win, and compare traders.

## Quick start

```bash
cd polymarket-trader-analyzer
chmod +x run.sh
./run.sh polika72
```

Or with the CLI:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
polyanalyst analyze polika72          # full sync on first run
polyanalyst update polika72           # incremental (only new trades)
polyanalyst show polika72             # latest saved dossier
polyanalyst compare polika72 someoneelse
polyanalyst list
```

Accepts `@username`, bare username, or `0x` wallet.

## What it does

1. **Resolves** identity via Polymarket Data/Gamma APIs  
2. **Pulls full history** with time-window pagination (no offset cutoffs): activity, trades, closed + open positions  
3. **Stores** everything in local SQLite (`data/polyanalyst.db`) for reuse  
4. **Incremental updates** only fetch since the last sync (with overlap)  
5. **Computes** cashflow PnL, closed-position PnL, equity curve, timing/sizing, MM heuristics  
6. **Validates** against Polymarket leaderboard + PolyData public pages  
7. **Writes** a strategy dossier explaining entries/exits/sizing and a replication playbook  
8. **Compares** multiple traders for commons vs differences  

## Outputs

Per trader under `data/reports/<username>/`:

- `strategy.md` — deep strategy write-up  
- `summary.json` — metrics  
- `markets.json` — per-market round trips  
- `validation.json` — PnL source checks  

## PnL definitions

| Field | Meaning |
|---|---|
| `cashflow_realized` | sells − buys + redeems + rebates (PolyData-style realized cash) |
| `cashflow_core` | same without rebates |
| `closed_positions_sum` | sum of Polymarket `closed-positions.realizedPnl` |
| Leaderboard ALL | Polymarket official `/v1/leaderboard?timePeriod=ALL` |

Small gaps between sources are expected (open inventory, NegRisk, rebates, indexing lag). The validator flags MATCH vs DRIFT.

## Notes

- Public APIs only — no trading / no private keys  
- First full sync for a heavy trader can take several minutes  
- Research tool; not financial advice  
