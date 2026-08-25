# Deep Trader Autopsy — HomeRunHazard

- Wallet: `0x5268527977f700f9bf9b6d5cd843859e4e70135d`
- Identity: **`two_sided_inventory_mm`**
- Primary focus: **sports_totals**
- Span: 2026-04-24T14:39:18+00:00 → 2026-05-07T12:35:18+00:00 (12.91 days)
- Generated: 2026-08-25T16:46:54.878991+00:00

## A. Data integrity / reconciliation

| Source | PnL | Trades / notes |
|---|---:|---|
| Our cashflow realized | -$2,419,854.53 | trades=26,170 |
| Our core cashflow | -$2,438,366.83 | buys=26,170 sells=0 |
| Our closed-legs sum | $2,231,236.73 | closed=42,624 WR=54.0% |
| Polymarket leaderboard ALL | $2,248,711.81 | vol=$264,797,406.19 rank=67 |
| PolyData | $2,250,300.68 | trades=268747 WR=0.5418 |

- **MATCH** `polymarket_leaderboard_ALL` pnl: ours=2231236.7279 ref=2248711.8139243205 diff=-17475.086
- **MATCH** `polydata` realized_pnl: ours=2231236.7279 ref=2250300.68 diff=-19063.9521
- **DRIFT** `polydata` n_trades: ours=26170 ref=268747 diff=-242577
- **MATCH** `polydata` win_rate: ours=0.5402 ref=0.5418 diff=-0.0016
- **DRIFT** `internal` cashflow_vs_closed: ours=-2419854.5251 ref=2231236.7279 diff=-4651091.253

## B. Core identity

- Scanner MM label: `likely_market_maker` (score 45)
- Trades both outcomes in 69% of markets (inventory/MM signature)
- High-frequency cadence (median gap 10s)
- Heavy concentration in Over/Under sports totals (sports MM niche)
- Both-sides inventory: 753 markets (68.64%)
- Clip USDC median/p90/max: $8.17 / $488.54 / $9,369.92
- Sport categories: `{'sports_totals': -194767.89, 'sports_match': -291205.24}`
- Slug tokens: [('mlb', 607), ('atp', 174), ('nba', 156), ('wta', 144), ('nhl', 9), ('lal', 6), ('ten', 3)]

### Maker vs Taker

| Leg | Maker % | Taker % | Maker fills | Taker fills |
|---|---:|---:|---:|---:|
| Entry | 84.91% | 15.09% | 24,232 | 1,938 |
| Exit | None% | None% | 0 | 0 |


### Price bands

| Band | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| 0-20¢ | 28 | 4.8% | -$43,431.34 | -$1,551.12 |
| 20-40¢ | 156 | 31.2% | -$125,802.79 | -$806.43 |
| 40-60¢ | 816 | 55.5% | -$424,811.46 | -$520.60 |
| 60-80¢ | 80 | 75.0% | $47,345.47 | $591.82 |
| 80-100¢ | 17 | 93.8% | $60,726.99 | $3,572.18 |

## C. Equity & risk

- Final cashflow equity: -$826,491.53
- Max drawdown: -$1,248,741.22 (0.0% of peak)
- Longest drawdown: 13 days
- Daily Sharpe (ann.): -4.624
- Profit factor: 1.0434
- Top 10 winners: $202,627.39 (21.63% of win PnL)
- Top 10 losers: -$483,957.70 (34.01% of loss PnL)
- Max inventory shares: 180889.27

### Top winners
- $30,407.98 · 1h50m · Madrid Open: Anastasia Potapova vs Elena Rybakina
- $27,567.49 · 1h08m · Madrid Open: Alexander Bublik vs Stefanos Tsitsipas
- $24,774.18 · 1h36m · Madrid Open: Thiago Agustin Tirante vs Tommy Paul
- $21,400.73 · 1h36m · 76ers vs. Knicks
- $18,618.95 · 1h01m · Madrid Open: Jessica Pegula vs Marta Kostyuk
- $18,085.18 · 10h49m · Athletics vs. Philadelphia Phillies: O/U 8.5
- $17,054.02 · 2h09m · Milwaukee Brewers vs. St. Louis Cardinals: O/U 8.5
- $16,281.38 · 2m37s · Cincinnati Reds vs. Chicago Cubs: O/U 8.5
- $15,666.68 · 5h21m · Athletics vs. Philadelphia Phillies: O/U 9.5
- $12,770.80 · 1h31m · Toronto Blue Jays vs. Tampa Bay Rays

### Top losers
- -$16,346.11 · 2h29m · Colorado Rockies vs. New York Mets
- -$19,436.44 · 1h32m · Madrid Open: Terence Atmane vs Alexander Zverev
- -$21,487.41 · 1h52m · Madrid Open: Daniil Medvedev vs Fabian Marozsan
- -$23,006.33 · 1h28m · Internazionali BNL d'Italia: Federico Cina vs Alexander Blockx
- -$54,557.39 · 2h08m · Madrid Open: Aryna Sabalenka vs Naomi Osaka
- -$57,746.38 · 1h29m · New York Mets vs. Colorado Rockies: O/U 10.5
- -$59,416.63 · 1h47m · 76ers vs. Knicks: O/U 212.5
- -$69,098.34 · 1h27m · Madrid Open: Stefanos Tsitsipas vs Casper Ruud
- -$70,897.12 · 2h03m · Baltimore Orioles vs. New York Yankees
- -$91,965.56 · 1h39m · 76ers vs. Knicks: O/U 211.5

## D. Trade management

### Hold-time buckets

| Bucket | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| <30s | 228 | 66.1% | $20,573.48 | $90.23 |
| 30s-2m | 25 | 68.4% | $2,702.79 | $108.11 |
| 2-5m | 34 | 55.2% | $7,037.48 | $206.98 |
| 5-15m | 53 | 44.0% | $512.34 | $9.67 |
| 15m+ | 757 | 50.6% | -$516,799.21 | -$682.69 |

- After early adverse (>2¢ vs entry within 2m): n=0, avg PnL n/a, median first-sell n/a, median hold n/a
- After favorable first sell (+2¢): n=0, avg PnL n/a, median MFE capture None
- Campaigns (re-entry after flat): 0 (0.0%), avg entries None, PnL $0.00, avg n/a, WR None%
- Single-entry: n=1097, PnL -$485,973.13, avg -$443.00
- Flatten-before-resolution flag rate: 0.6773; hold-to-resolution style n=1097; redeems $2,693,132.00; merges $1,593,363.00
- Avg-down while MTM-red on losers: 345/469 (73.56%); Δ if skipped on those $0.00; global never-red-buy Δ $0.00

### Family mix

| Family | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| Other | 679 | 50.7% | -$337,510.06 | -$497.07 |
| Over/Under | 418 | 57.9% | -$148,463.07 | -$355.17 |

## E. Edge diagnosis

- Time to MFE (winners): median n/a, p25 n/a, p75 n/a, p90 n/a
- Big MFE ≥10¢: n=0; within 30s=0; within 60s=0 (0.0% of big moves)

**Edge thesis:** Classic inventory MM — both-sides presence with spread capture; edge from quoting and inventory skew, not event sniping alone.

## F. vs polika72

| Metric | This trader | polika72 |
|---|---:|---:|
| identity | two_sided_inventory_mm | one_sided_informed_scalper |
| trades | 26170 | 19978 |
| cashflow_pnl | -2419854.5251 | 58204.9839 |
| win_rate | 0.5402 | 0.8008 |
| entry_taker_pct | 15.09 | 61.62 |
| both_sides_rate | 0.6864 | 0.0068 |
| median_clip | 8.1673 | 11.29 |
| campaign_pct | 0.0 | 5.85 |
| max_dd | -1248741.2218 | -601.1817 |
| time_to_mfe_med | None | 64 |

### Steal / avoid

- **Steal:** both-sides inventory discipline (closer to true MM than polika72).
- **Steal:** maker-led entries (better for quoting stack on Kalshi).
- **Avoid:** their drawdown profile — size down vs polika72 risk.
- **Avoid:** averaging down while red.

## G. Kalshi two-sided informed MM relevance

High relevance to a Kalshi two-sided informed MM: both-sides + quoting DNA. Port inventory caps, skew rules, and maker exit logic; replace Polymarket sports feed with Kalshi event feeds.
