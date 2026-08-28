# Deep Trader Autopsy — kch123

- Wallet: `0x6a72f61820b26b1fe4d956e17b6dc2a1ea3033ee`
- Identity: **`two_sided_inventory_mm`**
- Primary focus: **sports_match**
- Span: 2025-06-25T19:14:46+00:00 → 2026-01-27T20:53:31+00:00 (216.07 days)
- Generated: 2026-08-28T15:23:19.763660+00:00

## A. Data integrity / reconciliation

| Source | PnL | Trades / notes |
|---|---:|---|
| Our cashflow realized | $3,628,200.69 | trades=106,103 |
| Our core cashflow | $3,628,142.05 | buys=106,005 sells=98 |
| Our closed-legs sum | $13,390,318.52 | closed=4,033 WR=52.7% |
| Polymarket leaderboard ALL | $11,386,690.88 | vol=$298,637,138.56 rank=5 |
| PolyData | $11,386,690.88 | trades=171115 WR=0.5467 |

- **DRIFT** `polymarket_leaderboard_ALL` pnl: ours=13390318.5232 ref=11386690.875513867 diff=2003627.6477
- **DRIFT** `polydata` realized_pnl: ours=13390318.5232 ref=11386690.88 diff=2003627.6432
- **DRIFT** `polydata` n_trades: ours=106103 ref=171115 diff=-65012
- **MATCH** `polydata` win_rate: ours=0.5267 ref=0.5467 diff=-0.02
- **DRIFT** `internal` cashflow_vs_closed: ours=3628200.6939 ref=13390318.5232 diff=-9762117.8293

## B. Core identity

- Scanner MM label: `strong_market_maker` (score 70)
- Trades both outcomes in 57% of markets (inventory/MM signature)
- Avg sell > avg buy in 91% of markets (spread capture)
- High-frequency cadence (median gap 12s)
- Heavy concentration in Over/Under sports totals (sports MM niche)
- Both-sides inventory: 994 markets (56.64%)
- Clip USDC median/p90/max: $15.09 / $1,078.00 / $729,628.77
- Sport categories: `{'sports_match': 8091620.88, 'sports_totals': 1458261.66, 'other': 401529.48, 'politics': -62103.19}`
- Slug tokens: [('nhl', 953), ('nfl', 328), ('nba', 151), ('mlb', 34), ('ten', 24), ('mma', 18), ('lal', 14), ('ucl', 6), ('bun', 1)]

### Maker vs Taker

| Leg | Maker % | Taker % | Maker fills | Taker fills |
|---|---:|---:|---:|---:|
| Entry | 72.49% | 27.51% | 96,876 | 9,129 |
| Exit | 0.81% | 99.19% | 66 | 32 |

- `enter_maker_exit_taker`: 29
- `enter_maker_exit_maker`: 2
- `enter_taker_exit_taker`: 1

### Price bands

| Band | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| 0-20¢ | 43 | 7.0% | -$338,837.48 | -$7,879.94 |
| 20-40¢ | 186 | 31.7% | $1,882,927.07 | $10,123.26 |
| 40-60¢ | 1094 | 53.1% | $6,760,241.70 | $6,179.38 |
| 60-80¢ | 354 | 68.9% | $1,565,063.73 | $4,421.08 |
| 80-100¢ | 78 | 93.6% | $19,913.80 | $255.31 |

## C. Equity & risk

- Final cashflow equity: $11,500,337.66
- Max drawdown: -$1,702,683.95 (-3643.6% of peak)
- Longest drawdown: 0 days
- Daily Sharpe (ann.): 3.126
- Profit factor: 1.2366
- Top 10 winners: $5,355,953.30 (10.71% of win PnL)
- Top 10 losers: -$5,222,937.24 (13.02% of loss PnL)
- Max inventory shares: 1716198.77

### Top winners
- $1,095,000.00 · 0s · Will Villarreal CF win on 2026-01-20?
- $986,792.15 · 3h33m · Spread: Seahawks (-4.5)
- $580,000.00 · 22m18s · Will Paris Saint-Germain FC win on 2026-01-20?
- $481,040.39 · 19h11m · Stars vs. Oilers
- $417,465.14 · 2h08m · Texas State vs. Southern Miss
- $375,013.18 · 11h36m · Wild vs. Penguins
- $371,663.82 · 6h02m · Will Stade Rennais FC 1901 win on 2026-01-18?
- $357,255.70 · 2h09m · Capitals vs. Blackhawks
- $345,950.63 · 38m04s · Clemson vs. Louisville
- $345,772.30 · 2h25m · Flames vs. Sharks

### Top losers
- -$412,300.01 · 3h10m · Alabama vs. Oklahoma
- -$430,296.71 · 2h39m · Ravens vs. Packers
- -$430,358.49 · 4h37m · Patriots vs. Ravens
- -$456,849.98 · 6h36m · Spread: Lions (-3.5)
- -$510,999.30 · 9m14s · Will Olympiakós SFP win on 2026-01-20?
- -$519,406.04 · 50m16s · Blue Jays vs. Dodgers
- -$533,797.48 · 3h35m · Chiefs vs. Cowboys
- -$549,430.45 · 5h12m · Bills vs. Jaguars
- -$665,499.98 · 9h25m · Blue Jays vs. Mariners
- -$713,998.80 · 21m22s · Will FC Barcelona win on 2026-01-18?

## D. Trade management

### Hold-time buckets

| Bucket | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| <30s | 254 | 53.1% | $5,821,482.00 | $22,919.22 |
| 30s-2m | 52 | 48.1% | -$1,208,686.98 | -$23,243.98 |
| 2-5m | 52 | 55.8% | $1,515,090.46 | $29,136.36 |
| 5-15m | 84 | 52.4% | $860,994.02 | $10,249.93 |
| 15m+ | 1313 | 55.4% | $2,900,429.31 | $2,209.01 |

- After early adverse (>2¢ vs entry within 2m): n=0, avg PnL n/a, median first-sell n/a, median hold n/a
- After favorable first sell (+2¢): n=27, avg PnL $33,436.69, median MFE capture 1.0
- Campaigns (re-entry after flat): 0 (0.0%), avg entries None, PnL $0.00, avg n/a, WR None%
- Single-entry: n=1755, PnL $9,889,308.83, avg $5,634.93
- Flatten-before-resolution flag rate: 0.7635; hold-to-resolution style n=1723; redeems $107,761,410.85; merges $7,872,136.96
- Avg-down while MTM-red on losers: 488/795 (61.38%); Δ if skipped on those -$561.19; global never-red-buy Δ -$102,154.61

### Family mix

| Family | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| Yes/No moneyline | 25 | 44.0% | $967,341.36 | $38,693.65 |
| Other | 1435 | 55.0% | $7,312,709.81 | $5,095.97 |
| Over/Under | 295 | 54.2% | $1,609,257.66 | $5,455.11 |

## E. Edge diagnosis

- Time to MFE (winners): median 4h04m, p25 3h33m, p75 4h42m, p90 4h52m
- Big MFE ≥10¢: n=22; within 30s=0; within 60s=0 (0.0% of big moves)

**Edge thesis:** Classic inventory MM — both-sides presence with spread capture; edge from quoting and inventory skew, not event sniping alone.

## F. vs polika72

| Metric | This trader | polika72 |
|---|---:|---:|
| identity | two_sided_inventory_mm | one_sided_informed_scalper |
| trades | 106103 | 19978 |
| cashflow_pnl | 3628200.6939 | 58204.9839 |
| win_rate | 0.5267 | 0.8008 |
| entry_taker_pct | 27.51 | 61.62 |
| both_sides_rate | 0.5664 | 0.0068 |
| median_clip | 15.0877 | 11.29 |
| campaign_pct | 0.0 | 5.85 |
| max_dd | -1702683.9473 | -601.1817 |
| time_to_mfe_med | 14664 | 64 |

### Steal / avoid

- **Steal:** both-sides inventory discipline (closer to true MM than polika72).
- **Steal:** maker-led entries (better for quoting stack on Kalshi).
- **Avoid:** their drawdown profile — size down vs polika72 risk.
- **Avoid:** averaging down while red.

## G. Kalshi two-sided informed MM relevance

High relevance to a Kalshi two-sided informed MM: both-sides + quoting DNA. Port inventory caps, skew rules, and maker exit logic; replace Polymarket sports feed with Kalshi event feeds.
