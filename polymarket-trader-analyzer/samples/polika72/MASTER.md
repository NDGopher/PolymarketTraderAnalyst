# MASTER AUTOPSY — polika72

> Single file for humans **and** bots. Machine-readable twin: `MASTER.json` · Equity: `equity_curve.csv`.

- Wallet: `0x13997bdbf1b291b7ba65afaf1f0d8e4719ee48c8`
- Generated: `2026-08-25T21:55:26.311503+00:00`
- Identity class: **`one_sided_informed_scalper`**

## 0. Executive verdict

This trader is classified as **one_sided_informed_scalper** with primary focus **sports_totals**. Preferred PnL (**cashflow_core**) **$57,699.08** (leaderboard ALL $57,431.61; MATCH). Unique trades **19,978**. Copy difficulty **8/10** · ease **3/10**. Requires live event latency + execution; pattern is clear but edge is speed/data.

**Exit mechanics:** `sell_secondary_market`
**Kalshi two-sided MM fit:** MEDIUM — use as taker/impulse overlay on a Kalshi MM core, not as the core itself
**Preferred PnL note:** Cashflow usually tracks leaderboard for buy+sell scalpers.

## 1. Reconciliation (mandatory)

| Source | PnL | Extra |
|---|---:|---|
| **Preferred (cashflow_core)** | **$57,699.08** | vs LB diff=267.47 |
| Ours cashflow realized | $58,204.98 | trades=19,978 buy_only=False |
| Ours core (ex-rebate) | $57,699.08 | WR legs=80.08% |
| Ours closed-legs sum | $61,909.37 | PF=3.2979 |
| Polymarket leaderboard ALL | $57,431.61 | vol=$1,050,695.46 rank=3240 |
| PolyData | $52,640.69 | trades=24078 WR=0.6567 |

- MATCH: `polymarket_leaderboard_ALL` pnl ours=57699.0816 field=cashflow_core ref=57431.607979187625 diff=267.4736
- DRIFT: `polydata` realized_pnl ours=57699.0816 field=cashflow_core ref=52640.69 diff=5058.3916
- DRIFT: `polydata` n_trades ours=19978 field=None ref=24078 diff=-4100
- DRIFT: `polydata` win_rate ours=0.8008 field=None ref=0.6567 diff=0.1441
- MATCH: `internal` cashflow_vs_closed ours=58204.9839 field=None ref=61909.3681 diff=-3704.3842

## 2. Identity & microstructure

- Both-sides rate: 0.68% (37 markets)
- Clip median/p90/max: $10.57 / $52.52 / $1,479.63
- Category PnL: `{'sports_totals': 40877.63, 'sports_match': 14704.2, 'other': 6180.6, 'crypto': 146.94}`
- Start BUY first: 5422 · SELL first: 0
- Entry maker/taker: 38.38% / 61.62% (3,899/5,178 fills)
- Exit maker/taker: 49.09% / 50.91% (6,935/3,966 fills)
- Patterns: `{'enter_taker_exit_taker': 1468, 'enter_taker_exit_maker': 1723, 'enter_maker_exit_maker': 1062, 'enter_maker_exit_taker': 680}`

### Outcome volume (top)

| Outcome | Buy USDC | Sell USDC | Sell−Buy |
|---|---:|---:|---:|
| Over | $157,034.80 | $196,259.93 | $39,225.13 |
| Yes | $34,911.66 | $48,246.35 | $13,334.69 |
| No | $8,916.84 | $14,808.30 | $5,891.46 |
| United States | $34.64 | $118.84 | $84.20 |
| Colombia | $45.00 | $65.87 | $20.87 |
| Germany | $30.90 | $32.16 | $1.26 |
| Panama | $44.99 | $3.91 | -$41.08 |
| Bosnia and Herzegovina | $15.95 | $26.65 | $10.70 |
| Jeonbuk Hyundai Motors FC | $16.38 | $25.34 | $8.96 |
| AA Ponte Preta | $17.98 | $20.56 | $2.58 |
| FC Sheriff Tiraspol | $17.10 | $17.82 | $0.72 |
| Hammarby IF | $14.95 | $19.62 | $4.68 |

## 3. Performance metrics (kitchen sink)

- Expectancy / market: $12.37
- Avg win / avg loss: $22.13 / -$27.07 · ratio=0.8175
- PnL / day: $350.82 · trades/day=120.41 · markets/day=32.68
- PnL concentration HHI: 0.001245 (higher=more concentrated)
- Notional sum: $462,179.70 · median ticket $10.57
- Buy price median: 0.48 · Sell price median: 0.61
- Activity types: `{'DEPOSIT': 8, 'TRADE': 19978, 'REDEEM': 2321, 'MAKER_REBATE': 108, 'WITHDRAWAL': 20, 'TAKER_REBATE': 10}`
- Open risk: `{'n': 424, 'cash_pnl': -8115.1, 'current_value': 0.0, 'redeemable': 424}`

### Hold-time engine

| Bucket | N | WR | Total PnL | Avg | Median |
|---|---:|---:|---:|---:|---:|
| <30s | 717 | 74.87% | $2,351.19 | $3.28 | $0.00 |
| 30s-2m | 3234 | 86.65% | $42,763.37 | $13.22 | $5.44 |
| 2-5m | 731 | 64.54% | $2,609.46 | $3.57 | $1.33 |
| 5-15m | 291 | 59.49% | $442.89 | $1.52 | $1.70 |
| 15m+ | 449 | 75.41% | $13,742.46 | $30.61 | $11.51 |

### Entry price bands

| Band | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| 0-20¢ | 909 | 70.96% | $4,517.97 | $4.97 |
| 20-40¢ | 1285 | 77.24% | $15,230.70 | $11.85 |
| 40-60¢ | 1494 | 82.06% | $22,820.93 | $15.28 |
| 60-80¢ | 1463 | 86.36% | $17,974.32 | $12.29 |
| 80-100¢ | 271 | 78.36% | $1,365.45 | $5.04 |

### Family

| Family | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| Over/Under | 3543 | 77.91% | $40,676.84 | $11.48 |
| Yes/No moneyline | 1743 | 84.32% | $21,062.80 | $12.08 |
| Other | 136 | 87.20% | $169.73 | $1.25 |

## 4. Equity curve (critical)

### 4a. Cashflow activity equity

- Final equity (cashflow): **$58,204.98**
- Max DD: **-$601.18** (-1.28% of peak)
- Longest DD: **0 days**
- Daily Sharpe (ann.): **14.692**
- Days: 166

Files: `equity_curve.csv` · `equity_curve.json` (source=`cashflow_activity`)

<details><summary>Daily cashflow equity table (full)</summary>

| Date | Equity | Daily PnL | Drawdown |
|---|---:|---:|---:|
| 2026-03-12 | 144.53 | 144.53 | 0.00 |
| 2026-03-13 | 222.84 | 78.31 | 0.00 |
| 2026-03-14 | 394.57 | 171.73 | 0.00 |
| 2026-03-15 | 505.51 | 110.94 | 0.00 |
| 2026-03-16 | 511.68 | 6.17 | 0.00 |
| 2026-03-17 | 1116.63 | 604.95 | 0.00 |
| 2026-03-18 | 1572.74 | 456.11 | 0.00 |
| 2026-03-19 | 1660.79 | 88.05 | 0.00 |
| 2026-03-20 | 1836.77 | 175.98 | 0.00 |
| 2026-03-21 | 2461.27 | 624.50 | 0.00 |
| 2026-03-22 | 3131.21 | 669.94 | 0.00 |
| 2026-03-23 | 3142.80 | 11.58 | 0.00 |
| 2026-03-24 | 3178.36 | 35.56 | 0.00 |
| 2026-03-25 | 3224.26 | 45.90 | 0.00 |
| 2026-03-26 | 3590.45 | 366.19 | 0.00 |
| 2026-03-27 | 3755.32 | 164.88 | 0.00 |
| 2026-03-28 | 3852.84 | 97.51 | 0.00 |
| 2026-03-29 | 4038.49 | 185.65 | 0.00 |
| 2026-03-30 | 4053.53 | 15.05 | 0.00 |
| 2026-03-31 | 4581.86 | 528.32 | 0.00 |
| 2026-04-01 | 4766.71 | 184.85 | 0.00 |
| 2026-04-02 | 5191.83 | 425.12 | 0.00 |
| 2026-04-03 | 5920.35 | 728.53 | 0.00 |
| 2026-04-04 | 7956.87 | 2036.52 | 0.00 |
| 2026-04-05 | 9139.60 | 1182.73 | 0.00 |
| 2026-04-06 | 9522.11 | 382.52 | 0.00 |
| 2026-04-07 | 9761.34 | 239.23 | 0.00 |
| 2026-04-08 | 10171.01 | 409.66 | 0.00 |
| 2026-04-09 | 10514.65 | 343.64 | 0.00 |
| 2026-04-10 | 10787.56 | 272.91 | 0.00 |
| 2026-04-11 | 13020.44 | 2232.88 | 0.00 |
| 2026-04-12 | 14344.61 | 1324.17 | 0.00 |
| 2026-04-13 | 14940.95 | 596.34 | 0.00 |
| 2026-04-14 | 15821.64 | 880.69 | 0.00 |
| 2026-04-15 | 15998.57 | 176.94 | 0.00 |
| 2026-04-16 | 16602.55 | 603.98 | 0.00 |
| 2026-04-17 | 17374.70 | 772.15 | 0.00 |
| 2026-04-18 | 19282.80 | 1908.10 | 0.00 |
| 2026-04-19 | 20901.66 | 1618.85 | 0.00 |
| 2026-04-20 | 21471.99 | 570.33 | 0.00 |
| 2026-04-21 | 21812.38 | 340.39 | 0.00 |
| 2026-04-22 | 21934.21 | 121.83 | 0.00 |
| 2026-04-23 | 22270.83 | 336.63 | 0.00 |
| 2026-04-24 | 22769.62 | 498.78 | 0.00 |
| 2026-04-25 | 23014.74 | 245.12 | 0.00 |
| 2026-04-26 | 23996.02 | 981.28 | 0.00 |
| 2026-04-27 | 24668.48 | 672.46 | 0.00 |
| 2026-04-28 | 24987.80 | 319.32 | 0.00 |
| 2026-04-29 | 25001.68 | 13.88 | 0.00 |
| 2026-04-30 | 25483.39 | 481.70 | 0.00 |
| 2026-05-01 | 25701.11 | 217.73 | 0.00 |
| 2026-05-02 | 27317.83 | 1616.72 | 0.00 |
| 2026-05-03 | 27722.34 | 404.51 | 0.00 |
| 2026-05-04 | 27742.33 | 19.99 | 0.00 |
| 2026-05-05 | 27886.87 | 144.53 | 0.00 |
| 2026-05-06 | 27970.25 | 83.38 | 0.00 |
| 2026-05-07 | 27994.24 | 24.00 | 0.00 |
| 2026-05-08 | 27956.92 | -37.32 | -37.32 |
| 2026-05-09 | 28214.08 | 257.16 | 0.00 |
| 2026-05-10 | 28286.14 | 72.06 | 0.00 |
| 2026-05-11 | 28442.19 | 156.05 | 0.00 |
| 2026-05-12 | 28524.46 | 82.27 | 0.00 |
| 2026-05-13 | 28958.66 | 434.20 | 0.00 |
| 2026-05-14 | 29045.09 | 86.42 | 0.00 |
| 2026-05-15 | 29278.31 | 233.22 | 0.00 |
| 2026-05-16 | 29812.01 | 533.71 | 0.00 |
| 2026-05-17 | 32343.39 | 2531.37 | 0.00 |
| 2026-05-18 | 32498.63 | 155.24 | 0.00 |
| 2026-05-19 | 32784.06 | 285.43 | 0.00 |
| 2026-05-20 | 33030.62 | 246.56 | 0.00 |
| 2026-05-21 | 33367.76 | 337.14 | 0.00 |
| 2026-05-22 | 33678.71 | 310.96 | 0.00 |
| 2026-05-23 | 34803.18 | 1124.47 | 0.00 |
| 2026-05-24 | 36056.43 | 1253.26 | 0.00 |
| 2026-05-25 | 36180.67 | 124.24 | 0.00 |
| 2026-05-26 | 36236.79 | 56.12 | 0.00 |
| 2026-05-27 | 36329.76 | 92.97 | 0.00 |
| 2026-05-28 | 36415.70 | 85.95 | 0.00 |
| 2026-05-29 | 36547.54 | 131.84 | 0.00 |
| 2026-05-30 | 36898.21 | 350.66 | 0.00 |
| 2026-05-31 | 37391.40 | 493.19 | 0.00 |
| 2026-06-01 | 37618.71 | 227.32 | 0.00 |
| 2026-06-02 | 37912.58 | 293.87 | 0.00 |
| 2026-06-03 | 37966.34 | 53.76 | 0.00 |
| 2026-06-04 | 38300.16 | 333.82 | 0.00 |
| 2026-06-05 | 38433.53 | 133.37 | 0.00 |
| 2026-06-06 | 38896.53 | 463.00 | 0.00 |
| 2026-06-07 | 39046.61 | 150.08 | 0.00 |
| 2026-06-08 | 39181.79 | 135.18 | 0.00 |
| 2026-06-09 | 39270.77 | 88.99 | 0.00 |
| 2026-06-10 | 39453.40 | 182.63 | 0.00 |
| 2026-06-11 | 39754.61 | 301.21 | 0.00 |
| 2026-06-12 | 40069.62 | 315.01 | 0.00 |
| 2026-06-13 | 40605.98 | 536.35 | 0.00 |
| 2026-06-14 | 42183.70 | 1577.73 | 0.00 |
| 2026-06-15 | 42818.12 | 634.42 | 0.00 |
| 2026-06-16 | 44906.42 | 2088.30 | 0.00 |
| 2026-06-17 | 44979.20 | 72.78 | 0.00 |
| 2026-06-18 | 44975.58 | -3.62 | -3.62 |
| 2026-06-19 | 44782.29 | -193.29 | -196.91 |
| 2026-06-20 | 45003.22 | 220.93 | 0.00 |
| 2026-06-21 | 45681.68 | 678.46 | 0.00 |
| 2026-06-22 | 45866.42 | 184.74 | 0.00 |
| 2026-06-23 | 45872.76 | 6.34 | 0.00 |
| 2026-06-24 | 46311.89 | 439.13 | 0.00 |
| 2026-06-25 | 46314.49 | 2.60 | 0.00 |
| 2026-06-26 | 46814.57 | 500.08 | 0.00 |
| 2026-06-27 | 46213.39 | -601.18 | -601.18 |
| 2026-06-28 | 46946.33 | 732.94 | 0.00 |
| 2026-06-29 | 47122.27 | 175.94 | 0.00 |
| 2026-06-30 | 47640.74 | 518.47 | 0.00 |
| 2026-07-01 | 48109.82 | 469.08 | 0.00 |
| 2026-07-03 | 48813.74 | 703.91 | 0.00 |
| 2026-07-04 | 48998.01 | 184.28 | 0.00 |
| 2026-07-05 | 49061.66 | 63.65 | 0.00 |
| 2026-07-06 | 49136.09 | 74.43 | 0.00 |
| 2026-07-07 | 49343.19 | 207.10 | 0.00 |
| 2026-07-08 | 49407.17 | 63.99 | 0.00 |
| 2026-07-09 | 49443.10 | 35.92 | 0.00 |
| 2026-07-10 | 49444.15 | 1.05 | 0.00 |
| 2026-07-11 | 49475.58 | 31.43 | 0.00 |
| 2026-07-12 | 49530.07 | 54.49 | 0.00 |
| 2026-07-13 | 49572.47 | 42.40 | 0.00 |
| 2026-07-14 | 49588.62 | 16.15 | 0.00 |
| 2026-07-15 | 49743.47 | 154.85 | 0.00 |
| 2026-07-16 | 49952.00 | 208.54 | 0.00 |
| 2026-07-17 | 50041.94 | 89.94 | 0.00 |
| 2026-07-18 | 50306.83 | 264.88 | 0.00 |
| 2026-07-19 | 50382.61 | 75.79 | 0.00 |
| 2026-07-20 | 50392.43 | 9.82 | 0.00 |
| 2026-07-21 | 50443.11 | 50.68 | 0.00 |
| 2026-07-22 | 50843.74 | 400.63 | 0.00 |
| 2026-07-23 | 51430.14 | 586.40 | 0.00 |
| 2026-07-24 | 51588.21 | 158.08 | 0.00 |
| 2026-07-25 | 51718.35 | 130.14 | 0.00 |
| 2026-07-26 | 52078.90 | 360.54 | 0.00 |
| 2026-07-27 | 52345.75 | 266.85 | 0.00 |
| 2026-07-28 | 52420.11 | 74.36 | 0.00 |
| 2026-07-29 | 52634.33 | 214.22 | 0.00 |
| 2026-07-30 | 52877.02 | 242.70 | 0.00 |
| 2026-07-31 | 52938.16 | 61.13 | 0.00 |
| 2026-08-01 | 53044.94 | 106.78 | 0.00 |
| 2026-08-02 | 53496.68 | 451.74 | 0.00 |
| 2026-08-03 | 53550.05 | 53.37 | 0.00 |
| 2026-08-04 | 53614.77 | 64.72 | 0.00 |
| 2026-08-05 | 53685.22 | 70.45 | 0.00 |
| 2026-08-06 | 53765.80 | 80.58 | 0.00 |
| 2026-08-07 | 53884.36 | 118.56 | 0.00 |
| 2026-08-08 | 54184.08 | 299.72 | 0.00 |
| 2026-08-09 | 54557.50 | 373.42 | 0.00 |
| 2026-08-10 | 54530.97 | -26.54 | -26.54 |
| 2026-08-11 | 54692.15 | 161.19 | 0.00 |
| 2026-08-12 | 55205.51 | 513.36 | 0.00 |
| 2026-08-13 | 55479.35 | 273.84 | 0.00 |
| 2026-08-14 | 55514.25 | 34.90 | 0.00 |
| 2026-08-15 | 55791.89 | 277.63 | 0.00 |
| 2026-08-16 | 56241.19 | 449.30 | 0.00 |
| 2026-08-17 | 56442.22 | 201.03 | 0.00 |
| 2026-08-18 | 56533.20 | 90.98 | 0.00 |
| 2026-08-19 | 56398.39 | -134.81 | -134.81 |
| 2026-08-20 | 56292.73 | -105.65 | -240.46 |
| 2026-08-21 | 56638.47 | 345.73 | 0.00 |
| 2026-08-22 | 57323.47 | 685.00 | 0.00 |
| 2026-08-23 | 58115.11 | 791.64 | 0.00 |
| 2026-08-24 | 58159.67 | 44.56 | 0.00 |
| 2026-08-25 | 58204.98 | 45.31 | 0.00 |

</details>

### 4b. Closed-positions equity (alt — critical for buy-only books)

- Final closed equity: **$61,909.37**
- Max DD: **-$1,347.91**
- Daily Sharpe (ann.): **10.102**
- Days: 163

Files: `equity_curve_closed.csv` · `equity_curve_closed.json` (source=`closed_positions`)

<details><summary>Daily closed equity table (full)</summary>

| Date | Equity | Daily PnL | Drawdown |
|---|---:|---:|---:|
| 2026-03-12 | 194.73 | 194.73 | 0.00 |
| 2026-03-13 | 217.96 | 23.23 | 0.00 |
| 2026-03-14 | 409.70 | 191.74 | 0.00 |
| 2026-03-15 | 506.47 | 96.78 | 0.00 |
| 2026-03-16 | 510.39 | 3.92 | 0.00 |
| 2026-03-17 | 515.29 | 4.90 | 0.00 |
| 2026-03-18 | 1532.30 | 1017.01 | 0.00 |
| 2026-03-19 | 1653.74 | 121.44 | 0.00 |
| 2026-03-20 | 1872.53 | 218.79 | 0.00 |
| 2026-03-21 | 2509.63 | 637.10 | 0.00 |
| 2026-03-22 | 2623.38 | 113.74 | 0.00 |
| 2026-03-23 | 2715.34 | 91.96 | 0.00 |
| 2026-03-25 | 2756.33 | 40.99 | 0.00 |
| 2026-03-26 | 3325.58 | 569.25 | 0.00 |
| 2026-03-27 | 3821.25 | 495.66 | 0.00 |
| 2026-03-28 | 3971.57 | 150.33 | 0.00 |
| 2026-03-29 | 4076.03 | 104.45 | 0.00 |
| 2026-03-30 | 4158.30 | 82.27 | 0.00 |
| 2026-03-31 | 4543.30 | 385.00 | 0.00 |
| 2026-04-01 | 4920.75 | 377.45 | 0.00 |
| 2026-04-02 | 5335.11 | 414.35 | 0.00 |
| 2026-04-03 | 6107.55 | 772.44 | 0.00 |
| 2026-04-04 | 7374.01 | 1266.46 | 0.00 |
| 2026-04-05 | 9900.86 | 2526.85 | 0.00 |
| 2026-04-06 | 11180.86 | 1280.00 | 0.00 |
| 2026-04-07 | 11424.48 | 243.62 | 0.00 |
| 2026-04-08 | 10756.56 | -667.92 | -667.92 |
| 2026-04-09 | 11298.21 | 541.65 | -126.26 |
| 2026-04-10 | 11905.39 | 607.18 | 0.00 |
| 2026-04-11 | 15391.09 | 3485.70 | 0.00 |
| 2026-04-12 | 17890.71 | 2499.62 | 0.00 |
| 2026-04-13 | 18086.54 | 195.84 | 0.00 |
| 2026-04-14 | 18142.66 | 56.12 | 0.00 |
| 2026-04-15 | 19836.72 | 1694.06 | 0.00 |
| 2026-04-16 | 21163.57 | 1326.85 | 0.00 |
| 2026-04-17 | 22102.80 | 939.23 | 0.00 |
| 2026-04-18 | 22763.56 | 660.75 | 0.00 |
| 2026-04-19 | 24360.60 | 1597.04 | 0.00 |
| 2026-04-20 | 24445.94 | 85.34 | 0.00 |
| 2026-04-21 | 24398.22 | -47.72 | -47.72 |
| 2026-04-22 | 23098.03 | -1300.20 | -1347.91 |
| 2026-04-23 | 23515.57 | 417.54 | -930.37 |
| 2026-04-24 | 24322.36 | 806.78 | -123.58 |
| 2026-04-25 | 24071.07 | -251.29 | -374.87 |
| 2026-04-26 | 25361.89 | 1290.82 | 0.00 |
| 2026-04-27 | 25733.10 | 371.20 | 0.00 |
| 2026-04-28 | 26183.28 | 450.18 | 0.00 |
| 2026-04-29 | 26260.61 | 77.33 | 0.00 |
| 2026-04-30 | 26597.83 | 337.22 | 0.00 |
| 2026-05-01 | 26837.93 | 240.10 | 0.00 |
| 2026-05-02 | 28804.12 | 1966.19 | 0.00 |
| 2026-05-03 | 29294.01 | 489.88 | 0.00 |
| 2026-05-04 | 29885.64 | 591.63 | 0.00 |
| 2026-05-05 | 30175.88 | 290.24 | 0.00 |
| 2026-05-06 | 30301.77 | 125.90 | 0.00 |
| 2026-05-07 | 30212.85 | -88.93 | -88.93 |
| 2026-05-08 | 30283.72 | 70.87 | -18.05 |
| 2026-05-09 | 30529.15 | 245.43 | 0.00 |
| 2026-05-10 | 31092.20 | 563.05 | 0.00 |
| 2026-05-11 | 31264.17 | 171.97 | 0.00 |
| 2026-05-12 | 31394.93 | 130.76 | 0.00 |
| 2026-05-13 | 31826.97 | 432.04 | 0.00 |
| 2026-05-14 | 31935.77 | 108.80 | 0.00 |
| 2026-05-15 | 32064.46 | 128.69 | 0.00 |
| 2026-05-16 | 32419.01 | 354.55 | 0.00 |
| 2026-05-17 | 34720.08 | 2301.08 | 0.00 |
| 2026-05-18 | 35269.16 | 549.07 | 0.00 |
| 2026-05-19 | 35537.31 | 268.16 | 0.00 |
| 2026-05-20 | 35769.18 | 231.87 | 0.00 |
| 2026-05-21 | 36018.16 | 248.98 | 0.00 |
| 2026-05-22 | 36432.75 | 414.59 | 0.00 |
| 2026-05-23 | 37444.23 | 1011.48 | 0.00 |
| 2026-05-24 | 38216.58 | 772.35 | 0.00 |
| 2026-05-25 | 38712.45 | 495.87 | 0.00 |
| 2026-05-26 | 38704.92 | -7.53 | -7.53 |
| 2026-05-27 | 38758.47 | 53.55 | 0.00 |
| 2026-05-28 | 38875.82 | 117.35 | 0.00 |
| 2026-05-29 | 39141.32 | 265.50 | 0.00 |
| 2026-05-30 | 39551.57 | 410.25 | 0.00 |
| 2026-05-31 | 39761.21 | 209.63 | 0.00 |
| 2026-06-01 | 40325.30 | 564.09 | 0.00 |
| 2026-06-02 | 40768.91 | 443.61 | 0.00 |
| 2026-06-03 | 40799.15 | 30.25 | 0.00 |
| 2026-06-04 | 41232.54 | 433.39 | 0.00 |
| 2026-06-05 | 41442.14 | 209.60 | 0.00 |
| 2026-06-06 | 41717.22 | 275.08 | 0.00 |
| 2026-06-07 | 41854.98 | 137.76 | 0.00 |
| 2026-06-08 | 42158.77 | 303.79 | 0.00 |
| 2026-06-09 | 43229.38 | 1070.62 | 0.00 |
| 2026-06-10 | 43662.94 | 433.56 | 0.00 |
| 2026-06-11 | 43929.96 | 267.02 | 0.00 |
| 2026-06-12 | 44272.51 | 342.55 | 0.00 |
| 2026-06-13 | 44723.03 | 450.52 | 0.00 |
| 2026-06-14 | 45769.29 | 1046.26 | 0.00 |
| 2026-06-15 | 46409.57 | 640.28 | 0.00 |
| 2026-06-16 | 47014.64 | 605.07 | 0.00 |
| 2026-06-17 | 47972.90 | 958.25 | 0.00 |
| 2026-06-18 | 47795.01 | -177.88 | -177.88 |
| 2026-06-19 | 47746.79 | -48.22 | -226.11 |
| 2026-06-20 | 47944.17 | 197.38 | -28.72 |
| 2026-06-21 | 47957.64 | 13.47 | -15.26 |
| 2026-06-22 | 48407.68 | 450.04 | 0.00 |
| 2026-06-23 | 48413.28 | 5.59 | 0.00 |
| 2026-06-24 | 48823.03 | 409.76 | 0.00 |
| 2026-06-26 | 49031.11 | 208.08 | 0.00 |
| 2026-06-27 | 48564.11 | -467.00 | -467.00 |
| 2026-06-28 | 49183.10 | 618.99 | 0.00 |
| 2026-06-29 | 49252.72 | 69.63 | 0.00 |
| 2026-06-30 | 49253.64 | 0.92 | 0.00 |
| 2026-07-01 | 49256.74 | 3.10 | 0.00 |
| 2026-07-03 | 49248.75 | -7.99 | -7.99 |
| 2026-07-04 | 49336.72 | 87.98 | 0.00 |
| 2026-07-05 | 49357.65 | 20.93 | 0.00 |
| 2026-07-06 | 49377.23 | 19.57 | 0.00 |
| 2026-07-07 | 49478.11 | 100.88 | 0.00 |
| 2026-07-08 | 49535.81 | 57.69 | 0.00 |
| 2026-07-09 | 49603.57 | 67.76 | 0.00 |
| 2026-07-11 | 49616.38 | 12.82 | 0.00 |
| 2026-07-12 | 49554.55 | -61.83 | -61.83 |
| 2026-07-13 | 49556.63 | 2.08 | -59.75 |
| 2026-07-14 | 49591.43 | 34.80 | -24.95 |
| 2026-07-15 | 49666.82 | 75.39 | 0.00 |
| 2026-07-16 | 49761.67 | 94.85 | 0.00 |
| 2026-07-17 | 49818.97 | 57.31 | 0.00 |
| 2026-07-18 | 49963.94 | 144.97 | 0.00 |
| 2026-07-19 | 49999.35 | 35.41 | 0.00 |
| 2026-07-20 | 50042.66 | 43.31 | 0.00 |
| 2026-07-21 | 50080.92 | 38.26 | 0.00 |
| 2026-07-22 | 50236.59 | 155.67 | 0.00 |
| 2026-07-23 | 50488.77 | 252.18 | 0.00 |
| 2026-07-24 | 50624.77 | 136.00 | 0.00 |
| 2026-07-25 | 50754.79 | 130.02 | 0.00 |
| 2026-07-26 | 51086.92 | 332.13 | 0.00 |
| 2026-07-27 | 51202.41 | 115.48 | 0.00 |
| 2026-07-28 | 51241.71 | 39.30 | 0.00 |
| 2026-07-29 | 51396.16 | 154.46 | 0.00 |
| 2026-07-30 | 51489.79 | 93.62 | 0.00 |
| 2026-07-31 | 51521.48 | 31.70 | 0.00 |
| 2026-08-01 | 51602.38 | 80.90 | 0.00 |
| 2026-08-02 | 51827.35 | 224.97 | 0.00 |
| 2026-08-03 | 51888.97 | 61.62 | 0.00 |
| 2026-08-04 | 51932.87 | 43.90 | 0.00 |
| 2026-08-05 | 52016.15 | 83.28 | 0.00 |
| 2026-08-06 | 52112.27 | 96.11 | 0.00 |
| 2026-08-07 | 52209.38 | 97.11 | 0.00 |
| 2026-08-08 | 52455.85 | 246.47 | 0.00 |
| 2026-08-09 | 52395.65 | -60.20 | -60.20 |
| 2026-08-10 | 52408.93 | 13.28 | -46.92 |
| 2026-08-11 | 52557.25 | 148.32 | 0.00 |
| 2026-08-12 | 53123.65 | 566.39 | 0.00 |
| 2026-08-13 | 53241.30 | 117.65 | 0.00 |
| 2026-08-14 | 53360.30 | 119.00 | 0.00 |
| 2026-08-15 | 53576.16 | 215.87 | 0.00 |
| 2026-08-16 | 53799.80 | 223.64 | 0.00 |
| 2026-08-17 | 53932.36 | 132.56 | 0.00 |
| 2026-08-18 | 54020.73 | 88.37 | 0.00 |
| 2026-08-19 | 54026.32 | 5.59 | 0.00 |
| 2026-08-20 | 54082.07 | 55.75 | 0.00 |
| 2026-08-21 | 54167.52 | 85.44 | 0.00 |
| 2026-08-22 | 54460.10 | 292.58 | 0.00 |
| 2026-08-23 | 55589.73 | 1129.63 | 0.00 |
| 2026-08-24 | 61871.16 | 6281.43 | 0.00 |
| 2026-08-25 | 61909.37 | 38.20 | 0.00 |

</details>

### Top winners / losers contribution

Top10 winners $6,051.67 (6.82% of wins) · Top10 losers -$4,429.46 (16.48% of losses) · PF=3.2979

- WIN $841.93 · 4344s · FC St. Pauli 1910 vs. FC Bayern München: O/U 3.5
- WIN $670.10 · 1728s · FC Bayern München vs. Real Madrid CF: O/U 4.5
- WIN $645.59 · 362s · FC Bayern München vs. Real Madrid CF: O/U 3.5
- WIN $640.86 · 4724s · FC St. Pauli 1910 vs. FC Bayern München: O/U 4.5
- WIN $629.26 · 138s · Will Club Atlético de Madrid win on 2026-08-23?
- WIN $564.47 · 786s · Will Real Madrid CF win on 2026-03-17?
- WIN $544.83 · 4208s · FC St. Pauli 1910 vs. FC Bayern München: O/U 2.5
- WIN $508.06 · 58s · Paris Saint-Germain vs. Aston Villa: O/U 3.5
- WIN $504.28 · 44s · Will Paris Saint-Germain FC win on 2026-04-14?
- WIN $502.30 · 570s · Netherlands vs. Japan: O/U 4.5

- LOSS -$384.52 · 1410s · Cádiz CF vs. Córdoba CF: O/U 4.5
- LOSS -$388.13 · 136s · Real Madrid CF vs. Deportivo Alavés: O/U 3.5
- LOSS -$414.38 · 490s · UD Las Palmas vs. SD Huesca: O/U 3.5
- LOSS -$416.80 · 74s · Sporting CP vs. Arsenal FC: O/U 2.5
- LOSS -$427.77 · 490s · RC Strasbourg Alsace vs. OGC Nice: O/U 4.5
- LOSS -$427.80 · 46s · Will Paris Saint-Germain FC win on 2026-04-22?
- LOSS -$471.20 · 4560s · Paris Saint-Germain FC vs. Liverpool FC: O/U 3.5
- LOSS -$474.32 · 226s · Panama vs. England: Both Teams to Score
- LOSS -$508.72 · 5250s · Melbourne City FC vs. Western Sydney Wanderers FC: O/U 4.5
- LOSS -$515.82 · 406s · RC Strasbourg Alsace vs. OGC Nice: O/U 3.5

## 5. Trade management deep dive

- Adverse early (>2¢): `{'n_early_adverse': 400, 'avg_pnl': -12.86, 'median_t_first_sell': 56, 'median_hold': 83}`
- Favorable first-sell: `{'n_first_sell_up_2c': 4058, 'avg_pnl': 18.13, 'median_mfe_capture': 1.0, 'mean_mfe_capture': 0.9582}`
- Campaigns: `{'n': 317, 'pct': 5.85, 'avg_entries': 2.09, 'pnl': 9675.13, 'avg_pnl': 30.52, 'win_rate': 0.8202, 'single_n': 5105, 'single_pnl': 52234.23, 'single_avg_pnl': 10.23}`
- Avg-down: `{'n_losers': 993, 'n_losers_with_red_buys': 15, 'pct_losers': 1.51, 'total_delta_if_skipped_on_losers': 62.53, 'global_fifo_sim': 58487.99, 'global_fifo_never_red_buy': 58429.79, 'global_delta': -58.2}`
- Resolution behavior: `{'flattened_before_flag_rate': 0.9035, 'hold_to_resolution_style_n': 489, 'redeems_usdc': 2147.2582870000015, 'merges_usdc': 0.0}`
- Latency: `{'time_to_mfe_median': 64, 'time_to_mfe_p25': 44, 'time_to_mfe_p75': 99, 'time_to_mfe_p90': 389, 'mfe_ge_10c_n': 3256, 'mfe_ge_10c_within_30s': 222, 'mfe_ge_10c_within_60s': 1624, 'pct_big_within_60s': 49.88}`

### What works / fails
- WORKS: Winners capture median spread 0.2 vs losers -0.04
- WORKS: Both-sides inventory on 0.8% of winning markets (losers 0.4%)
- WORKS: Hold bucket <5m: avg PnL $10.19 on 4682 markets (WR 75%)
- WORKS: Hold bucket 5-30m: avg PnL $7.58 on 440 markets (WR 60%)
- WORKS: Hold bucket 30m-2h: avg PnL $35.79 on 292 markets (WR 73%)
- WORKS: Entry band 0.20-0.40: avg $11.84 across 1287 markets
- WORKS: Entry band 0.40-0.60: avg $15.30 across 1490 markets
- WORKS: Entry band 0.60-0.80: avg $12.26 across 1464 markets
- WORKS: Buy-ladder behavior: fade-into-weakness markets=64, chase-up markets=253

## 6. Strategy overview (in depth)

# Strategy Dossier: polika72

- **Wallet:** `0x13997bdbf1b291b7ba65afaf1f0d8e4719ee48c8`
- **History span:** 2026-03-12T17:59:13+00:00 → 2026-08-25T15:48:07+00:00 (165.91 days)
- **Trades:** 19,978 (buys 9,077 / sells 10,901)
- **Markets touched:** 5,422
- **Closed positions:** 5,035

## Headline performance

| Metric | Value |
|---|---|
| Realized cashflow (sells − buys + redeems + rebates) | $58,204.98 |
| Core cashflow (ex-rebates) | $57,699.08 |
| Closed-positions realized sum | $61,909.37 |
| Win rate (closed) | 80.08% (4032W / 1003L) |
| Profit factor | 3.2979 |
| Gross wins / losses | $88,851.53 / -$26,942.16 |
| Equity max drawdown | -$2,214.97 |
| Polymarket leaderboard (ALL) | $57,431.61 PnL · vol $1,050,695.46 · rank 3240 |

## Source validation

- **MATCH** `polymarket_leaderboard_ALL` pnl: ours=57699.0816 ref=57431.607979187625 diff=267.4736
- **DRIFT** `polydata` realized_pnl: ours=57699.0816 ref=52640.69 diff=5058.3916
- **DRIFT** `polydata` n_trades: ours=19978 ref=24078 diff=-4100
- **DRIFT** `polydata` win_rate: ours=0.8008 ref=0.6567 diff=0.1441
- **MATCH** `internal` cashflow_vs_closed: ours=58204.9839 ref=61909.3681 diff=-3704.3842

## What kind of trader is this?

**Classification:** `likely_market_maker` (score 65/100)

- Fast round-trips (<2h) in 100% of two-sided markets
- Avg sell > avg buy in 84% of markets (spread capture)
- High-frequency cadence (median gap 45s)
- Heavy concentration in Over/Under sports totals (sports MM niche)

Supporting rates — both-sides markets: 0.0068, fast round-trips: 0.9984, spread-capture rate: 0.8376.

## Exact edge thesis

polika72 looks like a **market maker on a scanner score**, but the fill tape says otherwise: they almost never warehouse both outcomes. The real edge is **one-sided live scalping** on sports (especially O/U Over) — buy a clip, sell the same outcome higher within seconds/minutes, maker-biased, rinse and repeat. Equity compounds from thousands of small positive markouts, not from predicting finals.

See `bot_playbook.md` for the full entry/management/exit autopsy and bot architecture.

## Where the money comes from

- **sports_totals**: $40,877.63 across 3321 closed legs
- **sports_match**: $14,704.20 across 1135 closed legs
- **other**: $6,180.60 across 576 closed legs
- **crypto**: $146.94 across 3 closed legs

## Timing

- Peak UTC hours: 19, 18, 14, 0, 17
- Peak weekdays (0=Mon): [6, 5, 3]
- Median inter-trade gap: 45s

## Sizing

- Median ticket $10.57, mean $23.13, p90 $52.52, max $1,479.63
- Share size median 24.5, mean 49.1094

## Trade-by-trade pattern (representative winners)

These vignettes are reconstructed from fills: average entry, average exit, hold time, and closed realized PnL.

### FC St. Pauli 1910 vs. FC Bayern München: O/U 3.5
- Entries ≈ **0.370** · Exits ≈ **0.599** · Spread ≈ **0.229**
- Fills: 6 buys / 9 sells · hold 1h 12m · both-sides=False · realized $841.93

### FC Bayern München vs. Real Madrid CF: O/U 4.5
- Entries ≈ **0.544** · Exits ≈ **0.692** · Spread ≈ **0.148**
- Fills: 7 buys / 4 sells · hold 28m 48s · both-sides=False · realized $670.10

### FC Bayern München vs. Real Madrid CF: O/U 3.5
- Entries ≈ **0.651** · Exits ≈ **0.775** · Spread ≈ **0.124**
- Fills: 4 buys / 4 sells · hold 6m 2s · both-sides=False · realized $645.59

### FC St. Pauli 1910 vs. FC Bayern München: O/U 4.5
- Entries ≈ **0.188** · Exits ≈ **0.275** · Spread ≈ **0.087**
- Fills: 7 buys / 24 sells · hold 1h 18m · both-sides=False · realized $640.86

### Will Club Atlético de Madrid win on 2026-08-23?
- Entries ≈ **0.426** · Exits ≈ **0.748** · Spread ≈ **0.322**
- Fills: 2 buys / 3 sells · hold 2m 18s · both-sides=False · realized $629.26

### FC St. Pauli 1910 vs. FC Bayern München: O/U 2.5
- Entries ≈ **0.569** · Exits ≈ **0.889** · Spread ≈ **0.320**
- Fills: 5 buys / 6 sells · hold 1h 10m · both-sides=False · realized $544.83

### Paris Saint-Germain vs. Aston Villa: O/U 3.5
- Entries ≈ **0.360** · Exits ≈ **0.610** · Spread ≈ **0.250**
- Fills: 11 buys / 4 sells · hold 58s · both-sides=False · realized $508.06

### Will Paris Saint-Germain FC win on 2026-04-14?
- Entries ≈ **0.210** · Exits ≈ **0.650** · Spread ≈ **0.440**
- Fills: 3 buys / 9 sells · hold 44s · both-sides=False · realized $504.28

### Netherlands vs. Japan: O/U 4.5
- Entries ≈ **0.050** · Exits ≈ **0.136** · Spread ≈ **0.087**
- Fills: 3 buys / 4 sells · hold 9m 30s · both-sides=False · realized $502.30

### US Cremonese vs. Bologna FC 1909: O/U 2.5
- Entries ≈ **0.440** · Exits ≈ **0.670** · Spread ≈ **0.231**
- Fills: 3 buys / 17 sells · hold 1m 46s · both-sides=False · realized $463.71

## Top closed winners / losers

**Winners**
- FC St. Pauli 1910 vs. FC Bayern München: O/U 3.5: $841.93 · bought $508.32 · sold $838.49 · hold 1h 12m
- FC Bayern München vs. Real Madrid CF: O/U 4.5: $670.10 · bought $811.14 · sold $1,043.98 · hold 28m 48s
- FC Bayern München vs. Real Madrid CF: O/U 3.5: $645.59 · bought $755.61 · sold $908.66 · hold 6m 2s
- FC St. Pauli 1910 vs. FC Bayern München: O/U 4.5: $640.86 · bought $245.95 · sold $368.77 · hold 1h 18m
- Will Club Atlético de Madrid win on 2026-08-23?: $629.26 · bought $892.75 · sold $1,567.38 · hold 2m 18s
- Will Real Madrid CF win on 2026-03-17?: $564.47 · bought $44.59 · sold $609.06 · hold 13m 6s
- FC St. Pauli 1910 vs. FC Bayern München: O/U 2.5: $544.83 · bought $417.14 · sold $660.50 · hold 1h 10m
- Paris Saint-Germain vs. Aston Villa: O/U 3.5: $508.06 · bought $731.95 · sold $930.01 · hold 58s
- Will Paris Saint-Germain FC win on 2026-04-14?: $504.28 · bought $286.21 · sold $907.85 · hold 44s
- Netherlands vs. Japan: O/U 4.5: $502.30 · bought $297.03 · sold $817.91 · hold 9m 30s

**Losers**
- RC Strasbourg Alsace vs. OGC Nice: O/U 3.5: -$515.82 · bought $284.54 · sold $230.58
- Melbourne City FC vs. Western Sydney Wanderers FC: O/U 4.5: -$508.72 · bought $270.55 · sold $260.04
- Panama vs. England: Both Teams to Score: -$474.32 · bought $503.98 · sold $30.54
- Paris Saint-Germain FC vs. Liverpool FC: O/U 3.5: -$471.20 · bought $289.76 · sold $399.53
- Will Paris Saint-Germain FC win on 2026-04-22?: -$427.80 · bought $58.50 · sold $150.60
- RC Strasbourg Alsace vs. OGC Nice: O/U 4.5: -$427.77 · bought $123.17 · sold $81.78
- Sporting CP vs. Arsenal FC: O/U 2.5: -$416.80 · bought $47.18 · sold $42.35
- UD Las Palmas vs. SD Huesca: O/U 3.5: -$414.38 · bought $152.34 · sold $130.84
- Real Madrid CF vs. Deportivo Alavés: O/U 3.5: -$388.13 · bought $359.04 · sold $313.15
- Cádiz CF vs. Córdoba CF: O/U 4.5: -$384.52 · bought $100.00 · sold $239.85

## Replication playbook (how to copy the edge)

1. **Universe:** Focus on liquid sports match + totals (O/U) markets with tight books.
2. **Role:** Quote or take both sides near mid; prioritize markets you can exit before resolution.
3. **Sizing:** Start near their median ticket (~$10.57) and scale only with inventory limits.
4. **Inventory:** Cap net Yes/No (or Over/Under) imbalance; flatten when mid moves through you.
5. **Hold time:** Target minutes–hours, not overnight directional risk, unless hedged via opposite outcome.
6. **Edge source:** Capture spread + mean reversion after flow, not oracle forecasting alpha.
7. **Ops:** Automate via CLOB maker orders; track maker rebates; kill-switch on drawdown.
8. **Do not blindly copy:** Their edge depends on latency, fee tier, and bankroll. Replicate *mechanics*, not wallet follows.

## Cashflow anatomy

- Buys: $203,970.44
- Sells: $259,522.26
- Redeems: $2,147.26
- Maker rebates: $481.53
- Taker rebates: $24.37

_Generated 2026-08-25T21:55:26.000306+00:00_


## 7. Bot / copy playbook

- Difficulty: **8/10** · Ease: **3/10**
- Why: Requires live event latency + execution; pattern is clear but edge is speed/data.

### Build steps
1. Live sports feed (goals/shots/xG / play-by-play)
2. Taker entry on impulse + maker exit engine
3. Universe filter: liquid O/U / match markets
4. Markout kill-switch at +5s/+30s/+60s
5. No avg-down without new event confirmation
6. Size to clip median first; scale only after markout match

### Steal
- Short-horizon impulse capture within ~60s
- Prioritize hold bucket 30s-2m (their PnL engine)

### Avoid
- Don't copy size before matching markout distributions

Bot parameters: `{'preferred_entry_price_median': 0.4836, 'preferred_entry_price_p25_p75': (0.3, 0.66), 'target_spread_median': 0.2, 'target_spread_p75': 0.3137, 'max_hold_seconds_p75': 112, 'median_hold_seconds': 66, 'clip_size_usdc_median': 11.287, 'clip_size_usdc_p90': 53.32, 'both_sides_on_winners_rate': 0.0082, 'require_exit_above_entry': True, 'flatten_before_resolution': True, 'maker_bias': True}`

# Elite Replication Playbook — polika72

Wallet `0x13997bdbf1b291b7ba65afaf1f0d8e4719ee48c8`. Reverse-engineered from the **full unique fill tape** (19,978 trades · 5,422 markets). This is an implementation spec for a high-end bot, not vibes.

## 0. True strategy identity (read this first)

**polika72 is NOT a classic two-sided market maker.** Both-sides inventory is ~0–1% of winning markets. The real craft is:

> **Live / short-horizon one-sided scalping on sports markets (especially O/U Over)** — BUY a clip, then SELL the *same* outcome higher within seconds to a few minutes. Maker-biased. Repeat.

Evidence: BUY→SELL opens 3478/5422 episodes; median winner hold 1m06s; winner median spread (exit−entry) 0.2; Over PnL $40,676.84 vs Under $0.00; maker rebates $481.53 >> taker $24.37.

Heuristic label from the scanner may still say `likely_market_maker` because of fast round-trips + sell>buy + maker rebates. **Operationally, build a live scalper with optional maker quoting**, not a Yes/No pair inventory bot.

## 1. Performance anchors

| Source / metric | Value |
|---|---|
| Cashflow realized (sells−buys+redeems+rebates) | $58,204.98 |
| Core cashflow (ex-rebates) | $57,699.08 |
| Closed-position legs sum | $61,909.37 |
| Leg win rate / profit factor | 80.08% / 3.2979 |
| Polymarket leaderboard ALL | $57,431.61 · vol $1,050,695.46 · rank 3240 |
| polymarket_leaderboard_ALL pnl | ref=57431.607979187625 ours=57699.0816 (MATCH) |
| polydata realized_pnl | ref=52640.69 ours=57699.0816 (DRIFT) |
| polydata n_trades | ref=24078 ours=19978 (DRIFT) |
| polydata win_rate | ref=0.6567 ours=0.8008 (DRIFT) |

Notes: Polymarket leaderboard ALL is the primary official PnL check (we match within tolerance). PolyData uses a different event aggregation / trade counting method — expect DRIFT on WR and trade count; use it as a secondary research signal, not the ground truth for fills.

## 2. Universe — where the money is

- **O/U / totals:** 3543 markets · $40,676.84 · avg $11.48 · median hold 1m17s · median spread 0.14
- **Match / other sports:** 1407 markets · $19,244.14 · avg $13.68
- **Outcome PnL leaders:**
  - **Over**: $40,676.84
  - **Yes**: $15,710.24
  - **No**: $5,352.56
  - **United States**: $66.79
  - **CA Talleres**: $15.39
  - **Club Nacional de Football**: $11.05

### Bot universe rules

1. Only liquid live sports (soccer/football first — their tape is soccer-heavy).
2. Prefer O/U lines with tight books and active in-game trading.
3. Default bias toward **Over** unless your signal says otherwise (their Over PnL dominates).
4. Skip politics/crypto until you have separate evidence.
5. Require enough depth to enter ~median clip and exit within 1–2 minutes.

## 3. ENTRY — exact mechanics

### Style histogram
- `directional_buy_above_mid`: 1563
- `directional_buy_sub_mid`: 1371
- `directional_buy_cheap_tail`: 1264
- `directional_buy_near_mid`: 824
- `directional_buy_expensive_favorite`: 363
- `two_sided_inventory_near_mid`: 12
- `two_sided_inventory_sub_mid`: 10
- `two_sided_inventory_cheap_tail`: 7
- `two_sided_inventory_expensive_favorite`: 4
- `two_sided_inventory_above_mid`: 4

### First-two-fill sequences
- `BUY->SELL`: 3478
- `BUY->BUY`: 1570
- `single_fill`: 374

### Entry price → realized edge

| Avg buy band | Markets | Total PnL | Avg PnL |
|---|---:|---:|---:|
| 0.00-0.20 | 911 | $4,534.27 | $4.98 |
| 0.20-0.40 | 1287 | $15,243.27 | $11.84 |
| 0.40-0.60 | 1490 | $22,792.05 | $15.30 |
| 0.60-0.80 | 1464 | $17,941.96 | $12.26 |
| 0.80-1.00 | 270 | $1,397.81 | $5.18 |

**Best band:** 0.40–0.60 (near mid) — highest average PnL. Tails (≤0.20 or ≥0.80) make less per market.

### Entry checklist (bot)

1. Clip **$11.29** median (p90 $53.32).
2. Aim entry price ~**0.4836** (IQR (0.3, 0.66)).
3. Trigger = microstructure, not long-term forecast:
   - mid dips / liquidity hole you can buy
   - imminent volatility (attack, corner, shot) where Over can jump
   - resting bid gets lifted? you’re being taken — manage immediately
4. Prefer **maker bids**; take only if the expected jump already started and ask is still inside your edge.
5. Same-second multi-fills are normal (one order, many counterparties) — treat as one decision, many fills.

## 4. MANAGEMENT — what they do after entry

### Styles
- `single_clip`: 2720
- `scalp_sub_15m`: 1964
- `scale_in_scale_out`: 423
- `intraday_swing`: 281
- `market_make_both_outcomes`: 28
- `multi_hour_position`: 6

### Winners vs losers

| Metric | Winners | Losers |
|---|---:|---:|
| N | 4012 | 993 |
| PnL | $88,793.58 | -$26,884.21 |
| Median hold | 1m06s | 1m50s |
| Median spread | 0.2 | -0.04 |
| Scale-in rate | 0.2804 | 0.3897 |
| Scale-out rate | 0.4045 | 0.5186 |
| Avg fills/market | 3.71 | 4.15 |
| Both-sides rate | 0.0082 | 0.004 |

### The real management loop (one-sided scalp)

```
BUY clip(s) on Over (or chosen outcome)
   │
   ├─ price jumps in your favor within seconds → SELL in clips (scale-out)
   ├─ price chops flat → keep working asks above entry; time-stop
   └─ price dumps → cut quickly (losers show sell-below-buy); do NOT average forever
Optional: re-enter later cheaper if a second impulse sets up (seen in big O/U winners)
```

Critical deltas:

- **Winners** sell above buy (median spread **0.2**). **Losers** often exit worse (median spread **-0.04**).
- Losers scale-in **more** (0.3897 vs 0.2804) — averaging down is how they bleed; the bot should **forbid** revenge scale-ins without a fresh signal.
- Hold edge peaks in **<5m** ({'n': 4682, 'pnl': 47724.0203, 'avg': 10.1931, 'win_rate': 0.754}) and a strong **30m–2h** bucket for the larger in-game campaigns.

## 5. EXIT — rules that print

- `spread_harvest_sell_above_buy`: 4099
- `adverse_exit_sell_below_buy`: 734
- `hold_to_resolution_or_redeem`: 489
- `mixed_roundtrip`: 100

| Hold bucket | N | Total PnL | Avg | Win rate |
|---|---:|---:|---:|---:|
| <5m | 4682 | $47,724.02 | $10.19 | 75.4% |
| 5-30m | 440 | $3,334.56 | $7.58 | 59.6% |
| 30m-2h | 292 | $10,450.79 | $35.79 | 73.0% |
| 2-12h | 7 | $374.86 | $53.55 | 85.7% |
| 12h+ | 1 | $25.14 | $25.14 | 100.0% |

### Exit engine params

1. **TP / ask distance:** target ≈ **0.2** above avg entry (p75 stretch 0.3137). On live O/U this is often a burst move, not slow grind.
2. **Time stop:** median hold 1m06s; p75 1m52s for the scalps — escalate urgency after that.
3. **Scale-out:** peel into strength (their winners stack sells). Don’t wait for one perfect print.
4. **Stop:** if mid < entry − ~3–5¢ on unhedged inventory with no signal → take the loss (copy losers’ speed, not their hope).
5. **Flatten before resolution** — redeem is residual.
6. Taker exits are fine when the move already happened and maker asks won’t fill.

## 6. What works / what fails

### Works
- Winners capture median spread 0.2 vs losers -0.04
- Both-sides inventory on 0.8% of winning markets (losers 0.4%)
- Hold bucket <5m: avg PnL $10.19 on 4682 markets (WR 75%)
- Hold bucket 5-30m: avg PnL $7.58 on 440 markets (WR 60%)
- Hold bucket 30m-2h: avg PnL $35.79 on 292 markets (WR 73%)
- Entry band 0.20-0.40: avg $11.84 across 1287 markets
- Entry band 0.40-0.60: avg $15.30 across 1490 markets
- Entry band 0.60-0.80: avg $12.26 across 1464 markets
- Buy-ladder behavior: fade-into-weakness markets=64, chase-up markets=253

### Fails
- (no strong negative bucket)
- Chase vs fade ladders: `{'chase_up': 253, 'fade_down': 64}`

## 7. Fill-by-fill autopsies (copy these patterns)

### Example 1: FC St. Pauli 1910 vs. FC Bayern München: O/U 3.5
PnL $841.93 · hold 1h12m · 6B/9S · avg entry 0.3703 → exit 0.5992 (spread 0.2289) · `scale_in_scale_out`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-04-11T16:40:15+00:00 | BUY | Over | 256.45 | 0.4500 | 115.40 |
| 2026-04-11T16:40:15+00:00 | BUY | Over | 256.40 | 0.4470 | 114.61 |
| 2026-04-11T16:40:15+00:00 | BUY | Over | 256.45 | 0.4500 | 115.40 |
| 2026-04-11T16:41:37+00:00 | SELL | Over | 17.20 | 0.5900 | 10.15 |
| 2026-04-11T16:42:13+00:00 | SELL | Over | 3.02 | 0.5700 | 1.72 |
| 2026-04-11T16:42:15+00:00 | SELL | Over | 231.78 | 0.5700 | 132.11 |
| 2026-04-11T16:42:21+00:00 | SELL | Over | 265.00 | 0.5800 | 153.70 |
| 2026-04-11T16:42:21+00:00 | SELL | Over | 265.00 | 0.5800 | 153.70 |
| 2026-04-11T17:45:45+00:00 | BUY | Over | 201.13 | 0.2700 | 54.30 |
| 2026-04-11T17:45:45+00:00 | BUY | Over | 201.12 | 0.2700 | 54.30 |
| 2026-04-11T17:45:45+00:00 | BUY | Over | 201.12 | 0.2700 | 54.30 |
| 2026-04-11T17:48:01+00:00 | SELL | Over | 210.20 | 0.4371 | 91.89 |
| 2026-04-11T17:52:23+00:00 | SELL | Over | 39.00 | 0.7549 | 29.44 |
| 2026-04-11T17:52:25+00:00 | SELL | Over | 19.00 | 0.7500 | 14.25 |
| 2026-04-11T17:52:39+00:00 | SELL | Over | 349.10 | 0.7205 | 251.53 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 2: FC Bayern München vs. Real Madrid CF: O/U 3.5
PnL $645.59 · hold 6m02s · 4B/4S · avg entry 0.6513 → exit 0.775 (spread 0.1238) · `scale_in_scale_out`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-04-15T19:02:40+00:00 | BUY | Over | 351.06 | 0.6407 | 224.93 |
| 2026-04-15T19:02:40+00:00 | BUY | Over | 351.05 | 0.6400 | 224.67 |
| 2026-04-15T19:02:40+00:00 | BUY | Over | 351.05 | 0.6400 | 224.67 |
| 2026-04-15T19:03:16+00:00 | SELL | Over | 358.70 | 0.7500 | 269.02 |
| 2026-04-15T19:03:18+00:00 | SELL | Over | 358.70 | 0.7571 | 271.57 |
| 2026-04-15T19:03:26+00:00 | SELL | Over | 347.30 | 0.7900 | 274.37 |
| 2026-04-15T19:07:54+00:00 | BUY | Over | 107.03 | 0.7600 | 81.34 |
| 2026-04-15T19:08:42+00:00 | SELL | Over | 107.70 | 0.8700 | 93.70 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 3: FC St. Pauli 1910 vs. FC Bayern München: O/U 4.5
PnL $640.86 · hold 1h18m · 7B/24S · avg entry 0.1881 → exit 0.2751 (spread 0.087) · `scale_in_scale_out`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-04-11T16:40:15+00:00 | BUY | Over | 208.16 | 0.2600 | 54.12 |
| 2026-04-11T16:40:15+00:00 | BUY | Over | 208.17 | 0.2600 | 54.12 |
| 2026-04-11T16:40:15+00:00 | BUY | Over | 208.16 | 0.2600 | 54.12 |
| 2026-04-11T16:41:17+00:00 | SELL | Over | 85.00 | 0.3488 | 29.65 |
| 2026-04-11T16:41:19+00:00 | SELL | Over | 9.10 | 0.3200 | 2.91 |
| 2026-04-11T16:41:27+00:00 | SELL | Over | 203.40 | 0.3200 | 65.09 |
| 2026-04-11T16:42:01+00:00 | SELL | Over | 24.37 | 0.3000 | 7.31 |
| 2026-04-11T16:42:01+00:00 | SELL | Over | 132.60 | 0.3000 | 39.78 |
| 2026-04-11T16:42:01+00:00 | SELL | Over | 40.00 | 0.3000 | 12.00 |
| 2026-04-11T16:42:03+00:00 | SELL | Over | 40.29 | 0.3000 | 12.09 |
| 2026-04-11T16:42:03+00:00 | SELL | Over | 33.33 | 0.3000 | 10.00 |
| 2026-04-11T16:43:13+00:00 | SELL | Over | 70.80 | 0.3854 | 27.28 |
| 2026-04-11T17:45:45+00:00 | BUY | Over | 225.51 | 0.1200 | 27.06 |
| 2026-04-11T17:45:45+00:00 | BUY | Over | 225.49 | 0.1200 | 27.06 |
| 2026-04-11T17:45:45+00:00 | BUY | Over | 225.49 | 0.1200 | 27.06 |
| 2026-04-11T17:47:21+00:00 | SELL | Over | 37.80 | 0.1562 | 5.90 |
| 2026-04-11T17:48:21+00:00 | SELL | Over | 17.80 | 0.2300 | 4.09 |
| 2026-04-11T17:48:31+00:00 | SELL | Over | 61.38 | 0.1200 | 7.37 |
| 2026-04-11T17:48:33+00:00 | SELL | Over | 83.33 | 0.1200 | 10.00 |
| 2026-04-11T17:48:41+00:00 | SELL | Over | 75.20 | 0.2529 | 19.02 |
| 2026-04-11T17:51:27+00:00 | SELL | Over | 36.00 | 0.4100 | 14.76 |
| 2026-04-11T17:51:31+00:00 | SELL | Over | 36.00 | 0.4100 | 14.76 |
| 2026-04-11T17:51:31+00:00 | SELL | Over | 15.00 | 0.4100 | 6.15 |
| 2026-04-11T17:51:47+00:00 | SELL | Over | 15.00 | 0.4000 | 6.00 |
| 2026-04-11T17:51:49+00:00 | SELL | Over | 37.00 | 0.4000 | 14.80 |
| 2026-04-11T17:51:51+00:00 | SELL | Over | 15.00 | 0.4000 | 6.00 |
| 2026-04-11T17:52:07+00:00 | SELL | Over | 38.00 | 0.3900 | 14.82 |
| 2026-04-11T17:52:11+00:00 | SELL | Over | 27.60 | 0.3900 | 10.76 |
| 2026-04-11T17:58:05+00:00 | BUY | Over | 6.49 | 0.3700 | 2.40 |
| 2026-04-11T17:58:59+00:00 | SELL | Over | 6.60 | 0.6400 | 4.22 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 4: Will Club Atlético de Madrid win on 2026-08-23?
PnL $629.26 · hold 2m18s · 2B/3S · avg entry 0.426 → exit 0.7479 (spread 0.3219) · `scalp_sub_15m`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-08-23T16:24:07+00:00 | BUY | Yes | 1978.70 | 0.4249 | 840.78 |
| 2026-08-23T16:24:07+00:00 | BUY | Yes | 116.90 | 0.4446 | 51.98 |
| 2026-08-23T16:24:54+00:00 | SELL | Yes | 116.80 | 0.7500 | 87.60 |
| 2026-08-23T16:25:49+00:00 | SELL | Yes | 1978.60 | 0.7478 | 1479.63 |
| 2026-08-23T16:26:25+00:00 | SELL | Yes | 0.20 | 0.7500 | 0.15 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 5: Will Real Madrid CF win on 2026-03-17?
PnL $564.47 · hold 13m06s · 1B/2S · avg entry 0.07 → exit 0.9561 (spread 0.8861) · `scalp_sub_15m`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-03-17T21:51:37+00:00 | BUY | Yes | 637.00 | 0.0700 | 44.59 |
| 2026-03-17T21:52:33+00:00 | SELL | Yes | 171.70 | 0.8400 | 144.22 |
| 2026-03-17T22:04:43+00:00 | SELL | Yes | 465.30 | 0.9990 | 464.83 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 6: FC St. Pauli 1910 vs. FC Bayern München: O/U 2.5
PnL $544.83 · hold 1h10m · 5B/6S · avg entry 0.5686 → exit 0.8888 (spread 0.3202) · `scale_in_scale_out`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-04-11T16:40:15+00:00 | BUY | Over | 113.57 | 0.6639 | 75.40 |
| 2026-04-11T16:40:21+00:00 | BUY | Over | 6.06 | 0.6700 | 4.06 |
| 2026-04-11T16:42:21+00:00 | SELL | Over | 120.70 | 0.7900 | 95.35 |
| 2026-04-11T17:45:45+00:00 | BUY | Over | 204.66 | 0.5500 | 112.56 |
| 2026-04-11T17:45:45+00:00 | BUY | Over | 204.65 | 0.5500 | 112.56 |
| 2026-04-11T17:45:45+00:00 | BUY | Over | 204.65 | 0.5500 | 112.56 |
| 2026-04-11T17:46:51+00:00 | SELL | Over | 7.04 | 0.7100 | 5.00 |
| 2026-04-11T17:46:51+00:00 | SELL | Over | 6.00 | 0.7100 | 4.26 |
| 2026-04-11T17:46:53+00:00 | SELL | Over | 9.00 | 0.7100 | 6.39 |
| 2026-04-11T17:46:59+00:00 | SELL | Over | 202.00 | 0.7500 | 151.50 |
| 2026-04-11T17:50:23+00:00 | SELL | Over | 398.40 | 0.9990 | 398.00 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

## 8. Failure modes (do not bot these)

1. **RC Strasbourg Alsace vs. OGC Nice: O/U 3.5** -$515.82 · hold 6m46s · entry 0.34 → exit 0.27 · `scalp_sub_15m` / `adverse_exit_sell_below_buy`
2. **Melbourne City FC vs. Western Sydney Wanderers FC: O/U 4.5** -$508.72 · hold 1h27m · entry 0.2996 → exit 0.2866 · `scale_in_scale_out` / `adverse_exit_sell_below_buy`
3. **Panama vs. England: Both Teams to Score** -$474.32 · hold 3m46s · entry 0.66 → exit 0.04 · `single_clip` / `adverse_exit_sell_below_buy`
4. **Paris Saint-Germain FC vs. Liverpool FC: O/U 3.5** -$471.20 · hold 1h16m · entry 0.2806 → exit 0.47 · `scale_in_scale_out` / `spread_harvest_sell_above_buy`
5. **Will Paris Saint-Germain FC win on 2026-04-22?** -$427.80 · hold 46s · entry 0.06 → exit 0.15 · `single_clip` / `spread_harvest_sell_above_buy`
6. **RC Strasbourg Alsace vs. OGC Nice: O/U 4.5** -$427.77 · hold 8m10s · entry 0.17 → exit 0.11 · `scalp_sub_15m` / `adverse_exit_sell_below_buy`
7. **Sporting CP vs. Arsenal FC: O/U 2.5** -$416.80 · hold 1m14s · entry 0.06 → exit 0.0523 · `scalp_sub_15m` / `mixed_roundtrip`
8. **UD Las Palmas vs. SD Huesca: O/U 3.5** -$414.38 · hold 8m10s · entry 0.2097 → exit 0.1768 · `scalp_sub_15m` / `adverse_exit_sell_below_buy`
9. **Real Madrid CF vs. Deportivo Alavés: O/U 3.5** -$388.13 · hold 2m16s · entry 0.5837 → exit 0.507 · `scale_in_scale_out` / `adverse_exit_sell_below_buy`
10. **Cádiz CF vs. Córdoba CF: O/U 4.5** -$384.52 · hold 23m30s · entry 0.05 → exit 0.1199 · `intraday_swing` / `spread_harvest_sell_above_buy`

Common failure DNA: bought Over, game didn’t produce goals, sold lower or held into worthless.

## 9. Bot architecture (elite build)

```
LiveSportsFeed ──► Signal(impulse/dip) ──► Execution(maker-first)
                         │                      │
                         ▼                      ▼
                  PositionState ◄────── ExitEngine (TP/SL/time)
                         │
                         ▼
                   RiskGovernor (caps, kill switch)
```

### Modules

1. **LiveSportsFeed** — kickoff clock, shots, corners, goals (Opta/Betfair/odds APIs). Polymarket mid alone is laggy; their edge looks like **reacting to match state faster than the book**.
2. **Signal**
   - `dip_bid`: mid drops X¢ with depth refill → maker bid
   - `impulse_long_over`: attacking sequence / goal threat → bid or take Over
   - disable new entries near whistle/resolution
3. **Execution**
   - default post-only bids/asks; clip $11.29
   - allow taker for: (a) entry if signal already moving, (b) exit when TP prints through
   - cancel stale quotes > N seconds
4. **ExitEngine** — as in §5; always scale-out capable
5. **RiskGovernor**
   - max gross per market, max concurrent live matches
   - daily loss stop ≈ 1–2× median losing day from episode_stats
   - ban averaging down without new signal

### Core pseudocode

```python
for market in live_ou_markets():
    state = positions[market]
    if state.flat and signal.long_over(market):
        place_maker_bid(market, outcome='Over', clip=CLIP, limit=fair - buffer)
        # optional: take ask if impulse already underway and edge remains
    if state.long:
        work_asks_above(avg_entry + TARGET_SPREAD)
        if mid <= avg_entry - STOP or age > TIME_STOP:
            flatten(taker_ok=True)
        if mid >= avg_entry + TARGET_SPREAD:
            scale_out(fraction=0.5 then 0.5)
    if near_resolution(market):
        flatten(taker_ok=True)
```

## 10. Parameter block (start here)

```yaml
template: polika72
mode: one_sided_live_scalper  # not classic two-sided MM
preferred_outcome_bias: Over
clip_usdc_median: 11.287
clip_usdc_p90: 53.32
entry_price_median: 0.4836
entry_price_iqr: (0.3, 0.66)
target_spread: 0.2
target_spread_p75: 0.3137
median_hold_seconds: 66
max_hold_seconds_p75: 112
maker_bias: true
taker_allowed: entry_impulse_or_exit_urgency
both_sides_hedge: false  # tape does not support this as primary
avg_down_without_signal: false
flatten_before_resolution: true
```

## 11. Build roadmap

1. Replay their O/U Over fills against match timelines — confirm signal = live events.
2. Paper quoter on 3 leagues they touch most; match clip + hold distributions.
3. Enable maker entries only; measure markout at +30s/+2m.
4. Add taker impulse entries; compare markout.
5. Production with tiny clips; scale only when markout stays positive after fees.
6. Weekly `polyanalyst update polika72` — if their hold/spread regime shifts, re-fit params.

_Research only. Latency, fee tier, and sports-data quality decide whether this edge is yours._

_Generated 2026-08-25T21:55:26.000575+00:00_


## 8. Structured autopsy (A–G)

# Deep Trader Autopsy — polika72

- Wallet: `0x13997bdbf1b291b7ba65afaf1f0d8e4719ee48c8`
- Identity: **`one_sided_informed_scalper`**
- Primary focus: **sports_totals**
- Span: 2026-03-12T17:59:13+00:00 → 2026-08-25T15:48:07+00:00 (165.91 days)
- Generated: 2026-08-25T21:55:25.999959+00:00

## A. Data integrity / reconciliation

| Source | PnL | Trades / notes |
|---|---:|---|
| Our cashflow realized | $58,204.98 | trades=19,978 |
| Our core cashflow | $57,699.08 | buys=9,077 sells=10,901 |
| Our closed-legs sum | $61,909.37 | closed=5,035 WR=80.1% |
| Polymarket leaderboard ALL | $57,431.61 | vol=$1,050,695.46 rank=3240 |
| PolyData | $52,640.69 | trades=24078 WR=0.6567 |

- **MATCH** `polymarket_leaderboard_ALL` pnl: ours=57699.0816 ref=57431.607979187625 diff=267.4736
- **DRIFT** `polydata` realized_pnl: ours=57699.0816 ref=52640.69 diff=5058.3916
- **DRIFT** `polydata` n_trades: ours=19978 ref=24078 diff=-4100
- **DRIFT** `polydata` win_rate: ours=0.8008 ref=0.6567 diff=0.1441
- **MATCH** `internal` cashflow_vs_closed: ours=58204.9839 ref=61909.3681 diff=-3704.3842

## B. Core identity

- Scanner MM label: `likely_market_maker` (score 65)
- Fast round-trips (<2h) in 100% of two-sided markets
- Avg sell > avg buy in 84% of markets (spread capture)
- High-frequency cadence (median gap 45s)
- Heavy concentration in Over/Under sports totals (sports MM niche)
- Both-sides inventory: 37 markets (0.68%)
- Clip USDC median/p90/max: $10.57 / $52.52 / $1,479.63
- Sport categories: `{'sports_totals': 40877.63, 'sports_match': 14704.2, 'other': 6180.6, 'crypto': 146.94}`
- Slug tokens: [('ucl', 136), ('lal', 122), ('bun', 91), ('ten', 63), ('mma', 29)]

### Maker vs Taker

| Leg | Maker % | Taker % | Maker fills | Taker fills |
|---|---:|---:|---:|---:|
| Entry | 38.38% | 61.62% | 3,899 | 5,178 |
| Exit | 49.09% | 50.91% | 6,935 | 3,966 |

- `enter_taker_exit_maker`: 1723
- `enter_taker_exit_taker`: 1468
- `enter_maker_exit_maker`: 1062
- `enter_maker_exit_taker`: 680

### Price bands

| Band | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| 0-20¢ | 909 | 71.0% | $4,517.97 | $4.97 |
| 20-40¢ | 1285 | 77.2% | $15,230.70 | $11.85 |
| 40-60¢ | 1494 | 82.1% | $22,820.93 | $15.28 |
| 60-80¢ | 1463 | 86.4% | $17,974.32 | $12.29 |
| 80-100¢ | 271 | 78.4% | $1,365.45 | $5.04 |

## C. Equity & risk

- Final cashflow equity: $58,204.98
- Max drawdown: -$601.18 (-1.3% of peak)
- Longest drawdown: 0 days
- Daily Sharpe (ann.): 14.692
- Profit factor: 3.2979
- Top 10 winners: $6,051.67 (6.82% of win PnL)
- Top 10 losers: -$4,429.46 (16.48% of loss PnL)
- Max inventory shares: 6000.0

### Top winners
- $841.93 · 1h12m · FC St. Pauli 1910 vs. FC Bayern München: O/U 3.5
- $670.10 · 28m48s · FC Bayern München vs. Real Madrid CF: O/U 4.5
- $645.59 · 6m02s · FC Bayern München vs. Real Madrid CF: O/U 3.5
- $640.86 · 1h18m · FC St. Pauli 1910 vs. FC Bayern München: O/U 4.5
- $629.26 · 2m18s · Will Club Atlético de Madrid win on 2026-08-23?
- $564.47 · 13m06s · Will Real Madrid CF win on 2026-03-17?
- $544.83 · 1h10m · FC St. Pauli 1910 vs. FC Bayern München: O/U 2.5
- $508.06 · 58s · Paris Saint-Germain vs. Aston Villa: O/U 3.5
- $504.28 · 44s · Will Paris Saint-Germain FC win on 2026-04-14?
- $502.30 · 9m30s · Netherlands vs. Japan: O/U 4.5

### Top losers
- -$384.52 · 23m30s · Cádiz CF vs. Córdoba CF: O/U 4.5
- -$388.13 · 2m16s · Real Madrid CF vs. Deportivo Alavés: O/U 3.5
- -$414.38 · 8m10s · UD Las Palmas vs. SD Huesca: O/U 3.5
- -$416.80 · 1m14s · Sporting CP vs. Arsenal FC: O/U 2.5
- -$427.77 · 8m10s · RC Strasbourg Alsace vs. OGC Nice: O/U 4.5
- -$427.80 · 46s · Will Paris Saint-Germain FC win on 2026-04-22?
- -$471.20 · 1h16m · Paris Saint-Germain FC vs. Liverpool FC: O/U 3.5
- -$474.32 · 3m46s · Panama vs. England: Both Teams to Score
- -$508.72 · 1h27m · Melbourne City FC vs. Western Sydney Wanderers FC: O/U 4.5
- -$515.82 · 6m46s · RC Strasbourg Alsace vs. OGC Nice: O/U 3.5

## D. Trade management

### Hold-time buckets

| Bucket | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| <30s | 717 | 74.9% | $2,351.19 | $3.28 |
| 30s-2m | 3234 | 86.7% | $42,763.37 | $13.22 |
| 2-5m | 731 | 64.5% | $2,609.46 | $3.57 |
| 5-15m | 291 | 59.5% | $442.89 | $1.52 |
| 15m+ | 449 | 75.4% | $13,742.46 | $30.61 |

- After early adverse (>2¢ vs entry within 2m): n=400, avg PnL -$12.86, median first-sell 56s, median hold 1m23s
- After favorable first sell (+2¢): n=4058, avg PnL $18.13, median MFE capture 1.0
- Campaigns (re-entry after flat): 317 (5.85%), avg entries 2.09, PnL $9,675.13, avg $30.52, WR 82.0%
- Single-entry: n=5105, PnL $52,234.23, avg $10.23
- Flatten-before-resolution flag rate: 0.9035; hold-to-resolution style n=489; redeems $2,147.26; merges $0.00
- Avg-down while MTM-red on losers: 15/993 (1.51%); Δ if skipped on those $62.53; global never-red-buy Δ -$58.20

### Family mix

| Family | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| Over/Under | 3543 | 77.9% | $40,676.84 | $11.48 |
| Yes/No moneyline | 1743 | 84.3% | $21,062.80 | $12.08 |
| Other | 136 | 87.2% | $169.73 | $1.25 |

## E. Edge diagnosis

- Time to MFE (winners): median 1m04s, p25 44s, p75 1m39s, p90 6m29s
- Big MFE ≥10¢: n=3256; within 30s=222; within 60s=1624 (49.88% of big moves)

**Edge thesis:** Joins short-horizon informed / impulse flow — taker-heavy entries, exits into strength. Money from markout seconds–minutes after entry, not two-sided spreads.

## F. vs polika72

| Metric | This trader | polika72 |
|---|---:|---:|
| identity | one_sided_informed_scalper | one_sided_informed_scalper |
| trades | 19978 | 19978 |
| cashflow_pnl | 58204.9839 | 58204.9839 |
| win_rate | 0.8008 | 0.8008 |
| entry_taker_pct | 61.62 | 61.62 |
| both_sides_rate | 0.0068 | 0.0068 |
| median_clip | 10.567 | 11.29 |
| campaign_pct | 5.85 | 5.85 |
| max_dd | -601.1817 | -601.1817 |
| time_to_mfe_med | 64 | 64 |

### Steal / avoid

- **Steal:** impulse entry timing / live-event reaction if transferable.
- **Avoid:** copying one-sided Over bias blindly onto Kalshi without feed parity.

## G. Kalshi two-sided informed MM relevance

Partial relevance: the *informed impulse* leg maps to an aggressive/taker overlay on Kalshi, but this is NOT the core two-sided MM. Use as a signal/overlay module, not the whole bot.


## 9. Hour / DOW volume (UTC)

| Hour | USDC volume |
|---:|---:|
| 0 | 21151.84 |
| 1 | 15280.08 |
| 2 | 15855.8 |
| 3 | 7116.4 |
| 4 | 3320.59 |
| 5 | 4869.92 |
| 6 | 3018.7 |
| 7 | 4784.98 |
| 8 | 10517.37 |
| 9 | 6050.59 |
| 10 | 9381.94 |
| 11 | 24334.18 |
| 12 | 20626.22 |
| 13 | 22652.91 |
| 14 | 26222.38 |
| 15 | 17605.04 |
| 16 | 32487.56 |
| 17 | 30636.8 |
| 18 | 35194.42 |
| 19 | 54578.52 |
| 20 | 43399.25 |
| 21 | 14824.47 |
| 22 | 18674.8 |
| 23 | 19594.94 |

| DOW (0=Mon) | USDC volume |
|---:|---:|
| 0 | 29023.74 |
| 1 | 43589.89 |
| 2 | 42309.99 |
| 3 | 49408.07 |
| 4 | 50733.01 |
| 5 | 121883.06 |
| 6 | 125231.94 |

## 10. Bot schema pointer

Parse `MASTER.json` keys: `reconciliation`, `identity`, `performance`, `extras`, `copyability`, `equity_curve_daily`, `deep_dive_highlights`.
