# Cross-trader comparison — polika72 · HomeRunHazard · Winnertraders · WTSA

Preferred PnL = field closest to Polymarket leaderboard ALL (ground truth).

| Trader | Identity | Preferred PnL | LB ALL | Trades | WR | Both-sides | Entry maker% | Diff/Ease | Exit |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| polika72 | `one_sided_informed_scalper` | $57,699.08 | $57,338.72 | 19,978 | 80.1% | 0.7% | 38.38 | 8/3 | `sell_secondary_market` |
| HomeRunHazard | `two_sided_inventory_mm` | $2,231,236.73 | $2,248,711.81 | 26,170 | 54.0% | 68.6% | 84.91 | 8/3 | `merge_and_or_redeem_dominant` |
| Winnertraders | `hybrid_liquidity_scalper` | $16,661.90 | $17,578.63 | 20,475 | 65.1% | 9.2% | 62.15 | 6/5 | `sell_secondary_market` |
| WTSA | `directional_hold_to_resolution` | $169,030.34 | $442,550.51 | 17,934 | 98.7% | 1.6% | 54.66 | 9/2 | `merge_and_or_redeem_dominant` |

## Equity / risk

| Trader | Cashflow final | Cashflow max DD | Cashflow Sharpe | Closed final | Closed max DD | Closed Sharpe |
|---|---:|---:|---:|---:|---:|---:|
| polika72 | $58,204.98 | $-601.18 | 14.692 | $61,909.37 | $-1,347.91 | 10.102 |
| HomeRunHazard | $-826,491.53 | $-1,248,741.22 | -4.624 | $2,231,236.73 | $-518,390.05 | 4.867 |
| Winnertraders | $16,661.90 | $-1,436.31 | 4.732 | $-844.29 | $-15,819.00 | -0.162 |
| WTSA | $169,030.34 | $-596,843.08 | 0.715 | $3,581,052.07 | $0.00 | 18.961 |

## Copyability

### polika72
- Difficulty **8/10** · Ease **3/10**
- Requires live event latency + execution; pattern is clear but edge is speed/data.
- Kalshi fit: MEDIUM — use as taker/impulse overlay on a Kalshi MM core, not as the core itself

### HomeRunHazard
- Difficulty **8/10** · Ease **3/10**
- Two-sided inventory MM DNA (often buy YES + buy NO then MERGE/REDEEM). Needs quoting/inventory stack; buy-only books exit via merge/redeem instead of sells.
- Kalshi fit: HIGH — closest to two-sided informed MM DNA

### Winnertraders
- Difficulty **6/10** · Ease **5/10**
- Maker-led entries reduce latency race; still needs solid risk + universe selection.
- Kalshi fit: MEDIUM-HIGH — maker entries transfer well; add explicit both-sides module

### WTSA
- Difficulty **9/10** · Ease **2/10**
- Buy-and-hold / resolution harvesting at large notional. Easy mechanically (buy → wait → redeem) but edge is selection + bankroll + path risk, not a simple rule.
- Kalshi fit: MEDIUM — extract risk + hold rules; re-fit microstructure on Kalshi

## Artifact map

Per trader under `samples/<name>/`:
- `MASTER.md` — human mega-report
- `MASTER.json` — bot schema
- `equity_curve.csv` / `equity_curve_closed.csv`
