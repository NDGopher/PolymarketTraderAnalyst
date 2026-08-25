# MASTER AUTOPSY — HomeRunHazard

> Single file for humans **and** bots. Machine-readable twin: `MASTER.json` · Equity: `equity_curve.csv`.

- Wallet: `0x5268527977f700f9bf9b6d5cd843859e4e70135d`
- Generated: `2026-08-25T16:46:55.188350+00:00`
- Identity class: **`two_sided_inventory_mm`**

## 0. Executive verdict

This trader is classified as **two_sided_inventory_mm** with primary focus **sports_totals**. Preferred PnL (**closed_positions_sum**) **$2,231,236.73** (leaderboard ALL $2,248,711.81; MATCH). Unique trades **26,170**. Copy difficulty **8/10** · ease **3/10**. Two-sided inventory MM DNA (often buy YES + buy NO then MERGE/REDEEM). Needs quoting/inventory stack; buy-only books exit via merge/redeem instead of sells.

**Exit mechanics:** `merge_and_or_redeem_dominant`
**Kalshi two-sided MM fit:** HIGH — closest to two-sided informed MM DNA
**Preferred PnL note:** For buy-only / merge-redeem traders, cashflow equity can look deeply negative while closed-legs + leaderboard show true realized edge.

## 1. Reconciliation (mandatory)

| Source | PnL | Extra |
|---|---:|---|
| **Preferred (closed_positions_sum)** | **$2,231,236.73** | vs LB diff=-17475.09 |
| Ours cashflow realized | -$2,419,854.53 | trades=26,170 buy_only=True |
| Ours core (ex-rebate) | -$2,438,366.83 | WR legs=54.02% |
| Ours closed-legs sum | $2,231,236.73 | PF=1.0434 |
| Polymarket leaderboard ALL | $2,248,711.81 | vol=$264,797,406.19 rank=67 |
| PolyData | $2,250,300.68 | trades=268747 WR=0.5418 |

- MATCH: `polymarket_leaderboard_ALL` pnl ours=2231236.7279 field=closed_positions_sum ref=2248711.8139243205 diff=-17475.086
- MATCH: `polydata` realized_pnl ours=2231236.7279 field=closed_positions_sum ref=2250300.68 diff=-19063.9521
- DRIFT: `polydata` n_trades ours=26170 field=None ref=268747 diff=-242577
- MATCH: `polydata` win_rate ours=0.5402 field=None ref=0.5418 diff=-0.0016
- DRIFT: `internal` cashflow_vs_closed ours=-2419854.5251 field=None ref=2231236.7279 diff=-4651091.253

## 2. Identity & microstructure

- Both-sides rate: 68.64% (753 markets)
- Clip median/p90/max: $8.17 / $488.54 / $9,369.92
- Category PnL: `{'sports_totals': -194767.89, 'sports_match': -291205.24}`
- Start BUY first: 1097 · SELL first: 0
- Entry maker/taker: 84.91% / 15.09% (24,232/1,938 fills)
- Exit maker/taker: None% / None% (0/0 fills)
- Patterns: `{}`

### Outcome volume (top)

| Outcome | Buy USDC | Sell USDC | Sell−Buy |
|---|---:|---:|---:|
| Over | $334,106.23 | $0.00 | -$334,106.23 |
| Under | $298,613.36 | $0.00 | -$298,613.36 |
| Stefanos Tsitsipas | $141,954.50 | $0.00 | -$141,954.50 |
| Seattle Mariners | $111,674.20 | $0.00 | -$111,674.20 |
| Spurs | $107,098.22 | $0.00 | -$107,098.22 |
| Thunder | $95,513.99 | $0.00 | -$95,513.99 |
| Timberwolves | $94,745.40 | $0.00 | -$94,745.40 |
| Knicks | $87,352.56 | $0.00 | -$87,352.56 |
| Chicago White Sox | $79,529.57 | $0.00 | -$79,529.57 |
| Boston Red Sox | $78,726.44 | $0.00 | -$78,726.44 |
| Pistons | $76,632.79 | $0.00 | -$76,632.79 |
| Tampa Bay Rays | $72,974.79 | $0.00 | -$72,974.79 |

## 3. Performance metrics (kitchen sink)

- Expectancy / market: -$484.04
- Avg win / avg loss: $1,751.36 / -$3,034.01 · ratio=0.5772
- PnL / day: -$187,440.32 · trades/day=2027.11 · markets/day=84.97
- PnL concentration HHI: 0.00794 (higher=more concentrated)
- Notional sum: $5,122,859.13 · median ticket $8.17
- Buy price median: 0.44 · Sell price median: None
- Activity types: `{'DEPOSIT': 7, 'WITHDRAWAL': 1, 'TRADE': 26170, 'MERGE': 428, 'REDEEM': 788, 'REWARD': 7, 'MAKER_REBATE': 9}`
- Open risk: `{'n': 3092, 'cash_pnl': -1176599.53, 'current_value': 199068.09, 'redeemable': 2892}`

### Hold-time engine

| Bucket | N | WR | Total PnL | Avg | Median |
|---|---:|---:|---:|---:|---:|
| <30s | 228 | 66.06% | $20,573.48 | $90.23 | $0.00 |
| 30s-2m | 25 | 68.42% | $2,702.79 | $108.11 | $0.04 |
| 2-5m | 34 | 55.17% | $7,037.48 | $206.98 | $0.00 |
| 5-15m | 53 | 44.00% | $512.34 | $9.67 | -$5.96 |
| 15m+ | 757 | 50.61% | -$516,799.21 | -$682.69 | $0.00 |

### Entry price bands

| Band | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| 0-20¢ | 28 | 4.76% | -$43,431.34 | -$1,551.12 |
| 20-40¢ | 156 | 31.16% | -$125,802.79 | -$806.43 |
| 40-60¢ | 816 | 55.54% | -$424,811.46 | -$520.60 |
| 60-80¢ | 80 | 75.00% | $47,345.47 | $591.82 |
| 80-100¢ | 17 | 93.75% | $60,726.99 | $3,572.18 |

### Family

| Family | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| Other | 679 | 50.70% | -$337,510.06 | -$497.07 |
| Over/Under | 418 | 57.85% | -$148,463.07 | -$355.17 |

## 4. Equity curve (critical)

### 4a. Cashflow activity equity

- Final equity (cashflow): **-$826,491.53**
- Max DD: **-$1,248,741.22** (0.00% of peak)
- Longest DD: **13 days**
- Daily Sharpe (ann.): **-4.624**
- Days: 11

Files: `equity_curve.csv` · `equity_curve.json` (source=`cashflow_activity`)

<details><summary>Daily cashflow equity table (full)</summary>

| Date | Equity | Daily PnL | Drawdown |
|---|---:|---:|---:|
| 2026-04-24 | -93782.13 | -93782.13 | -93782.13 |
| 2026-04-25 | -211115.84 | -117333.71 | -211115.84 |
| 2026-04-26 | -8645.41 | 202470.44 | -8645.41 |
| 2026-04-27 | -60784.30 | -52138.89 | -60784.30 |
| 2026-04-28 | -209846.27 | -149061.97 | -209846.27 |
| 2026-04-29 | -210640.78 | -794.50 | -210640.78 |
| 2026-04-30 | -210531.78 | 109.00 | -210531.78 |
| 2026-05-04 | -317284.53 | -106752.76 | -317284.53 |
| 2026-05-05 | -1248741.22 | -931456.69 | -1248741.22 |
| 2026-05-06 | -856306.26 | 392434.96 | -856306.26 |
| 2026-05-07 | -826491.53 | 29814.74 | -826491.53 |

</details>

### 4b. Closed-positions equity (alt — critical for buy-only books)

- Final closed equity: **$2,231,236.73**
- Max DD: **-$518,390.05**
- Daily Sharpe (ann.): **4.867**
- Days: 120

Files: `equity_curve_closed.csv` · `equity_curve_closed.json` (source=`closed_positions`)

<details><summary>Daily closed equity table (full)</summary>

| Date | Equity | Daily PnL | Drawdown |
|---|---:|---:|---:|
| 2026-04-24 | -13132.79 | -13132.79 | -13132.79 |
| 2026-04-25 | -90236.50 | -77103.71 | -90236.50 |
| 2026-04-26 | -90768.15 | -531.66 | -90768.15 |
| 2026-04-27 | -181123.12 | -90354.97 | -181123.12 |
| 2026-04-28 | -253190.48 | -72067.35 | -253190.48 |
| 2026-04-29 | -240598.82 | 12591.66 | -240598.82 |
| 2026-04-30 | -238029.72 | 2569.10 | -238029.72 |
| 2026-05-05 | -414488.53 | -176458.81 | -414488.53 |
| 2026-05-06 | -404172.09 | 10316.44 | -404172.09 |
| 2026-05-07 | -518390.05 | -114217.96 | -518390.05 |
| 2026-05-08 | -459470.64 | 58919.41 | -459470.64 |
| 2026-05-09 | -412959.14 | 46511.50 | -412959.14 |
| 2026-05-10 | -394105.55 | 18853.59 | -394105.55 |
| 2026-05-11 | -449327.08 | -55221.53 | -449327.08 |
| 2026-05-12 | -449622.37 | -295.29 | -449622.37 |
| 2026-05-13 | -371915.59 | 77706.78 | -371915.59 |
| 2026-05-14 | -222396.11 | 149519.49 | -222396.11 |
| 2026-05-15 | -214882.82 | 7513.29 | -214882.82 |
| 2026-05-16 | -224015.07 | -9132.25 | -224015.07 |
| 2026-05-17 | -211710.81 | 12304.26 | -211710.81 |
| 2026-05-18 | -141898.61 | 69812.21 | -141898.61 |
| 2026-05-19 | -159218.84 | -17320.23 | -159218.84 |
| 2026-05-20 | -131839.64 | 27379.20 | -131839.64 |
| 2026-05-21 | -100905.37 | 30934.27 | -100905.37 |
| 2026-05-22 | 5664.33 | 106569.70 | 0.00 |
| 2026-05-23 | 75094.52 | 69430.19 | 0.00 |
| 2026-05-24 | 120974.27 | 45879.75 | 0.00 |
| 2026-05-25 | 104847.17 | -16127.10 | -16127.10 |
| 2026-05-26 | 149787.50 | 44940.34 | 0.00 |
| 2026-05-27 | 300648.77 | 150861.27 | 0.00 |
| 2026-05-28 | 198112.74 | -102536.03 | -102536.03 |
| 2026-05-29 | 194413.97 | -3698.77 | -106234.80 |
| 2026-05-30 | 250800.98 | 56387.01 | -49847.79 |
| 2026-05-31 | 359084.58 | 108283.60 | 0.00 |
| 2026-06-01 | 492476.08 | 133391.51 | 0.00 |
| 2026-06-02 | 496701.29 | 4225.21 | 0.00 |
| 2026-06-03 | 398710.41 | -97990.89 | -97990.89 |
| 2026-06-04 | 423671.39 | 24960.98 | -73029.91 |
| 2026-06-05 | 517704.84 | 94033.45 | 0.00 |
| 2026-06-06 | 744144.62 | 226439.79 | 0.00 |
| 2026-06-07 | 824213.07 | 80068.44 | 0.00 |
| 2026-06-08 | 818790.61 | -5422.45 | -5422.45 |
| 2026-06-09 | 989305.79 | 170515.17 | 0.00 |
| 2026-06-10 | 964051.80 | -25253.99 | -25253.99 |
| 2026-06-11 | 966219.41 | 2167.61 | -23086.38 |
| 2026-06-12 | 939129.13 | -27090.27 | -50176.66 |
| 2026-06-13 | 966366.40 | 27237.27 | -22939.39 |
| 2026-06-14 | 1019697.59 | 53331.20 | 0.00 |
| 2026-06-15 | 998600.78 | -21096.82 | -21096.82 |
| 2026-06-16 | 988965.62 | -9635.16 | -30731.97 |
| 2026-06-17 | 1051566.06 | 62600.44 | 0.00 |
| 2026-06-18 | 1084628.55 | 33062.50 | 0.00 |
| 2026-06-19 | 1089443.27 | 4814.71 | 0.00 |
| 2026-06-20 | 920679.78 | -168763.49 | -168763.49 |
| 2026-06-21 | 886410.03 | -34269.74 | -203033.23 |
| 2026-06-22 | 912679.23 | 26269.20 | -176764.03 |
| 2026-06-23 | 871596.22 | -41083.01 | -217847.05 |
| 2026-06-24 | 918180.47 | 46584.25 | -171262.80 |
| 2026-06-25 | 937645.22 | 19464.76 | -151798.04 |
| 2026-06-26 | 907103.12 | -30542.10 | -182340.15 |
| 2026-06-27 | 842839.27 | -64263.85 | -246604.00 |
| 2026-06-28 | 947520.34 | 104681.07 | -141922.93 |
| 2026-06-29 | 919641.38 | -27878.96 | -169801.88 |
| 2026-06-30 | 944829.53 | 25188.15 | -144613.73 |
| 2026-07-01 | 916378.70 | -28450.83 | -173064.57 |
| 2026-07-02 | 954313.43 | 37934.73 | -135129.83 |
| 2026-07-03 | 1016871.73 | 62558.30 | -72571.53 |
| 2026-07-04 | 1168202.50 | 151330.76 | 0.00 |
| 2026-07-05 | 1098600.78 | -69601.72 | -69601.72 |
| 2026-07-06 | 1035632.09 | -62968.69 | -132570.40 |
| 2026-07-07 | 1015244.81 | -20387.28 | -152957.68 |
| 2026-07-08 | 1063702.99 | 48458.18 | -104499.50 |
| 2026-07-09 | 1112473.37 | 48770.38 | -55729.13 |
| 2026-07-10 | 1132607.03 | 20133.66 | -35595.47 |
| 2026-07-11 | 1201130.10 | 68523.07 | 0.00 |
| 2026-07-12 | 1253370.85 | 52240.75 | 0.00 |
| 2026-07-13 | 1312614.73 | 59243.88 | 0.00 |
| 2026-07-14 | 1282340.57 | -30274.17 | -30274.17 |
| 2026-07-15 | 1273004.52 | -9336.05 | -39610.22 |
| 2026-07-16 | 1313367.76 | 40363.25 | 0.00 |
| 2026-07-17 | 1282430.90 | -30936.86 | -30936.86 |
| 2026-07-18 | 1408276.13 | 125845.23 | 0.00 |
| 2026-07-19 | 1454193.71 | 45917.58 | 0.00 |
| 2026-07-20 | 1457320.46 | 3126.76 | 0.00 |
| 2026-07-21 | 1396860.76 | -60459.70 | -60459.70 |
| 2026-07-22 | 1399339.19 | 2478.43 | -57981.27 |
| 2026-07-23 | 1485379.78 | 86040.59 | 0.00 |
| 2026-07-24 | 1406530.62 | -78849.16 | -78849.16 |
| 2026-07-25 | 1342646.45 | -63884.17 | -142733.32 |
| 2026-07-26 | 1493178.13 | 150531.67 | 0.00 |
| 2026-07-27 | 1510377.50 | 17199.37 | 0.00 |
| 2026-07-28 | 1410259.17 | -100118.33 | -100118.33 |
| 2026-07-29 | 1453728.56 | 43469.39 | -56648.94 |
| 2026-07-30 | 1458430.90 | 4702.34 | -51946.60 |
| 2026-07-31 | 1572161.86 | 113730.96 | 0.00 |
| 2026-08-01 | 1607025.30 | 34863.43 | 0.00 |
| 2026-08-02 | 1688627.83 | 81602.53 | 0.00 |
| 2026-08-03 | 1660976.00 | -27651.83 | -27651.83 |
| 2026-08-04 | 1680785.64 | 19809.64 | -7842.19 |
| 2026-08-05 | 1885819.48 | 205033.84 | 0.00 |
| 2026-08-06 | 1907921.46 | 22101.98 | 0.00 |
| 2026-08-07 | 2031260.28 | 123338.82 | 0.00 |
| 2026-08-08 | 2017702.98 | -13557.29 | -13557.29 |
| 2026-08-09 | 1953140.66 | -64562.32 | -78119.62 |
| 2026-08-10 | 1996184.80 | 43044.14 | -35075.48 |
| 2026-08-11 | 1998724.87 | 2540.07 | -32535.40 |
| 2026-08-12 | 2009492.88 | 10768.01 | -21767.40 |
| 2026-08-13 | 2043411.76 | 33918.88 | 0.00 |
| 2026-08-14 | 1942541.57 | -100870.19 | -100870.19 |
| 2026-08-15 | 1882649.30 | -59892.27 | -160762.46 |
| 2026-08-16 | 2014067.99 | 131418.69 | -29343.77 |
| 2026-08-17 | 2006521.32 | -7546.67 | -36890.43 |
| 2026-08-18 | 2119664.04 | 113142.72 | 0.00 |
| 2026-08-19 | 2236958.85 | 117294.81 | 0.00 |
| 2026-08-20 | 2161202.73 | -75756.12 | -75756.12 |
| 2026-08-21 | 2057206.69 | -103996.04 | -179752.16 |
| 2026-08-22 | 2124841.15 | 67634.46 | -112117.70 |
| 2026-08-23 | 2256456.26 | 131615.11 | 0.00 |
| 2026-08-24 | 2270729.98 | 14273.71 | 0.00 |
| 2026-08-25 | 2231236.73 | -39493.25 | -39493.25 |

</details>

### Top winners / losers contribution

Top10 winners $202,627.39 (21.63% of wins) · Top10 losers -$483,957.70 (34.01% of losses) · PF=1.0434

- WIN $30,407.98 · 6606s · Madrid Open: Anastasia Potapova vs Elena Rybakina
- WIN $27,567.49 · 4104s · Madrid Open: Alexander Bublik vs Stefanos Tsitsipas
- WIN $24,774.18 · 5774s · Madrid Open: Thiago Agustin Tirante vs Tommy Paul
- WIN $21,400.73 · 5776s · 76ers vs. Knicks
- WIN $18,618.95 · 3708s · Madrid Open: Jessica Pegula vs Marta Kostyuk
- WIN $18,085.18 · 38976s · Athletics vs. Philadelphia Phillies: O/U 8.5
- WIN $17,054.02 · 7762s · Milwaukee Brewers vs. St. Louis Cardinals: O/U 8.5
- WIN $16,281.38 · 157s · Cincinnati Reds vs. Chicago Cubs: O/U 8.5
- WIN $15,666.68 · 19274s · Athletics vs. Philadelphia Phillies: O/U 9.5
- WIN $12,770.80 · 5496s · Toronto Blue Jays vs. Tampa Bay Rays

- LOSS -$16,346.11 · 8990s · Colorado Rockies vs. New York Mets
- LOSS -$19,436.44 · 5560s · Madrid Open: Terence Atmane vs Alexander Zverev
- LOSS -$21,487.41 · 6776s · Madrid Open: Daniil Medvedev vs Fabian Marozsan
- LOSS -$23,006.33 · 5317s · Internazionali BNL d'Italia: Federico Cina vs Alexander Blockx
- LOSS -$54,557.39 · 7736s · Madrid Open: Aryna Sabalenka vs Naomi Osaka
- LOSS -$57,746.38 · 5373s · New York Mets vs. Colorado Rockies: O/U 10.5
- LOSS -$59,416.63 · 6470s · 76ers vs. Knicks: O/U 212.5
- LOSS -$69,098.34 · 5220s · Madrid Open: Stefanos Tsitsipas vs Casper Ruud
- LOSS -$70,897.12 · 7404s · Baltimore Orioles vs. New York Yankees
- LOSS -$91,965.56 · 5950s · 76ers vs. Knicks: O/U 211.5

## 5. Trade management deep dive

- Adverse early (>2¢): `{'n_early_adverse': 0, 'avg_pnl': None, 'median_t_first_sell': None, 'median_hold': None}`
- Favorable first-sell: `{'n_first_sell_up_2c': 0, 'avg_pnl': None, 'median_mfe_capture': None, 'mean_mfe_capture': None}`
- Campaigns: `{'n': 0, 'pct': 0.0, 'avg_entries': None, 'pnl': 0, 'avg_pnl': None, 'win_rate': None, 'single_n': 1097, 'single_pnl': -485973.13, 'single_avg_pnl': -443.0}`
- Avg-down: `{'n_losers': 469, 'n_losers_with_red_buys': 345, 'pct_losers': 73.56, 'total_delta_if_skipped_on_losers': 0.0, 'global_fifo_sim': 0.0, 'global_fifo_never_red_buy': 0.0, 'global_delta': 0.0}`
- Resolution behavior: `{'flattened_before_flag_rate': 0.6773, 'hold_to_resolution_style_n': 1097, 'redeems_usdc': 2693132.0005570017, 'merges_usdc': 1593363.0}`
- Latency: `{'time_to_mfe_median': None, 'time_to_mfe_p25': None, 'time_to_mfe_p75': None, 'time_to_mfe_p90': None, 'mfe_ge_10c_n': 0, 'mfe_ge_10c_within_30s': 0, 'mfe_ge_10c_within_60s': 0, 'pct_big_within_60s': 0.0}`

### What works / fails
- WORKS: Both-sides inventory on 69.5% of winning markets (losers 81.2%)
- WORKS: Hold bucket <5m: avg PnL $105.62 on 287 markets (WR 48%)
- WORKS: Hold bucket 5-30m: avg PnL $65.56 on 125 markets (WR 49%)
- WORKS: Entry band 0.60-0.80: avg $591.82 across 80 markets
- WORKS: Buy-ladder behavior: fade-into-weakness markets=331, chase-up markets=319
- FAILS: Hold bucket 30m-2h: avg PnL $-541.45 on 454 markets
- FAILS: Hold bucket 2-12h: avg PnL $-1250.34 on 192 markets
- FAILS: Hold bucket 12h+: avg PnL $-989.63 on 39 markets
- FAILS: Entry band 0.20-0.40: avg $-806.43 across 156 markets — avoid or tighten risk
- FAILS: Entry band 0.40-0.60: avg $-520.60 across 816 markets — avoid or tighten risk

## 6. Strategy overview (in depth)

# Strategy Dossier: HomeRunHazard

- **Wallet:** `0x5268527977f700f9bf9b6d5cd843859e4e70135d`
- **History span:** 2026-04-24T14:39:18+00:00 → 2026-05-07T12:35:18+00:00 (12.91 days)
- **Trades:** 26,170 (buys 26,170 / sells 0)
- **Markets touched:** 1,097
- **Closed positions:** 42,624

## Headline performance

| Metric | Value |
|---|---|
| Realized cashflow (sells − buys + redeems + rebates) | -$2,419,854.53 |
| Core cashflow (ex-rebates) | -$2,438,366.83 |
| Closed-positions realized sum | $2,231,236.73 |
| Win rate (closed) | 54.02% (23021W / 19597L) |
| Profit factor | 1.0434 |
| Gross wins / losses | $53,634,448.68 / -$51,403,211.95 |
| Equity max drawdown | -$1,510,984.52 |
| Polymarket leaderboard (ALL) | $2,248,711.81 PnL · vol $264,797,406.19 · rank 67 |

## Source validation

- **MATCH** `polymarket_leaderboard_ALL` pnl: ours=2231236.7279 ref=2248711.8139243205 diff=-17475.086
- **MATCH** `polydata` realized_pnl: ours=2231236.7279 ref=2250300.68 diff=-19063.9521
- **DRIFT** `polydata` n_trades: ours=26170 ref=268747 diff=-242577
- **MATCH** `polydata` win_rate: ours=0.5402 ref=0.5418 diff=-0.0016
- **DRIFT** `internal` cashflow_vs_closed: ours=-2419854.5251 ref=2231236.7279 diff=-4651091.253

## What kind of trader is this?

**Classification:** `likely_market_maker` (score 45/100)

- Trades both outcomes in 69% of markets (inventory/MM signature)
- High-frequency cadence (median gap 10s)
- Heavy concentration in Over/Under sports totals (sports MM niche)

Supporting rates — both-sides markets: 0.6864, fast round-trips: 0.0, spread-capture rate: 0.0.

## Exact edge thesis

HomeRunHazard primarily monetizes **liquidity / short-horizon mean reversion on sports markets**, not long-shot directional political bets. The tape shows repeated buy-then-sell with average exit price above average entry — the classic scalper / spread fingerprint.

See `bot_playbook.md` for the full entry/management/exit autopsy and bot architecture.

## Where the money comes from

- **sports_totals**: $1,509,899.51 across 18437 closed legs
- **sports_match**: $721,337.22 across 24187 closed legs

## Timing

- Peak UTC hours: 0, 23, 10, 11, 14
- Peak weekdays (0=Mon): [1, 2, 5]
- Median inter-trade gap: 10s

## Sizing

- Median ticket $8.17, mean $195.75, p90 $488.54, max $9,369.92
- Share size median 20.0, mean 401.4378

## Trade-by-trade pattern (representative winners)

These vignettes are reconstructed from fills: average entry, average exit, hold time, and closed realized PnL.

## Top closed winners / losers

**Winners**
- Madrid Open: Anastasia Potapova vs Elena Rybakina: $30,407.98 · bought $14,458.18 · sold $0.00 · hold 1h 50m
- Madrid Open: Alexander Bublik vs Stefanos Tsitsipas: $27,567.49 · bought $60,871.51 · sold $0.00 · hold 1h 8m
- Madrid Open: Thiago Agustin Tirante vs Tommy Paul: $24,774.18 · bought $65,721.63 · sold $0.00 · hold 1h 36m
- 76ers vs. Knicks: $21,400.73 · bought $13,351.34 · sold $0.00 · hold 1h 36m
- Madrid Open: Jessica Pegula vs Marta Kostyuk: $18,618.95 · bought $41,704.14 · sold $0.00 · hold 1h 1m
- Athletics vs. Philadelphia Phillies: O/U 8.5: $18,085.18 · bought $25,587.97 · sold $0.00 · hold 10h 49m
- Milwaukee Brewers vs. St. Louis Cardinals: O/U 8.5: $17,054.02 · bought $20,720.59 · sold $0.00 · hold 2h 9m
- Cincinnati Reds vs. Chicago Cubs: O/U 8.5: $16,281.38 · bought $1,424.67 · sold $0.00 · hold 2m 37s
- Athletics vs. Philadelphia Phillies: O/U 9.5: $15,666.68 · bought $16,713.55 · sold $0.00 · hold 5h 21m
- Toronto Blue Jays vs. Tampa Bay Rays: $12,770.80 · bought $5,049.06 · sold $0.00 · hold 1h 31m

**Losers**
- 76ers vs. Knicks: O/U 211.5: -$91,965.56 · bought $5,515.34 · sold $0.00
- Baltimore Orioles vs. New York Yankees: -$70,897.12 · bought $14,563.59 · sold $0.00
- Madrid Open: Stefanos Tsitsipas vs Casper Ruud: -$69,098.34 · bought $82,297.10 · sold $0.00
- 76ers vs. Knicks: O/U 212.5: -$59,416.63 · bought $6,154.03 · sold $0.00
- New York Mets vs. Colorado Rockies: O/U 10.5: -$57,746.38 · bought $8,714.96 · sold $0.00
- Madrid Open: Aryna Sabalenka vs Naomi Osaka: -$54,557.39 · bought $65,700.58 · sold $0.00
- Internazionali BNL d'Italia: Federico Cina vs Alexander Blockx: -$23,006.33 · bought $27,251.33 · sold $0.00
- Madrid Open: Daniil Medvedev vs Fabian Marozsan: -$21,487.41 · bought $10,570.16 · sold $0.00
- Madrid Open: Terence Atmane vs Alexander Zverev: -$19,436.44 · bought $14,107.74 · sold $0.00
- Colorado Rockies vs. New York Mets: -$16,346.11 · bought $25,739.19 · sold $0.00

## Replication playbook (how to copy the edge)

1. **Universe:** Focus on liquid sports match + totals (O/U) markets with tight books.
2. **Role:** Quote or take both sides near mid; prioritize markets you can exit before resolution.
3. **Sizing:** Start near their median ticket (~$8.17) and scale only with inventory limits.
4. **Inventory:** Cap net Yes/No (or Over/Under) imbalance; flatten when mid moves through you.
5. **Hold time:** Target minutes–hours, not overnight directional risk, unless hedged via opposite outcome.
6. **Edge source:** Capture spread + mean reversion after flow, not oracle forecasting alpha.
7. **Ops:** Automate via CLOB maker orders; track maker rebates; kill-switch on drawdown.
8. **Do not blindly copy:** Their edge depends on latency, fee tier, and bankroll. Replicate *mechanics*, not wallet follows.

## Cashflow anatomy

- Buys: $5,131,498.83
- Sells: $0.00
- Redeems: $2,693,132.00
- Maker rebates: $8,822.87
- Taker rebates: $0.00

_Generated 2026-08-25T16:46:54.879231+00:00_


## 7. Bot / copy playbook

- Difficulty: **8/10** · Ease: **3/10**
- Why: Two-sided inventory MM DNA (often buy YES + buy NO then MERGE/REDEEM). Needs quoting/inventory stack; buy-only books exit via merge/redeem instead of sells.

### Build steps
1. Two-sided quoter (or dual one-sided bids) with inventory caps on each outcome
2. Skew toward informed mid / live event state
3. Maker-first entries; taker only to flatten or complete a pair
4. If buy-only: implement MERGE when holding complementary shares + REDEEM at resolution
5. Per-market and portfolio risk limits; kill runaway inventory
6. Match their median gap cadence and clip distribution before adding size

### Steal
- Both-sides inventory discipline
- Maker-led entry style (better for quoting bots)
- Prioritize hold bucket <30s (their PnL engine)

### Avoid
- Averaging down while red on losers
- Their raw size/drawdown — scale down hard
- Fat left-tail single-market blowups — enforce per-market caps

Bot parameters: `{'preferred_entry_price_median': 0.5036, 'preferred_entry_price_p25_p75': (0.4568, 0.56), 'target_spread_median': None, 'target_spread_p75': None, 'max_hold_seconds_p75': 6578, 'median_hold_seconds': 3490, 'clip_size_usdc_median': 6.7871, 'clip_size_usdc_p90': 478.2857, 'both_sides_on_winners_rate': 0.6953, 'require_exit_above_entry': True, 'flatten_before_resolution': True, 'maker_bias': True}`

# Elite Replication Playbook — HomeRunHazard

Wallet `0x5268527977f700f9bf9b6d5cd843859e4e70135d`. Reverse-engineered from the **full unique fill tape** (26,170 trades · 1,097 markets). This is an implementation spec for a high-end bot, not vibes.

## 0. True strategy identity (read this first)

Classification `likely_market_maker` — mix of spread capture and directional inventory.

Heuristic label from the scanner may still say `likely_market_maker` because of fast round-trips + sell>buy + maker rebates. **Operationally, build a live scalper with optional maker quoting**, not a Yes/No pair inventory bot.

## 1. Performance anchors

| Source / metric | Value |
|---|---|
| Cashflow realized (sells−buys+redeems+rebates) | -$2,419,854.53 |
| Core cashflow (ex-rebates) | -$2,438,366.83 |
| Closed-position legs sum | $2,231,236.73 |
| Leg win rate / profit factor | 54.02% / 1.0434 |
| Polymarket leaderboard ALL | $2,248,711.81 · vol $264,797,406.19 · rank 67 |
| polymarket_leaderboard_ALL pnl | ref=2248711.8139243205 ours=2231236.7279 (MATCH) |
| polydata realized_pnl | ref=2250300.68 ours=2231236.7279 (MATCH) |
| polydata n_trades | ref=268747 ours=26170 (DRIFT) |
| polydata win_rate | ref=0.5418 ours=0.5402 (MATCH) |

Notes: Polymarket leaderboard ALL is the primary official PnL check (we match within tolerance). PolyData uses a different event aggregation / trade counting method — expect DRIFT on WR and trade count; use it as a secondary research signal, not the ground truth for fills.

## 2. Universe — where the money is

- **O/U / totals:** 418 markets · -$148,463.07 · avg -$355.17 · median hold 21m30s · median spread None
- **Match / other sports:** 457 markets · -$292,927.53 · avg -$640.98
- **Outcome PnL leaders:**
  - **Tampa Bay Rays**: $53,832.70
  - **Anastasia Potapova**: $44,318.10
  - **Boston Red Sox**: $43,966.59
  - **Spurs**: $43,048.95
  - **Kansas City Royals**: $31,223.74
  - **San Diego Padres**: $29,031.74

### Bot universe rules

1. Only liquid live sports (soccer/football first — their tape is soccer-heavy).
2. Prefer O/U lines with tight books and active in-game trading.
3. Default bias toward **Over** unless your signal says otherwise (their Over PnL dominates).
4. Skip politics/crypto until you have separate evidence.
5. Require enough depth to enter ~median clip and exit within 1–2 minutes.

## 3. ENTRY — exact mechanics

### Style histogram
- `two_sided_inventory_near_mid`: 288
- `two_sided_inventory_sub_mid`: 208
- `two_sided_inventory_above_mid`: 140
- `directional_buy_near_mid`: 132
- `directional_buy_sub_mid`: 127
- `two_sided_inventory_cheap_tail`: 78
- `directional_buy_above_mid`: 70
- `two_sided_inventory_expensive_favorite`: 39
- `directional_buy_cheap_tail`: 8
- `directional_buy_expensive_favorite`: 7

### First-two-fill sequences
- `BUY->BUY`: 917
- `single_fill`: 180

### Entry price → realized edge

| Avg buy band | Markets | Total PnL | Avg PnL |
|---|---:|---:|---:|
| 0.00-0.20 | 28 | -$43,431.34 | -$1,551.12 |
| 0.20-0.40 | 156 | -$125,802.79 | -$806.43 |
| 0.40-0.60 | 816 | -$424,811.46 | -$520.60 |
| 0.60-0.80 | 80 | $47,345.47 | $591.82 |
| 0.80-1.00 | 17 | $60,726.99 | $3,572.18 |

**Best band:** 0.40–0.60 (near mid) — highest average PnL. Tails (≤0.20 or ≥0.80) make less per market.

### Entry checklist (bot)

1. Clip **$6.79** median (p90 $478.29).
2. Aim entry price ~**0.5036** (IQR (0.4568, 0.56)).
3. Trigger = microstructure, not long-term forecast:
   - mid dips / liquidity hole you can buy
   - imminent volatility (attack, corner, shot) where Over can jump
   - resting bid gets lifted? you’re being taken — manage immediately
4. Prefer **maker bids**; take only if the expected jump already started and ask is still inside your edge.
5. Same-second multi-fills are normal (one order, many counterparties) — treat as one decision, many fills.

## 4. MANAGEMENT — what they do after entry

### Styles
- `intraday_swing`: 494
- `single_clip`: 287
- `multi_hour_position`: 227
- `scalp_sub_15m`: 89

### Winners vs losers

| Metric | Winners | Losers |
|---|---:|---:|
| N | 535 | 469 |
| PnL | $936,976.27 | -$1,422,949.40 |
| Median hold | 58m10s | 1h11m |
| Median spread | None | None |
| Scale-in rate | 0.8486 | 0.9019 |
| Scale-out rate | 0.0 | 0.0 |
| Avg fills/market | 23.25 | 28.46 |
| Both-sides rate | 0.6953 | 0.8124 |

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

- **Winners** sell above buy (median spread **None**). **Losers** often exit worse (median spread **None**).
- Losers scale-in **more** (0.9019 vs 0.8486) — averaging down is how they bleed; the bot should **forbid** revenge scale-ins without a fresh signal.
- Hold edge peaks in **<5m** ({'n': 287, 'pnl': 30313.7429, 'avg': 105.6228, 'win_rate': 0.4808}) and a strong **30m–2h** bucket for the larger in-game campaigns.

## 5. EXIT — rules that print

- `hold_to_resolution_or_redeem`: 1097

| Hold bucket | N | Total PnL | Avg | Win rate |
|---|---:|---:|---:|---:|
| <5m | 287 | $30,313.74 | $105.62 | 48.1% |
| 5-30m | 125 | $8,194.71 | $65.56 | 48.8% |
| 30m-2h | 454 | -$245,820.18 | -$541.45 | 49.1% |
| 2-12h | 192 | -$240,065.75 | -$1,250.34 | 48.4% |
| 12h+ | 39 | -$38,595.65 | -$989.63 | 51.3% |

### Exit engine params

1. **TP / ask distance:** target ≈ **None** above avg entry (p75 stretch None). On live O/U this is often a burst move, not slow grind.
2. **Time stop:** median hold 58m10s; p75 1h49m for the scalps — escalate urgency after that.
3. **Scale-out:** peel into strength (their winners stack sells). Don’t wait for one perfect print.
4. **Stop:** if mid < entry − ~3–5¢ on unhedged inventory with no signal → take the loss (copy losers’ speed, not their hope).
5. **Flatten before resolution** — redeem is residual.
6. Taker exits are fine when the move already happened and maker asks won’t fill.

## 6. What works / what fails

### Works
- Both-sides inventory on 69.5% of winning markets (losers 81.2%)
- Hold bucket <5m: avg PnL $105.62 on 287 markets (WR 48%)
- Hold bucket 5-30m: avg PnL $65.56 on 125 markets (WR 49%)
- Entry band 0.60-0.80: avg $591.82 across 80 markets
- Buy-ladder behavior: fade-into-weakness markets=331, chase-up markets=319

### Fails
- Hold bucket 30m-2h: avg PnL $-541.45 on 454 markets
- Hold bucket 2-12h: avg PnL $-1250.34 on 192 markets
- Hold bucket 12h+: avg PnL $-989.63 on 39 markets
- Entry band 0.20-0.40: avg $-806.43 across 156 markets — avoid or tighten risk
- Entry band 0.40-0.60: avg $-520.60 across 816 markets — avoid or tighten risk
- Chase vs fade ladders: `{'chase_up': 319, 'fade_down': 331}`

## 7. Fill-by-fill autopsies (copy these patterns)

## 8. Failure modes (do not bot these)

1. **76ers vs. Knicks: O/U 211.5** -$91,965.56 · hold 1h39m · entry 0.4604 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
2. **Baltimore Orioles vs. New York Yankees** -$70,897.12 · hold 2h03m · entry 0.5628 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
3. **Madrid Open: Stefanos Tsitsipas vs Casper Ruud** -$69,098.34 · hold 1h27m · entry 0.6135 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
4. **76ers vs. Knicks: O/U 212.5** -$59,416.63 · hold 1h47m · entry 0.4885 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
5. **New York Mets vs. Colorado Rockies: O/U 10.5** -$57,746.38 · hold 1h29m · entry 0.521 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
6. **Madrid Open: Aryna Sabalenka vs Naomi Osaka** -$54,557.39 · hold 2h08m · entry 0.3632 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
7. **Internazionali BNL d'Italia: Federico Cina vs Alexander Blockx** -$23,006.33 · hold 1h28m · entry 0.4214 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
8. **Madrid Open: Daniil Medvedev vs Fabian Marozsan** -$21,487.41 · hold 1h52m · entry 0.2168 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
9. **Madrid Open: Terence Atmane vs Alexander Zverev** -$19,436.44 · hold 1h32m · entry 0.2613 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
10. **Colorado Rockies vs. New York Mets** -$16,346.11 · hold 2h29m · entry 0.5674 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`

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
   - default post-only bids/asks; clip $6.79
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
template: HomeRunHazard
mode: one_sided_live_scalper  # not classic two-sided MM
preferred_outcome_bias: Over
clip_usdc_median: 6.7871
clip_usdc_p90: 478.2857
entry_price_median: 0.5036
entry_price_iqr: (0.4568, 0.56)
target_spread: None
target_spread_p75: None
median_hold_seconds: 3490
max_hold_seconds_p75: 6578
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

_Generated 2026-08-25T16:46:54.880319+00:00_


## 8. Structured autopsy (A–G)

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


## 9. Hour / DOW volume (UTC)

| Hour | USDC volume |
|---:|---:|
| 0 | 430380.45 |
| 1 | 345072.54 |
| 2 | 248138.13 |
| 3 | 188652.57 |
| 4 | 120244.14 |
| 5 | 49790.33 |
| 6 | 16225.6 |
| 7 | 27124.9 |
| 8 | 32399.36 |
| 9 | 149664.75 |
| 10 | 174033.52 |
| 11 | 229396.81 |
| 12 | 218727.61 |
| 13 | 149876.8 |
| 14 | 245907.42 |
| 15 | 211898.23 |
| 16 | 246582.64 |
| 17 | 258330.19 |
| 18 | 340933.15 |
| 19 | 214038.85 |
| 20 | 378034.23 |
| 21 | 165433.76 |
| 22 | 277662.54 |
| 23 | 404310.62 |

| DOW (0=Mon) | USDC volume |
|---:|---:|
| 0 | 488789.34 |
| 1 | 1501414.06 |
| 2 | 959878.15 |
| 3 | 381831.48 |
| 4 | 272539.07 |
| 5 | 864726.83 |
| 6 | 653680.21 |

## 10. Bot schema pointer

Parse `MASTER.json` keys: `reconciliation`, `identity`, `performance`, `extras`, `copyability`, `equity_curve_daily`, `deep_dive_highlights`.
