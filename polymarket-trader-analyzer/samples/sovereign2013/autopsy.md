# Deep Trader Autopsy — sovereign2013

- Wallet: `0xee613b3fc183ee44f9da9c05f53e2da107e3debf`
- Identity: **`two_sided_inventory_mm`**
- Primary focus: **sports_match**
- Span: 2025-08-07T14:54:45+00:00 → 2025-11-30T12:27:58+00:00 (114.9 days)
- Generated: 2026-08-28T15:08:28.306265+00:00

## A. Data integrity / reconciliation

| Source | PnL | Trades / notes |
|---|---:|---|
| Our cashflow realized | -$4,392,612.28 | trades=119,316 |
| Our core cashflow | -$4,392,657.34 | buys=119,305 sells=11 |
| Our closed-legs sum | $2,198,738.71 | closed=71,299 WR=51.1% |
| Polymarket leaderboard ALL | $3,588,720.22 | vol=$402,071,822.94 rank=38 |
| PolyData | $3,588,720.22 | trades=1047862 WR=0.5174 |

- **DRIFT** `polymarket_leaderboard_ALL` pnl: ours=2198738.7126 ref=3588720.2180176293 diff=-1389981.5054
- **DRIFT** `polydata` realized_pnl: ours=2198738.7126 ref=3588720.22 diff=-1389981.5074
- **DRIFT** `polydata` n_trades: ours=119316 ref=1047862 diff=-928546
- **MATCH** `polydata` win_rate: ours=0.5115 ref=0.5174 diff=-0.0059
- **DRIFT** `internal` cashflow_vs_closed: ours=-4392612.2757 ref=2198738.7126 diff=-6591350.9883

## B. Core identity

- Scanner MM label: `likely_market_maker` (score 65)
- Trades both outcomes in 62% of markets (inventory/MM signature)
- Fast round-trips (<2h) in 56% of two-sided markets
- High-frequency cadence (median gap 16s)
- Heavy concentration in Over/Under sports totals (sports MM niche)
- Both-sides inventory: 5516 markets (61.71%)
- Clip USDC median/p90/max: $19.64 / $655.00 / $7,212.70
- Sport categories: `{'sports_match': 371550.43, 'sports_totals': 20617.95, 'crypto': 3.3}`
- Slug tokens: [('nba', 2418), ('nhl', 927), ('nfl', 628), ('atp', 276), ('wta', 219), ('ten', 192), ('mlb', 171), ('lal', 162), ('ucl', 45), ('mma', 31)]

### Maker vs Taker

| Leg | Maker % | Taker % | Maker fills | Taker fills |
|---|---:|---:|---:|---:|
| Entry | 75.54% | 24.46% | 106,487 | 12,818 |
| Exit | 1.73% | 98.27% | 1 | 10 |

- `enter_taker_exit_taker`: 5
- `enter_maker_exit_taker`: 4

### Price bands

| Band | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| 0-20¢ | 79 | 10.1% | -$25,220.90 | -$319.25 |
| 20-40¢ | 423 | 28.6% | $159,801.53 | $377.78 |
| 40-60¢ | 7858 | 51.2% | $133,059.22 | $16.93 |
| 60-80¢ | 434 | 78.1% | $100,054.11 | $230.54 |
| 80-100¢ | 144 | 84.7% | $24,477.71 | $169.98 |

## C. Equity & risk

- Final cashflow equity: $364,775.31
- Max drawdown: -$808,384.30 (-65700.4% of peak)
- Longest drawdown: 0 days
- Daily Sharpe (ann.): 0.449
- Profit factor: 1.0414
- Top 10 winners: $600,512.29 (7.91% of win PnL)
- Top 10 losers: -$543,562.91 (7.55% of loss PnL)
- Max inventory shares: 274377.96

### Top winners
- $113,953.16 · 11h17m · Spread: Utah State Aggies (-10.5)
- $85,597.66 · 9h35m · Tulane vs. Temple
- $71,389.74 · 5h22m · Heat vs. Lakers: O/U 232.5
- $64,009.54 · 20h46m · Nuggets vs. Trail Blazers
- $54,499.31 · 16h44m · Spread: Broncos (-8.5)
- $45,994.41 · 6h37m · Spread: Knicks (-8.5)
- $45,108.24 · 18h58m · Buccaneers vs. Rams: O/U 49.5
- $43,701.95 · 8h22m · Texas State vs. Southern Miss
- $38,261.32 · 11h03m · Hawks vs. Cavaliers: O/U 231.5
- $37,996.97 · 17h23m · Spread: Central Michigan (-9.5)

### Top losers
- -$30,622.12 · 5h40m · UAB Blazers vs. Rice
- -$36,742.02 · 20h38m · Nets vs. Celtics
- -$36,894.01 · 13h58m · Missouri vs. Oklahoma
- -$37,034.38 · 7h31m · Chiefs vs. Bills: O/U 50.5
- -$51,257.30 · 1h15m · Army vs. Air Force
- -$55,214.96 · 21h20m · Bills vs. Texans: O/U 44.5
- -$55,520.54 · 20h23m · Spread: Rockets (-7.5)
- -$70,979.38 · 15h52m · Spread: Florida State (-6.5)
- -$70,992.09 · 46m38s · Spread: Thunder (-8.5)
- -$98,306.11 · 6m26s · Spread: Virginia Cavaliers (-3.5)

## D. Trade management

### Hold-time buckets

| Bucket | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| <30s | 1696 | 51.6% | $1,617.95 | $0.95 |
| 30s-2m | 90 | 57.8% | $7,188.75 | $79.88 |
| 2-5m | 82 | 54.3% | $8,926.03 | $108.85 |
| 5-15m | 205 | 45.9% | -$96,688.51 | -$471.65 |
| 15m+ | 6865 | 51.7% | $471,127.45 | $68.63 |

- After early adverse (>2¢ vs entry within 2m): n=0, avg PnL n/a, median first-sell n/a, median hold n/a
- After favorable first sell (+2¢): n=0, avg PnL n/a, median MFE capture 1.0
- Campaigns (re-entry after flat): 4 (0.04%), avg entries 2.25, PnL $5.10, avg $1.27, WR 75.0%
- Single-entry: n=8934, PnL $392,166.58, avg $43.90
- Flatten-before-resolution flag rate: 0.948; hold-to-resolution style n=8929; redeems $26,027,412.51; merges $4,757,387.59
- Avg-down while MTM-red on losers: 2166/4322 (50.12%); Δ if skipped on those $0.00; global never-red-buy Δ $0.05

### Family mix

| Family | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| Other | 5059 | 51.8% | $277,429.20 | $54.84 |
| Over/Under | 3875 | 51.4% | $114,731.37 | $29.61 |
| Yes/No moneyline | 4 | 75.0% | $11.10 | $2.78 |

## E. Edge diagnosis

- Time to MFE (winners): median 13h09m, p25 n/a, p75 n/a, p90 13h09m
- Big MFE ≥10¢: n=0; within 30s=0; within 60s=0 (0.0% of big moves)

**Edge thesis:** Classic inventory MM — both-sides presence with spread capture; edge from quoting and inventory skew, not event sniping alone.

## F. vs polika72

| Metric | This trader | polika72 |
|---|---:|---:|
| identity | two_sided_inventory_mm | one_sided_informed_scalper |
| trades | 119316 | 19978 |
| cashflow_pnl | -4392612.2757 | 58204.9839 |
| win_rate | 0.5115 | 0.8008 |
| entry_taker_pct | 24.46 | 61.62 |
| both_sides_rate | 0.6171 | 0.0068 |
| median_clip | 19.6429 | 11.29 |
| campaign_pct | 0.04 | 5.85 |
| max_dd | -808384.2986 | -601.1817 |
| time_to_mfe_med | 47346 | 64 |

### Steal / avoid

- **Steal:** both-sides inventory discipline (closer to true MM than polika72).
- **Steal:** maker-led entries (better for quoting stack on Kalshi).
- **Avoid:** their drawdown profile — size down vs polika72 risk.
- **Avoid:** averaging down while red.

## G. Kalshi two-sided informed MM relevance

High relevance to a Kalshi two-sided informed MM: both-sides + quoting DNA. Port inventory caps, skew rules, and maker exit logic; replace Polymarket sports feed with Kalshi event feeds.
