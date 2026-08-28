# Deep Trader Autopsy — ImJustKen

- Wallet: `0x9d84ce0306f8551e02efef1680475fc0f1dc1344`
- Identity: **`directional_or_unclear`**
- Primary focus: **other**
- Span: 2022-12-12T20:58:21+00:00 → 2024-10-23T20:47:17+00:00 (680.99 days)
- Generated: 2026-08-28T14:44:11.294665+00:00

## A. Data integrity / reconciliation

| Source | PnL | Trades / notes |
|---|---:|---|
| Our cashflow realized | -$43,822,026.87 | trades=320,389 |
| Our core cashflow | -$44,806,140.80 | buys=279,362 sells=41,027 |
| Our closed-legs sum | -$27,767,466.73 | closed=17,542 WR=45.3% |
| Polymarket leaderboard ALL | $3,291,874.41 | vol=$499,524,708.36 rank=44 |
| PolyData | $3,289,074.81 | trades=606672 WR=0.6133 |

- **DRIFT** `polymarket_leaderboard_ALL` pnl: ours=-27767466.7259 ref=3291874.409581338 diff=-31059341.1355
- **DRIFT** `polydata` realized_pnl: ours=-27767466.7259 ref=3289074.81 diff=-31056541.5359
- **DRIFT** `polydata` n_trades: ours=320389 ref=606672 diff=-286283
- **DRIFT** `polydata` win_rate: ours=0.453 ref=0.6133 diff=-0.1603
- **DRIFT** `internal` cashflow_vs_closed: ours=-43822026.8674 ref=-27767466.7259 diff=-16054560.1415

## B. Core identity

- Scanner MM label: `hybrid_mm_directional` (score 35)
- Trades both outcomes in 83% of markets (inventory/MM signature)
- High-frequency cadence (median gap 40s)
- Both-sides inventory: 4349 markets (82.73%)
- Clip USDC median/p90/max: $6.27 / $364.18 / $257,495.53
- Sport categories: `{'other': 19220.4, 'sports_totals': -16085.98, 'crypto': -121139.39, 'politics': -7245792.84, 'sports_match': -16967287.73}`
- Slug tokens: [('nfl', 190), ('ten', 88), ('nba', 57), ('ucl', 18), ('mma', 15), ('nhl', 13), ('ufc', 2), ('bun', 2)]

### Maker vs Taker

| Leg | Maker % | Taker % | Maker fills | Taker fills |
|---|---:|---:|---:|---:|
| Entry | 74.37% | 25.63% | 263,209 | 16,153 |
| Exit | 70.85% | 29.15% | 38,814 | 2,213 |

- `enter_maker_exit_maker`: 709
- `enter_maker_exit_taker`: 493
- `enter_taker_exit_maker`: 181
- `enter_taker_exit_taker`: 173

### Price bands

| Band | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| 0-20¢ | 1003 | 15.0% | -$20,215,081.46 | -$20,154.62 |
| 20-40¢ | 1006 | 42.0% | -$1,992,145.43 | -$1,980.26 |
| 40-60¢ | 2207 | 62.9% | -$2,238,783.34 | -$1,014.40 |
| 60-80¢ | 600 | 71.1% | $263,988.01 | $439.98 |
| 80-100¢ | 430 | 73.4% | -$54,463.06 | -$126.66 |

## C. Equity & risk

- Final cashflow equity: $9,705,808.04
- Max drawdown: -$3,612,434.05 (-27.1% of peak)
- Longest drawdown: 496 days
- Daily Sharpe (ann.): 2.49
- Profit factor: 0.4002
- Top 10 winners: $1,248,933.97 (27.62% of win PnL)
- Top 10 losers: -$6,940,010.04 (24.05% of loss PnL)
- Max inventory shares: 5577209.17

### Top winners
- $326,714.68 · 204d · Will Kamala Harris win the 2024 Democratic Presidential Nomination?
- $232,267.78 · 154d · Will JD Vance win the 2024 Republican VP nomination?
- $123,657.72 · 53d · No change in Fed interest rates after 2024 September meeting?
- $105,343.08 · 53d · Fed decreases interest rates by 50+ bps after September 2024 meeting?
- $89,816.48 · 301d · Biden drops out of presidential race?
- $89,328.73 · 66d · Will another candidate win the 2024 Republican VP nomination?
- $81,513.10 · 213d · Will Fed cut interest rates 4 times in 2024?
- $71,576.93 · 256d · Will 'Inside Out 2' gross most in 2024?
- $65,890.56 · 79d · Fed decreases interest rates by 25 bps after November 2024 meeting?
- $62,824.90 · 87d · Will Erdoğan win the 2023 Turkish presidential election?

### Top losers
- -$680,019.60 · 282d · Will any other Democratic Politician win the 2024 US Presidential Election?
- -$685,841.98 · 276d · Will Ron DeSantis win the 2024 US Presidential Election?
- -$687,759.69 · 161d · Will AOC win the 2024 US Presidential Election?
- -$688,153.04 · 216d · Will Hillary Clinton win the 2024 US Presidential Election?
- -$693,213.93 · 289d · Will any other Republican Politician win the 2024 US Presidential Election?
- -$698,953.42 · 269d · Will Kanye West win the 2024 US Presidential Election?
- -$700,142.50 · 175d · Will Vivek Ramaswamy win the 2024 US Presidential Election?
- -$701,513.72 · 195d · Will Bernie Sanders win the 2024 US Presidential Election?
- -$702,031.32 · 175d · Will Elizabeth Warren win the 2024 US Presidential Election?
- -$702,380.84 · 159d · Will Chris Christie win the 2024 US Presidential Election?

## D. Trade management

### Hold-time buckets

| Bucket | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| <30s | 245 | 39.1% | -$50,813.07 | -$207.40 |
| 30s-2m | 16 | 28.6% | -$15,015.20 | -$938.45 |
| 2-5m | 18 | 47.1% | -$9,418.72 | -$523.26 |
| 5-15m | 18 | 47.1% | -$3,525.05 | -$195.84 |
| 15m+ | 4960 | 52.1% | -$24,252,313.51 | -$4,889.58 |

- After early adverse (>2¢ vs entry within 2m): n=0, avg PnL n/a, median first-sell n/a, median hold n/a
- After favorable first sell (+2¢): n=321, avg PnL $498.54, median MFE capture 1.0
- Campaigns (re-entry after flat): 79 (1.5%), avg entries 2.09, PnL -$328,879.88, avg -$4,163.04, WR 46.8%
- Single-entry: n=5178, PnL -$24,002,205.68, avg -$4,635.42
- Flatten-before-resolution flag rate: 0.6761; hold-to-resolution style n=3690; redeems $9,988,870.32; merges $53,557,823.91
- Avg-down while MTM-red on losers: 1838/2532 (72.59%); Δ if skipped on those $252,487.45; global never-red-buy Δ -$77,062.25

### Family mix

| Family | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| Yes/No moneyline | 5018 | 51.0% | -$24,267,477.04 | -$4,836.09 |
| Other | 235 | 61.6% | -$62,275.02 | -$265.00 |
| Over/Under | 4 | 25.0% | -$1,333.49 | -$333.37 |

## E. Edge diagnosis

- Time to MFE (winners): median 34d, p25 5d, p75 114d, p90 190d
- Big MFE ≥10¢: n=244; within 30s=0; within 60s=0 (0.0% of big moves)

**Edge thesis:** Hybrid / mixed — inspect maker-taker mix, hold buckets, and redeem share above.

## F. vs polika72

| Metric | This trader | polika72 |
|---|---:|---:|
| identity | directional_or_unclear | one_sided_informed_scalper |
| trades | 320389 | 19978 |
| cashflow_pnl | -43822026.8674 | 58204.9839 |
| win_rate | 0.453 | 0.8008 |
| entry_taker_pct | 25.63 | 61.62 |
| both_sides_rate | 0.8273 | 0.0068 |
| median_clip | 6.269 | 11.29 |
| campaign_pct | 1.5 | 5.85 |
| max_dd | -3612434.0531 | -601.1817 |
| time_to_mfe_med | 2951454 | 64 |

### Steal / avoid

- **Steal:** both-sides inventory discipline (closer to true MM than polika72).
- **Steal:** maker-led entries (better for quoting stack on Kalshi).
- **Avoid:** their drawdown profile — size down vs polika72 risk.
- **Avoid:** averaging down while red.

## G. Kalshi two-sided informed MM relevance

Moderate relevance — extract risk limits and hold-time discipline; do not assume their edge transfers without Kalshi-specific microstructure testing.
