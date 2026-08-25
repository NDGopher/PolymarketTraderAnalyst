# Deep Trader Autopsy — Anjun

- Wallet: `0x43372356634781eea88d61bbdd7824cdce958882`
- Identity: **`directional_or_unclear`**
- Primary focus: **sports_match**
- Span: 2022-12-12T21:33:03+00:00 → 2026-08-25T21:15:19+00:00 (1351.99 days)
- Generated: 2026-08-25T21:56:17.950447+00:00

## A. Data integrity / reconciliation

| Source | PnL | Trades / notes |
|---|---:|---|
| Our cashflow realized | -$16,535,033.07 | trades=293,079 |
| Our core cashflow | -$16,744,017.33 | buys=240,328 sells=52,751 |
| Our closed-legs sum | $4,747,733.59 | closed=17,499 WR=59.7% |
| Polymarket leaderboard ALL | $861,718.32 | vol=$180,326,675.11 rank=229 |
| PolyData | $736,777.34 | trades=353745 WR=0.5994 |

- **DRIFT** `polymarket_leaderboard_ALL` pnl: ours=4747733.5925 ref=861718.3206124196 diff=3886015.2719
- **DRIFT** `polydata` realized_pnl: ours=4747733.5925 ref=736777.34 diff=4010956.2525
- **DRIFT** `polydata` n_trades: ours=293079 ref=353745 diff=-60666
- **MATCH** `polydata` win_rate: ours=0.5965 ref=0.5994 diff=-0.0029
- **DRIFT** `internal` cashflow_vs_closed: ours=-16535033.0665 ref=4747733.5925 diff=-21282766.659

## B. Core identity

- Scanner MM label: `hybrid_mm_directional` (score 35)
- Trades both outcomes in 40% of markets (inventory/MM signature)
- High-frequency cadence (median gap 42s)
- Both-sides inventory: 5408 markets (40.23%)
- Clip USDC median/p90/max: $4.69 / $304.22 / $332,666.33
- Sport categories: `{'sports_match': 3453758.56, 'sports_totals': 609339.17, 'other': 220976.6, 'crypto': 61985.09, 'politics': -133107.96}`
- Slug tokens: [('nba', 401), ('ucl', 239), ('nhl', 237), ('nfl', 141), ('mlb', 137), ('ten', 136), ('lal', 65), ('bun', 55), ('ufc', 30), ('atp', 26), ('mma', 9), ('wta', 4)]

### Maker vs Taker

| Leg | Maker % | Taker % | Maker fills | Taker fills |
|---|---:|---:|---:|---:|
| Entry | 84.97% | 15.03% | 231,860 | 8,468 |
| Exit | 67.32% | 32.68% | 49,411 | 3,340 |

- `enter_maker_exit_maker`: 1773
- `enter_maker_exit_taker`: 1358
- `enter_taker_exit_taker`: 228
- `enter_taker_exit_maker`: 193

### Price bands

| Band | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| 0-20¢ | 2288 | 25.1% | -$168,265.55 | -$73.54 |
| 20-40¢ | 2293 | 52.3% | $1,206,784.00 | $526.29 |
| 40-60¢ | 4641 | 74.4% | $2,698,619.60 | $581.47 |
| 60-80¢ | 1709 | 79.1% | $734,773.04 | $429.94 |
| 80-100¢ | 2420 | 87.8% | $172,649.40 | $71.34 |

## C. Equity & risk

- Final cashflow equity: -$122,739.82
- Max drawdown: -$2,006,136.70 (-110.8% of peak)
- Longest drawdown: 1162 days
- Daily Sharpe (ann.): -0.018
- Profit factor: 1.7058
- Top 10 winners: $847,918.03 (10.68% of win PnL)
- Top 10 losers: -$761,134.95 (20.43% of loss PnL)
- Max inventory shares: 833332.0

### Top winners
- $131,664.69 · 10h18m · No change in Fed interest rates after July 2025 meeting?
- $105,113.49 · 394d · Will China invade Taiwan by end of 2026?
- $103,563.83 · 2d · Will "Avatar: Fire and Ash" Opening Weekend Box Office be less than 90m?
- $89,971.60 · 2d · Will 'Lilo & Stitch' gross between $140-150m opening weekend?
- $89,804.85 · 313d · Will A Minecraft Movie be the top grossing movie of 2025?
- $80,652.18 · 98d · Will Spain win the 2026 FIFA World Cup?
- $79,370.24 · 8h29m · Fed decreases interest rates by 25 bps after September 2025 meeting?
- $63,091.56 · 20d · Khamenei out as Supreme Leader of Iran by March 31?
- $55,574.03 · 2h45m · Will Nigeria vs. Morocco end in a draw?
- $49,111.57 · 18d · No change in Fed interest rates after June 2025 meeting?

### Top losers
- -$40,920.17 · 3h03m · Exact Score: Norway 2 - 1 England?
- -$41,271.80 · 5h16m · Fed decreases interest rates by 25 bps after May 2025 meeting?
- -$45,405.66 · 11d · No change in Fed interest rates after September 2025 meeting?
- -$48,324.87 · 5d · US strikes Iran by February 28, 2026?
- -$75,431.42 · 6d · Will 'Lilo & Stitch' gross less than $140m opening weekend?
- -$79,233.38 · 8h29m · Will 'Lilo & Stitch' gross between $150-160m opening weekend?
- -$89,994.77 · 97d · Will Zootopia 2 be the top grossing movie of 2025?
- -$99,899.08 · 3d · Will "Avatar: Fire and Ash" Opening Weekend Box Office be between 101m and 112m?
- -$101,960.43 · 1h49m · Will Jake Paul win his boxing match against Anthony Joshua?
- -$138,693.38 · 43m26s · Will Arsenal FC win on 2026-05-30?

## D. Trade management

### Hold-time buckets

| Bucket | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| <30s | 2986 | 76.7% | $1,556,343.36 | $521.21 |
| 30s-2m | 327 | 80.3% | $339,181.91 | $1,037.25 |
| 2-5m | 286 | 78.4% | $255,161.22 | $892.17 |
| 5-15m | 497 | 83.7% | $336,767.72 | $677.60 |
| 15m+ | 9346 | 64.1% | $1,725,497.25 | $184.62 |

- After early adverse (>2¢ vs entry within 2m): n=1, avg PnL $8.77, median first-sell 1m27s, median hold 8m32s
- After favorable first sell (+2¢): n=675, avg PnL $989.98, median MFE capture 1.0
- Campaigns (re-entry after flat): 852 (6.34%), avg entries 2.23, PnL $118,788.22, avg $139.42, WR 57.0%
- Single-entry: n=12590, PnL $4,094,163.23, avg $325.19
- Flatten-before-resolution flag rate: 0.6971; hold-to-resolution style n=9799; redeems $60,170,305.21; merges $21,146,747.00
- Avg-down while MTM-red on losers: 1565/3371 (46.43%); Δ if skipped on those $34,220.04; global never-red-buy Δ -$139,554.82

### Family mix

| Family | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| Yes/No moneyline | 8708 | 62.0% | $767,181.08 | $88.10 |
| Over/Under | 1296 | 84.2% | $543,838.01 | $419.63 |
| Other | 3438 | 78.9% | $2,901,932.37 | $844.08 |

## E. Edge diagnosis

- Time to MFE (winners): median 14h45m, p25 1h52m, p75 11d, p90 73d
- Big MFE ≥10¢: n=548; within 30s=4; within 60s=7 (1.28% of big moves)

**Edge thesis:** Hybrid / mixed — inspect maker-taker mix, hold buckets, and redeem share above.

## F. vs polika72

| Metric | This trader | polika72 |
|---|---:|---:|
| identity | directional_or_unclear | one_sided_informed_scalper |
| trades | 293079 | 19978 |
| cashflow_pnl | -16535033.0665 | 58204.9839 |
| win_rate | 0.5965 | 0.8008 |
| entry_taker_pct | 15.03 | 61.62 |
| both_sides_rate | 0.4023 | 0.0068 |
| median_clip | 4.6923 | 11.29 |
| campaign_pct | 6.34 | 5.85 |
| max_dd | -2006136.6952 | -601.1817 |
| time_to_mfe_med | 53114 | 64 |

### Steal / avoid

- **Steal:** both-sides inventory discipline (closer to true MM than polika72).
- **Steal:** maker-led entries (better for quoting stack on Kalshi).
- **Avoid:** their drawdown profile — size down vs polika72 risk.
- **Avoid:** averaging down while red.

## G. Kalshi two-sided informed MM relevance

Moderate relevance — extract risk limits and hold-time discipline; do not assume their edge transfers without Kalshi-specific microstructure testing.
