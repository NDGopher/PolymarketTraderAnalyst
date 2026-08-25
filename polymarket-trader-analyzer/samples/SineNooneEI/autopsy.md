# Deep Trader Autopsy — SineNooneEI

- Wallet: `0x38337de21ff0bb0a11a40761507d51e318d633d1`
- Identity: **`directional_hold_to_resolution`**
- Primary focus: **sports_match**
- Span: 2026-02-03T12:59:50+00:00 → 2026-08-24T17:11:52+00:00 (202.18 days)
- Generated: 2026-08-25T21:55:39.320831+00:00

## A. Data integrity / reconciliation

| Source | PnL | Trades / notes |
|---|---:|---|
| Our cashflow realized | $541,301.28 | trades=16,603 |
| Our core cashflow | $523,137.79 | buys=16,599 sells=4 |
| Our closed-legs sum | $3,761,463.08 | closed=1,070 WR=79.5% |
| Polymarket leaderboard ALL | $639,212.87 | vol=$29,168,764.39 rank=318 |
| PolyData | $506,308.10 | trades=14776 WR=0.5312 |

- **DRIFT** `polymarket_leaderboard_ALL` pnl: ours=541301.2799 ref=639212.8736756515 diff=-97911.5938
- **MATCH** `polydata` realized_pnl: ours=523137.7892 ref=506308.1 diff=16829.6892
- **DRIFT** `polydata` n_trades: ours=16603 ref=14776 diff=1827
- **DRIFT** `polydata` win_rate: ours=0.7953 ref=0.5312 diff=0.2641
- **DRIFT** `internal` cashflow_vs_closed: ours=541301.2799 ref=3761463.0818 diff=-3220161.8019

## B. Core identity

- Scanner MM label: `hybrid_mm_directional` (score 30)
- Fast round-trips (<2h) in 100% of two-sided markets
- High-frequency cadence (median gap 12s)
- Both-sides inventory: 16 markets (1.01%)
- Clip USDC median/p90/max: $29.11 / $2,314.63 / $86,562.02
- Sport categories: `{'sports_match': 3639964.63, 'sports_totals': 94457.53, 'other': 27040.92}`
- Slug tokens: [('atp', 62), ('wta', 41), ('mlb', 6), ('nhl', 3), ('nba', 2)]

### Maker vs Taker

| Leg | Maker % | Taker % | Maker fills | Taker fills |
|---|---:|---:|---:|---:|
| Entry | 40.59% | 59.41% | 14,924 | 1,675 |
| Exit | 0.0% | 100.0% | 0 | 4 |

- `enter_maker_exit_taker`: 2
- `enter_taker_exit_taker`: 2

### Price bands

| Band | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| 0-20¢ | 29 | 61.5% | $68,889.33 | $2,375.49 |
| 20-40¢ | 382 | 69.9% | $1,219,824.16 | $3,193.26 |
| 40-60¢ | 664 | 75.8% | $994,426.76 | $1,497.63 |
| 60-80¢ | 473 | 90.4% | $1,410,157.89 | $2,981.31 |
| 80-100¢ | 32 | 88.5% | $68,164.95 | $2,130.15 |

## C. Equity & risk

- Final cashflow equity: $541,301.28
- Max drawdown: -$414,391.76 (-631.0% of peak)
- Longest drawdown: 6 days
- Daily Sharpe (ann.): 0.853
- Profit factor: 1.9658
- Top 10 winners: $815,751.94 (10.79% of win PnL)
- Top 10 losers: -$679,068.23 (17.87% of loss PnL)
- Max inventory shares: 179555.21

### Top winners
- $239,727.93 · 2s · LoL: Fnatic vs SK Gaming - Game 2 Winner
- $129,076.88 · 10h20m · Dota 2: Aurora vs MOUZ (BO3) - DreamLeague Stage 2
- $103,788.42 · 4h07m · LoL: T1 vs Dplus KIA (BO5) - LCK Cup Playoffs
- $66,004.70 · 0s · LoL: Dplus KIA vs DRX - Game 3 Winner
- $48,354.78 · 1h02m · Toronto Blue Jays vs. Baltimore Orioles: O/U 7.5
- $47,048.83 · 3h09m · Roland Garros ATP: Jakub Mensik vs Andrey Rublev
- $46,860.92 · 0s · Roland Garros WTA: Marta Kostyuk vs Mirra Andreeva
- $45,702.27 · 2h13m · LoL: Cloud9 vs FlyQuest (BO3) - LCS Lock In Group Stage
- $44,785.59 · 48s · LoL: DRX vs OKSavingsBank BRION - Game 2 Winner
- $44,401.63 · 2h31m · San Diego Padres vs. Washington Nationals: O/U 7.5

### Top losers
- -$45,213.06 · 1m40s · LoL: JD Gaming vs Top Esports - Game 2 Winner
- -$47,509.46 · 2m58s · LoL: Dplus KIA vs DN Freecs - Game 3 Winner
- -$49,989.72 · 8h20m · Counter-Strike: Vitality vs MOUZ (BO3) - IEM Krakow Playoffs
- -$52,198.45 · 2h55m · LoL: Cloud9 vs LYON (BO5) - LCS Lock In Playoffs
- -$59,675.53 · 6h26m · Counter-Strike: FURIA vs Vitality (BO5) - IEM Krakow Playoffs
- -$62,131.89 · 1m22s · LoL: DRX vs Nongshim Red Force - Game 1 Winner
- -$69,220.58 · 0s · LoL: Cloud9 vs LYON - Game 2 Winner
- -$81,935.18 · 1m56s · Will Chelsea FC win on 2026-03-14?
- -$84,487.84 · 20s · Counter-Strike: paiN vs Passion UA (BO3) - ESL Pro League Stage 1
- -$126,706.51 · 3h58m · Spread: Pistons (-8.5)

## D. Trade management

### Hold-time buckets

| Bucket | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| <30s | 1000 | 85.3% | $2,659,672.17 | $2,659.67 |
| 30s-2m | 303 | 73.2% | $349,628.85 | $1,153.89 |
| 2-5m | 76 | 70.2% | $12,785.85 | $168.23 |
| 5-15m | 25 | 55.0% | $16,849.11 | $673.96 |
| 15m+ | 176 | 74.7% | $722,527.10 | $4,105.27 |

- After early adverse (>2¢ vs entry within 2m): n=1, avg PnL $4,415.07, median first-sell 1m22s, median hold 1m22s
- After favorable first sell (+2¢): n=0, avg PnL n/a, median MFE capture None
- Campaigns (re-entry after flat): 1 (0.06%), avg entries 2, PnL $1,245.03, avg $1,245.03, WR 100.0%
- Single-entry: n=1579, PnL $3,760,218.05, avg $2,381.39
- Flatten-before-resolution flag rate: 0.6677; hold-to-resolution style n=1576; redeems $15,458,740.52; merges $0.00
- Avg-down while MTM-red on losers: 27/210 (12.86%); Δ if skipped on those $0.00; global never-red-buy Δ $0.00

### Family mix

| Family | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| Other | 1568 | 80.2% | $3,759,968.01 | $2,397.94 |
| Over/Under | 7 | 80.0% | $72,156.06 | $10,308.01 |
| Yes/No moneyline | 5 | 33.3% | -$70,660.99 | -$14,132.20 |

## E. Edge diagnosis

- Time to MFE (winners): median n/a, p25 n/a, p75 n/a, p90 n/a
- Big MFE ≥10¢: n=0; within 30s=0; within 60s=0 (0.0% of big moves)

**Edge thesis:** Directional positioning with significant redeem/merge cashflows — holds risk into resolution more than pure scalpers.

## F. vs polika72

| Metric | This trader | polika72 |
|---|---:|---:|
| identity | directional_hold_to_resolution | one_sided_informed_scalper |
| trades | 16603 | 19978 |
| cashflow_pnl | 541301.2799 | 58204.9839 |
| win_rate | 0.7953 | 0.8008 |
| entry_taker_pct | 59.41 | 61.62 |
| both_sides_rate | 0.0101 | 0.0068 |
| median_clip | 29.115 | 11.29 |
| campaign_pct | 0.06 | 5.85 |
| max_dd | -414391.7601 | -601.1817 |
| time_to_mfe_med | None | 64 |

### Steal / avoid

- **Avoid:** their drawdown profile — size down vs polika72 risk.
- **Avoid:** averaging down while red.

## G. Kalshi two-sided informed MM relevance

Moderate relevance — extract risk limits and hold-time discipline; do not assume their edge transfers without Kalshi-specific microstructure testing.
