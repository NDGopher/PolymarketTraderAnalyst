# Cross-trader comparison — MM/taker research batch

Preferred PnL = field closest to Polymarket leaderboard ALL (ground truth).

| Trader | Identity | Preferred PnL | LB ALL | Trades | WR | Both-sides | Entry maker% | Diff/Ease | Exit |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| polika72 | `one_sided_informed_scalper` | $58,204.98 | $58,267.39 | 19,978 | 80.1% | 0.7% | 38.38 | 8/3 | `sell_secondary_market` |
| HomeRunHazard | `two_sided_inventory_mm` | $2,231,236.73 | $2,466,469.30 | 26,170 | 54.0% | 68.6% | 84.91 | 8/3 | `merge_and_or_redeem_dominant` |
| Winnertraders | `hybrid_liquidity_scalper` | $16,661.90 | $17,697.33 | 20,475 | 65.1% | 9.2% | 62.15 | 6/5 | `sell_secondary_market` |
| WTSA | `directional_hold_to_resolution` | $169,030.34 | $417,264.87 | 17,934 | 98.7% | 1.6% | 54.66 | 9/2 | `merge_and_or_redeem_dominant` |
| SineNooneEI | `directional_hold_to_resolution` | $541,301.28 | $577,900.26 | 16,603 | 79.5% | 1.0% | 40.59 | 9/2 | `sell_secondary_market` |
| Anjun | `directional_or_unclear` | $4,747,733.59 | $887,229.51 | 293,079 | 59.7% | 40.2% | 84.97 | 7/4 | `sell_secondary_market` |
| kch123 | `two_sided_inventory_mm` | $13,390,318.52 | $11,386,690.88 | 106,103 | 52.7% | 56.6% | 72.49 | 7/4 | `sell_secondary_market` |
| sovereign2013 | `two_sided_inventory_mm` | $2,198,738.71 | $3,588,720.22 | 119,316 | 51.1% | 61.7% | 75.54 | 7/4 | `sell_secondary_market` |
| DrPufferfish | `hybrid_liquidity_scalper` | $4,175,613.54 | $4,055,413.26 | 64,290 | 90.2% | 11.3% | 77.64 | 6/5 | `sell_secondary_market` |
| ImJustKen | `directional_or_unclear` | $-27,767,466.73 | $3,291,874.41 | 320,389 | 45.3% | 82.7% | 74.37 | 7/4 | `sell_secondary_market` |

## Equity / risk

| Trader | Cashflow final | Cashflow max DD | Cashflow Sharpe | Closed final | Closed max DD | Closed Sharpe |
|---|---:|---:|---:|---:|---:|---:|
| polika72 | $58,204.98 | $-601.18 | 14.692 | $61,909.37 | $-1,347.91 | 10.102 |
| HomeRunHazard | $-826,491.53 | $-1,248,741.22 | -4.624 | $2,231,236.73 | $-518,390.05 | 4.867 |
| Winnertraders | $16,661.90 | $-1,436.31 | 4.732 | $-844.29 | $-15,819.00 | -0.162 |
| WTSA | $169,030.34 | $-596,843.08 | 0.715 | $3,581,052.07 | $0.00 | 18.961 |
| SineNooneEI | $541,301.28 | $-414,391.76 | 0.853 | $3,761,463.08 | $-253,587.02 | 8.186 |
| Anjun | $-122,739.82 | $-2,006,136.70 | -0.018 | $4,747,733.59 | $-975,979.72 | 3.607 |
| kch123 | $11,500,337.66 | $-1,702,683.95 | 3.126 | $13,390,318.52 | $-1,796,563.50 | 3.501 |
| sovereign2013 | $364,775.31 | $-808,384.30 | 0.449 | $2,198,738.71 | $-1,476,686.34 | 1.646 |
| DrPufferfish | $4,176,633.54 | $-1,021,203.64 | 2.377 | $46,297,730.97 | $-274,872.64 | 13.682 |
| ImJustKen | $9,705,808.04 | $-3,612,434.05 | 2.49 | $-27,767,466.73 | $-29,242,670.01 | -1.255 |

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

### SineNooneEI
- Difficulty **9/10** · Ease **2/10**
- Buy-and-hold / resolution harvesting at large notional. Easy mechanically (buy → wait → redeem) but edge is selection + bankroll + path risk, not a simple rule.
- Kalshi fit: MEDIUM — extract risk + hold rules; re-fit microstructure on Kalshi

### Anjun
- Difficulty **7/10** · Ease **4/10**
- Needs quoting stack, inventory skew, cancel/replace; closer to classic MM.
- Kalshi fit: HIGH — closest to two-sided informed MM DNA

### kch123
- Difficulty **7/10** · Ease **4/10**
- Needs quoting stack, inventory skew, cancel/replace; closer to classic MM.
- Kalshi fit: HIGH — closest to two-sided informed MM DNA

### sovereign2013
- Difficulty **7/10** · Ease **4/10**
- Needs quoting stack, inventory skew, cancel/replace; closer to classic MM.
- Kalshi fit: HIGH — closest to two-sided informed MM DNA

### DrPufferfish
- Difficulty **6/10** · Ease **5/10**
- Maker-led entries reduce latency race; still needs solid risk + universe selection.
- Kalshi fit: MEDIUM-HIGH — maker entries transfer well; add explicit both-sides module

### ImJustKen
- Difficulty **7/10** · Ease **4/10**
- Needs quoting stack, inventory skew, cancel/replace; closer to classic MM.
- Kalshi fit: HIGH — closest to two-sided informed MM DNA

## Artifact map

Per trader under `samples/<name>/`:
- `MASTER.md` — human mega-report
- `MASTER.json` — bot schema
- `equity_curve.csv` / `equity_curve_closed.csv`
