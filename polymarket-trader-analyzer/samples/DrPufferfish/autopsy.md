# Deep Trader Autopsy — DrPufferfish

- Wallet: `0xdb27bf2ac5d428a9c63dbc914611036855a6c56e`
- Identity: **`hybrid_liquidity_scalper`**
- Primary focus: **sports_match**
- Span: 2025-05-29T20:52:43+00:00 → 2026-01-12T20:49:11+00:00 (228.0 days)
- Generated: 2026-08-28T14:18:31.630086+00:00

## A. Data integrity / reconciliation

| Source | PnL | Trades / notes |
|---|---:|---|
| Our cashflow realized | $4,176,633.54 | trades=64,290 |
| Our core cashflow | $4,175,613.54 | buys=60,876 sells=3,414 |
| Our closed-legs sum | $46,297,730.97 | closed=881 WR=90.2% |
| Polymarket leaderboard ALL | $4,055,413.26 | vol=$248,548,251.18 rank=30 |
| PolyData | $4,055,413.26 | trades=272027 WR=0.481 |

- **MATCH** `polymarket_leaderboard_ALL` pnl: ours=4175613.5447 ref=4055413.259574452 diff=120200.2851
- **MATCH** `polydata` realized_pnl: ours=4175613.5447 ref=4055413.26 diff=120200.2847
- **DRIFT** `polydata` n_trades: ours=64290 ref=272027 diff=-207737
- **DRIFT** `polydata` win_rate: ours=0.9022 ref=0.481 diff=0.4212
- **DRIFT** `internal` cashflow_vs_closed: ours=4176633.543 ref=46297730.9682 diff=-42121097.4252

## B. Core identity

- Scanner MM label: `likely_market_maker` (score 55)
- Fast round-trips (<2h) in 30% of two-sided markets
- Avg sell > avg buy in 62% of markets (spread capture)
- High-frequency cadence (median gap 14s)
- Both-sides inventory: 81 markets (11.27%)
- Clip USDC median/p90/max: $1.98 / $108.42 / $248,000.00
- Sport categories: `{'sports_match': 12701974.54, 'sports_totals': 501166.19, 'other': 198386.06, 'crypto': 51128.55}`
- Slug tokens: [('nba', 286), ('nfl', 64), ('ucl', 55), ('lal', 43), ('mlb', 19), ('ufc', 15), ('ten', 11), ('bun', 7), ('nhl', 6), ('mma', 6), ('atp', 2)]

### Maker vs Taker

| Leg | Maker % | Taker % | Maker fills | Taker fills |
|---|---:|---:|---:|---:|
| Entry | 77.64% | 22.36% | 60,385 | 491 |
| Exit | 80.21% | 19.79% | 3,367 | 47 |

- `enter_maker_exit_maker`: 55
- `enter_maker_exit_taker`: 17
- `enter_taker_exit_taker`: 8
- `enter_taker_exit_maker`: 4

### Price bands

| Band | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| 0-20¢ | 127 | 74.2% | $1,108,752.75 | $8,730.34 |
| 20-40¢ | 151 | 89.7% | $4,540,068.24 | $30,066.68 |
| 40-60¢ | 266 | 91.6% | $6,532,097.53 | $24,556.76 |
| 60-80¢ | 113 | 97.7% | $1,356,925.63 | $12,008.19 |
| 80-100¢ | 42 | 97.1% | $144,351.35 | $3,436.94 |

## C. Equity & risk

- Final cashflow equity: $4,176,633.54
- Max drawdown: -$1,021,203.64 (-195.0% of peak)
- Longest drawdown: 0 days
- Daily Sharpe (ann.): 2.377
- Profit factor: 21.0256
- Top 10 winners: $3,274,310.35 (22.37% of win PnL)
- Top 10 losers: -$668,286.89 (56.52% of loss PnL)
- Max inventory shares: 763421.99

### Top winners
- $600,658.75 · 4d · Will the New York Knicks win the 2026 NBA Finals?
- $495,581.93 · 9h51m · Hawks vs. Knicks
- $315,612.42 · 15m12s · Hornets vs. Thunder
- $299,232.99 · 21m16s · Will Liverpool FC win on 2026-01-01?
- $289,219.21 · 2h52m · Nuggets vs. Mavericks
- $270,717.18 · 11h53m · Spread: Patriots (-3.5)
- $261,750.14 · 5h49m · Spread: Eagles (-4.5)
- $255,573.09 · 22h21m · Spurs vs. Lakers
- $252,076.15 · 14m00s · Spread: Broncos (-13.5)
- $233,888.50 · 0s · Spread: Raptors (-2.5)

### Top losers
- -$29,143.07 · 15h55m · UFC Fight Night: Muhammad vs. Machado Garry (Welterweight, Main Card)
- -$29,671.92 · 5d · Will the Seattle Mariners win the 2025 World Series?
- -$32,532.08 · 0s · Champions League Final: 3+ goals?
- -$39,793.93 · 1h06m · Thunder vs. Jazz
- -$65,540.87 · 44m40s · Eagles vs. Chargers
- -$67,653.93 · 30m04s · Falcons vs. Vikings
- -$84,368.74 · 20m08s · Spread: Thunder (-11.5)
- -$87,922.18 · 13m40s · Chiefs vs. Broncos
- -$108,248.05 · 8m26s · Spread: Pistons (-9.5)
- -$123,412.12 · 13h32m · Pistons vs. Celtics

## D. Trade management

### Hold-time buckets

| Bucket | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| <30s | 181 | 89.3% | $2,124,933.99 | $11,739.97 |
| 30s-2m | 37 | 100.0% | $669,395.66 | $18,091.77 |
| 2-5m | 41 | 100.0% | $944,608.13 | $23,039.22 |
| 5-15m | 68 | 89.2% | $847,113.77 | $12,457.56 |
| 15m+ | 392 | 86.1% | $8,866,603.79 | $22,618.89 |

- After early adverse (>2¢ vs entry within 2m): n=0, avg PnL n/a, median first-sell n/a, median hold n/a
- After favorable first sell (+2¢): n=23, avg PnL $64,298.24, median MFE capture 1.0
- Campaigns (re-entry after flat): 8 (1.11%), avg entries 2.25, PnL $130,448.55, avg $16,306.07, WR 62.5%
- Single-entry: n=711, PnL $13,322,206.78, avg $18,737.28
- Flatten-before-resolution flag rate: 0.5396; hold-to-resolution style n=615; redeems $28,094,127.30; merges $0.00
- Avg-down while MTM-red on losers: 9/45 (20.0%); Δ if skipped on those -$2,007.97; global never-red-buy Δ -$18,062.45

### Family mix

| Family | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| Yes/No moneyline | 332 | 85.2% | $2,807,111.09 | $8,455.15 |
| Other | 375 | 91.5% | $10,619,619.38 | $28,318.99 |
| Over/Under | 12 | 100.0% | $25,924.87 | $2,160.41 |

## E. Edge diagnosis

- Time to MFE (winners): median 5h12m, p25 1h39m, p75 18h30m, p90 2d
- Big MFE ≥10¢: n=15; within 30s=0; within 60s=0 (0.0% of big moves)

**Edge thesis:** Hybrid / mixed — inspect maker-taker mix, hold buckets, and redeem share above.

## F. vs polika72

| Metric | This trader | polika72 |
|---|---:|---:|
| identity | hybrid_liquidity_scalper | one_sided_informed_scalper |
| trades | 64290 | 19978 |
| cashflow_pnl | 4176633.543 | 58204.9839 |
| win_rate | 0.9022 | 0.8008 |
| entry_taker_pct | 22.36 | 61.62 |
| both_sides_rate | 0.1127 | 0.0068 |
| median_clip | 1.976 | 11.29 |
| campaign_pct | 1.11 | 5.85 |
| max_dd | -1021203.6444 | -601.1817 |
| time_to_mfe_med | 18729 | 64 |

### Steal / avoid

- **Steal:** maker-led entries (better for quoting stack on Kalshi).
- **Avoid:** their drawdown profile — size down vs polika72 risk.
- **Avoid:** averaging down while red.

## G. Kalshi two-sided informed MM relevance

Moderate relevance — extract risk limits and hold-time discipline; do not assume their edge transfers without Kalshi-specific microstructure testing.
