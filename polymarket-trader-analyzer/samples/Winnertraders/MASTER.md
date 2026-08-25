# MASTER AUTOPSY — Winnertraders

> Single file for humans **and** bots. Machine-readable twin: `MASTER.json` · Equity: `equity_curve.csv`.

- Wallet: `0x13464aabec792c36b062316f474713e681330448`
- Generated: `2026-08-25T16:47:01.382465+00:00`
- Identity class: **`hybrid_liquidity_scalper`**

## 0. Executive verdict

This trader is classified as **hybrid_liquidity_scalper** with primary focus **sports_totals**. Preferred PnL (**cashflow_realized**) **$16,661.90** (leaderboard ALL $17,578.63; MATCH). Unique trades **20,475**. Copy difficulty **6/10** · ease **5/10**. Maker-led entries reduce latency race; still needs solid risk + universe selection.

**Exit mechanics:** `sell_secondary_market`
**Kalshi two-sided MM fit:** MEDIUM-HIGH — maker entries transfer well; add explicit both-sides module
**Preferred PnL note:** Cashflow usually tracks leaderboard for buy+sell scalpers.

## 1. Reconciliation (mandatory)

| Source | PnL | Extra |
|---|---:|---|
| **Preferred (cashflow_realized)** | **$16,661.90** | vs LB diff=-916.73 |
| Ours cashflow realized | $16,661.90 | trades=20,475 buy_only=False |
| Ours core (ex-rebate) | $16,180.10 | WR legs=65.11% |
| Ours closed-legs sum | -$844.29 | PF=0.9845 |
| Polymarket leaderboard ALL | $17,578.63 | vol=$2,032,708.12 rank=9026 |
| PolyData | $17,655.63 | trades=16162 WR=0.5926 |

- MATCH: `polymarket_leaderboard_ALL` pnl ours=16661.9043 field=cashflow_realized ref=17578.63184561259 diff=-916.7275
- MATCH: `polydata` realized_pnl ours=16661.9043 field=cashflow_realized ref=17655.63 diff=-993.7257
- DRIFT: `polydata` n_trades ours=20475 field=None ref=16162 diff=4313
- DRIFT: `polydata` win_rate ours=0.6511 field=None ref=0.5926 diff=0.0585
- DRIFT: `internal` cashflow_vs_closed ours=16661.9043 field=None ref=-844.295 diff=17506.1993

## 2. Identity & microstructure

- Both-sides rate: 9.24% (254 markets)
- Clip median/p90/max: $6.80 / $62.50 / $2,575.00
- Category PnL: `{'sports_totals': 9253.28, 'other': 994.88, 'crypto': -294.95, 'sports_match': -10797.51}`
- Start BUY first: 2750 · SELL first: 0
- Entry maker/taker: 62.15% / 37.85% (8,836/3,073 fills)
- Exit maker/taker: 69.16% / 30.84% (6,640/1,926 fills)
- Patterns: `{'enter_taker_exit_maker': 649, 'enter_maker_exit_maker': 1011, 'enter_maker_exit_taker': 513, 'enter_taker_exit_taker': 296}`

### Outcome volume (top)

| Outcome | Buy USDC | Sell USDC | Sell−Buy |
|---|---:|---:|---:|
| Under | $80,793.20 | $86,642.06 | $5,848.86 |
| Yes | $20,858.24 | $20,972.63 | $114.39 |
| No | $11,801.20 | $12,053.81 | $252.60 |
| Over | $5,242.27 | $9,132.89 | $3,890.62 |
| South Africa | $4,188.51 | $3,945.12 | -$243.39 |
| Sri Lanka | $4,056.52 | $4,019.83 | -$36.69 |
| New Zealand | $3,480.31 | $3,772.38 | $292.06 |
| India | $3,490.85 | $3,590.62 | $99.77 |
| Pakistan | $2,915.22 | $3,172.15 | $256.93 |
| West Indies | $2,673.02 | $2,648.07 | -$24.95 |
| Australia | $3,017.39 | $2,242.35 | -$775.03 |
| England | $2,226.06 | $2,500.45 | $274.39 |

## 3. Performance metrics (kitchen sink)

- Expectancy / market: -$0.31
- Avg win / avg loss: $28.18 / -$53.28 · ratio=0.5289
- PnL / day: $76.14 · trades/day=93.56 · markets/day=12.57
- PnL concentration HHI: 0.004035 (higher=more concentrated)
- Notional sum: $464,215.26 · median ticket $6.80
- Buy price median: 0.32 · Sell price median: 0.46
- Activity types: `{'DEPOSIT': 26, 'TRADE': 20475, 'WITHDRAWAL': 133, 'REDEEM': 532, 'REWARD': 6, 'MAKER_REBATE': 106, 'YIELD': 2, 'TAKER_REBATE': 9}`
- Open risk: `{'n': 0, 'cash_pnl': 0, 'current_value': 0, 'redeemable': 0}`

### Hold-time engine

| Bucket | N | WR | Total PnL | Avg | Median |
|---|---:|---:|---:|---:|---:|
| <30s | 139 | 7.97% | -$2,304.51 | -$16.58 | -$6.30 |
| 30s-2m | 130 | 65.38% | $1,668.70 | $12.84 | $1.98 |
| 2-5m | 229 | 69.74% | $1,352.47 | $5.91 | $2.58 |
| 5-15m | 574 | 74.56% | $2,338.79 | $4.07 | $4.49 |
| 15m+ | 1678 | 65.79% | -$3,899.76 | -$2.32 | $4.50 |

### Entry price bands

| Band | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| 0-20¢ | 748 | 51.34% | -$2,672.31 | -$3.57 |
| 20-40¢ | 671 | 58.27% | -$2,758.27 | -$4.11 |
| 40-60¢ | 639 | 70.33% | $1,638.26 | $2.56 |
| 60-80¢ | 465 | 78.23% | $117.08 | $0.25 |
| 80-100¢ | 227 | 88.11% | $2,830.94 | $12.47 |

### Family

| Family | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| Over/Under | 1379 | 68.72% | $9,359.87 | $6.79 |
| Other | 835 | 62.94% | -$10,758.69 | -$12.88 |
| Yes/No moneyline | 536 | 58.77% | $554.53 | $1.03 |

## 4. Equity curve (critical)

### 4a. Cashflow activity equity

- Final equity (cashflow): **$16,661.90**
- Max DD: **-$1,436.31** (-321.48% of peak)
- Longest DD: **15 days**
- Daily Sharpe (ann.): **4.732**
- Days: 216

Files: `equity_curve.csv` · `equity_curve.json` (source=`cashflow_activity`)

<details><summary>Daily cashflow equity table (full)</summary>

| Date | Equity | Daily PnL | Drawdown |
|---|---:|---:|---:|
| 2026-01-16 | -121.92 | -121.92 | -121.92 |
| 2026-01-17 | 93.56 | 215.48 | 0.00 |
| 2026-01-18 | 141.54 | 47.98 | 0.00 |
| 2026-01-19 | 159.22 | 17.68 | 0.00 |
| 2026-01-20 | -116.08 | -275.31 | -275.31 |
| 2026-01-21 | -102.23 | 13.86 | -261.45 |
| 2026-01-22 | -78.60 | 23.63 | -237.82 |
| 2026-01-23 | -27.15 | 51.45 | -186.37 |
| 2026-01-24 | -106.34 | -79.19 | -265.56 |
| 2026-01-25 | 73.17 | 179.51 | -86.05 |
| 2026-01-26 | -292.77 | -365.94 | -451.99 |
| 2026-01-27 | -266.45 | 26.32 | -425.67 |
| 2026-01-28 | -272.94 | -6.49 | -432.17 |
| 2026-01-29 | -347.74 | -74.80 | -506.97 |
| 2026-01-30 | -311.44 | 36.30 | -470.66 |
| 2026-01-31 | -332.10 | -20.66 | -491.33 |
| 2026-02-01 | -352.64 | -20.54 | -511.87 |
| 2026-02-02 | -115.60 | 237.04 | -274.82 |
| 2026-02-03 | 0.94 | 116.54 | -158.28 |
| 2026-02-04 | 210.37 | 209.43 | 0.00 |
| 2026-02-05 | 368.14 | 157.77 | 0.00 |
| 2026-02-06 | 58.65 | -309.49 | -309.49 |
| 2026-02-07 | 285.97 | 227.33 | -82.16 |
| 2026-02-08 | 693.42 | 407.44 | 0.00 |
| 2026-02-09 | 445.18 | -248.24 | -248.24 |
| 2026-02-10 | 1122.41 | 677.23 | 0.00 |
| 2026-02-11 | 1773.51 | 651.09 | 0.00 |
| 2026-02-12 | 4546.46 | 2772.95 | 0.00 |
| 2026-02-13 | 4275.61 | -270.85 | -270.85 |
| 2026-02-14 | 4741.93 | 466.31 | 0.00 |
| 2026-02-15 | 5236.66 | 494.73 | 0.00 |
| 2026-02-16 | 4834.99 | -401.67 | -401.67 |
| 2026-02-17 | 5227.52 | 392.53 | -9.14 |
| 2026-02-18 | 5034.06 | -193.47 | -202.60 |
| 2026-02-19 | 4143.62 | -890.44 | -1093.05 |
| 2026-02-20 | 3800.35 | -343.27 | -1436.31 |
| 2026-02-21 | 4789.01 | 988.66 | -447.65 |
| 2026-02-22 | 4731.11 | -57.90 | -505.55 |
| 2026-02-23 | 5029.00 | 297.89 | -207.67 |
| 2026-02-24 | 4960.61 | -68.39 | -276.05 |
| 2026-02-25 | 4843.00 | -117.60 | -393.66 |
| 2026-02-26 | 4777.98 | -65.02 | -458.68 |
| 2026-02-27 | 5475.42 | 697.44 | 0.00 |
| 2026-02-28 | 5322.06 | -153.36 | -153.36 |
| 2026-03-01 | 5557.61 | 235.55 | 0.00 |
| 2026-03-02 | 5473.02 | -84.59 | -84.59 |
| 2026-03-03 | 5362.85 | -110.17 | -194.76 |
| 2026-03-04 | 5356.15 | -6.70 | -201.46 |
| 2026-03-05 | 5525.51 | 169.36 | -32.10 |
| 2026-03-06 | 5052.58 | -472.93 | -505.03 |
| 2026-03-07 | 5218.88 | 166.31 | -338.73 |
| 2026-03-08 | 5187.52 | -31.37 | -370.10 |
| 2026-03-09 | 5163.34 | -24.18 | -394.28 |
| 2026-03-10 | 5269.65 | 106.31 | -287.96 |
| 2026-03-11 | 5121.57 | -148.08 | -436.04 |
| 2026-03-12 | 5083.27 | -38.31 | -474.34 |
| 2026-03-13 | 4974.09 | -109.18 | -583.52 |
| 2026-03-14 | 5018.08 | 43.99 | -539.53 |
| 2026-03-15 | 5150.63 | 132.55 | -406.99 |
| 2026-03-16 | 5480.57 | 329.94 | -77.04 |
| 2026-03-17 | 5510.89 | 30.32 | -46.72 |
| 2026-03-18 | 5702.20 | 191.31 | 0.00 |
| 2026-03-19 | 5495.32 | -206.88 | -206.88 |
| 2026-03-20 | 5889.21 | 393.89 | 0.00 |
| 2026-03-21 | 5485.11 | -404.10 | -404.10 |
| 2026-03-22 | 5325.75 | -159.37 | -563.46 |
| 2026-03-23 | 5321.55 | -4.19 | -567.66 |
| 2026-03-25 | 5261.62 | -59.93 | -627.59 |
| 2026-03-26 | 5293.12 | 31.50 | -596.09 |
| 2026-03-27 | 5438.68 | 145.56 | -450.53 |
| 2026-03-28 | 5501.55 | 62.87 | -387.66 |
| 2026-03-29 | 5573.90 | 72.35 | -315.31 |
| 2026-03-30 | 5547.23 | -26.66 | -341.98 |
| 2026-03-31 | 5556.40 | 9.17 | -332.81 |
| 2026-04-01 | 5872.58 | 316.17 | -16.63 |
| 2026-04-02 | 6349.56 | 476.98 | 0.00 |
| 2026-04-03 | 6425.68 | 76.12 | 0.00 |
| 2026-04-04 | 6373.37 | -52.30 | -52.30 |
| 2026-04-05 | 6532.56 | 159.18 | 0.00 |
| 2026-04-06 | 6547.88 | 15.32 | 0.00 |
| 2026-04-07 | 6483.81 | -64.07 | -64.07 |
| 2026-04-08 | 6630.43 | 146.62 | 0.00 |
| 2026-04-09 | 7225.10 | 594.66 | 0.00 |
| 2026-04-10 | 7187.90 | -37.20 | -37.20 |
| 2026-04-11 | 7082.87 | -105.03 | -142.23 |
| 2026-04-12 | 7110.60 | 27.73 | -114.49 |
| 2026-04-13 | 7053.18 | -57.42 | -171.92 |
| 2026-04-14 | 7102.62 | 49.44 | -122.47 |
| 2026-04-15 | 7103.05 | 0.42 | -122.05 |
| 2026-04-16 | 7124.47 | 21.42 | -100.63 |
| 2026-04-17 | 7010.50 | -113.96 | -214.59 |
| 2026-04-18 | 6914.07 | -96.43 | -311.03 |
| 2026-04-19 | 7136.03 | 221.96 | -89.07 |
| 2026-04-20 | 7145.08 | 9.05 | -80.02 |
| 2026-04-21 | 7259.03 | 113.95 | 0.00 |
| 2026-04-22 | 7582.55 | 323.51 | 0.00 |
| 2026-04-23 | 7340.83 | -241.71 | -241.71 |
| 2026-04-24 | 7354.60 | 13.77 | -227.94 |
| 2026-04-25 | 7121.71 | -232.90 | -460.84 |
| 2026-04-26 | 7127.07 | 5.36 | -455.48 |
| 2026-04-27 | 7225.23 | 98.16 | -357.32 |
| 2026-04-28 | 7202.78 | -22.45 | -379.77 |
| 2026-04-29 | 7247.57 | 44.79 | -334.98 |
| 2026-04-30 | 7250.00 | 2.43 | -332.55 |
| 2026-05-01 | 7200.88 | -49.12 | -381.67 |
| 2026-05-02 | 7253.05 | 52.17 | -329.50 |
| 2026-05-03 | 7299.19 | 46.14 | -283.36 |
| 2026-05-04 | 7223.43 | -75.76 | -359.12 |
| 2026-05-05 | 7148.41 | -75.02 | -434.14 |
| 2026-05-06 | 7176.35 | 27.94 | -406.20 |
| 2026-05-07 | 7271.49 | 95.14 | -311.06 |
| 2026-05-08 | 7336.93 | 65.44 | -245.62 |
| 2026-05-09 | 7417.99 | 81.06 | -164.55 |
| 2026-05-10 | 7336.63 | -81.37 | -245.92 |
| 2026-05-11 | 7382.96 | 46.33 | -199.59 |
| 2026-05-12 | 7688.10 | 305.14 | 0.00 |
| 2026-05-13 | 7739.20 | 51.10 | 0.00 |
| 2026-05-18 | 7791.58 | 52.38 | 0.00 |
| 2026-05-19 | 7724.77 | -66.81 | -66.81 |
| 2026-05-20 | 7567.59 | -157.17 | -223.98 |
| 2026-05-21 | 7586.68 | 19.09 | -204.90 |
| 2026-05-22 | 7698.24 | 111.56 | -93.34 |
| 2026-05-23 | 7797.77 | 99.53 | 0.00 |
| 2026-05-24 | 7734.49 | -63.28 | -63.28 |
| 2026-05-25 | 8214.99 | 480.50 | 0.00 |
| 2026-05-26 | 8312.33 | 97.35 | 0.00 |
| 2026-05-27 | 8597.96 | 285.62 | 0.00 |
| 2026-05-28 | 8678.23 | 80.27 | 0.00 |
| 2026-05-29 | 9017.79 | 339.56 | 0.00 |
| 2026-05-30 | 9079.73 | 61.95 | 0.00 |
| 2026-05-31 | 9266.70 | 186.97 | 0.00 |
| 2026-06-01 | 9372.13 | 105.43 | 0.00 |
| 2026-06-02 | 9382.53 | 10.40 | 0.00 |
| 2026-06-03 | 8844.76 | -537.77 | -537.77 |
| 2026-06-04 | 9396.30 | 551.54 | 0.00 |
| 2026-06-05 | 9253.74 | -142.56 | -142.56 |
| 2026-06-06 | 9447.31 | 193.57 | 0.00 |
| 2026-06-07 | 9510.09 | 62.78 | 0.00 |
| 2026-06-08 | 9599.74 | 89.65 | 0.00 |
| 2026-06-09 | 9598.81 | -0.93 | -0.93 |
| 2026-06-10 | 9593.39 | -5.41 | -6.34 |
| 2026-06-11 | 9762.87 | 169.48 | 0.00 |
| 2026-06-12 | 10036.63 | 273.76 | 0.00 |
| 2026-06-13 | 10050.74 | 14.11 | 0.00 |
| 2026-06-14 | 10118.12 | 67.38 | 0.00 |
| 2026-06-15 | 10005.16 | -112.96 | -112.96 |
| 2026-06-16 | 10152.77 | 147.61 | 0.00 |
| 2026-06-17 | 10694.49 | 541.72 | 0.00 |
| 2026-06-18 | 10795.32 | 100.83 | 0.00 |
| 2026-06-19 | 10826.37 | 31.05 | 0.00 |
| 2026-06-20 | 10963.28 | 136.90 | 0.00 |
| 2026-06-21 | 11579.83 | 616.55 | 0.00 |
| 2026-06-22 | 11520.00 | -59.83 | -59.83 |
| 2026-06-23 | 11915.39 | 395.40 | 0.00 |
| 2026-06-24 | 11954.40 | 39.01 | 0.00 |
| 2026-06-25 | 12317.64 | 363.24 | 0.00 |
| 2026-06-26 | 12303.64 | -14.00 | -14.00 |
| 2026-06-27 | 12132.79 | -170.86 | -184.85 |
| 2026-06-28 | 12021.50 | -111.29 | -296.14 |
| 2026-06-29 | 12096.21 | 74.71 | -221.43 |
| 2026-06-30 | 11997.65 | -98.55 | -319.99 |
| 2026-07-01 | 12219.91 | 222.26 | -97.73 |
| 2026-07-02 | 12335.83 | 115.91 | 0.00 |
| 2026-07-03 | 12454.40 | 118.58 | 0.00 |
| 2026-07-04 | 13156.88 | 702.47 | 0.00 |
| 2026-07-05 | 13071.30 | -85.58 | -85.58 |
| 2026-07-06 | 12413.30 | -657.99 | -743.57 |
| 2026-07-07 | 13545.85 | 1132.55 | 0.00 |
| 2026-07-08 | 13594.83 | 48.98 | 0.00 |
| 2026-07-09 | 13602.87 | 8.04 | 0.00 |
| 2026-07-10 | 14078.18 | 475.31 | 0.00 |
| 2026-07-11 | 14539.65 | 461.46 | 0.00 |
| 2026-07-12 | 15223.37 | 683.72 | 0.00 |
| 2026-07-13 | 15310.26 | 86.89 | 0.00 |
| 2026-07-14 | 15699.25 | 388.99 | 0.00 |
| 2026-07-15 | 16013.83 | 314.58 | 0.00 |
| 2026-07-16 | 16139.21 | 125.38 | 0.00 |
| 2026-07-17 | 16154.85 | 15.64 | 0.00 |
| 2026-07-18 | 16473.65 | 318.80 | 0.00 |
| 2026-07-19 | 16521.83 | 48.18 | 0.00 |
| 2026-07-20 | 16485.43 | -36.39 | -36.39 |
| 2026-07-21 | 16625.83 | 140.40 | 0.00 |
| 2026-07-22 | 17002.89 | 377.06 | 0.00 |
| 2026-07-23 | 17120.43 | 117.54 | 0.00 |
| 2026-07-24 | 17118.05 | -2.37 | -2.37 |
| 2026-07-25 | 17014.93 | -103.12 | -105.50 |
| 2026-07-26 | 16605.35 | -409.59 | -515.08 |
| 2026-07-27 | 16714.64 | 109.29 | -405.79 |
| 2026-07-28 | 16806.90 | 92.26 | -313.53 |
| 2026-07-29 | 16897.40 | 90.50 | -223.03 |
| 2026-07-30 | 16992.74 | 95.34 | -127.69 |
| 2026-07-31 | 16997.03 | 4.29 | -123.40 |
| 2026-08-01 | 16783.98 | -213.05 | -336.45 |
| 2026-08-02 | 17132.61 | 348.63 | 0.00 |
| 2026-08-03 | 17166.03 | 33.42 | 0.00 |
| 2026-08-04 | 17250.56 | 84.54 | 0.00 |
| 2026-08-05 | 17411.04 | 160.48 | 0.00 |
| 2026-08-06 | 17337.12 | -73.92 | -73.92 |
| 2026-08-07 | 17439.25 | 102.13 | 0.00 |
| 2026-08-08 | 17500.64 | 61.39 | 0.00 |
| 2026-08-09 | 16978.51 | -522.13 | -522.13 |
| 2026-08-10 | 17014.01 | 35.50 | -486.63 |
| 2026-08-11 | 17023.60 | 9.59 | -477.04 |
| 2026-08-12 | 17182.42 | 158.81 | -318.22 |
| 2026-08-13 | 17112.56 | -69.86 | -388.08 |
| 2026-08-14 | 17214.80 | 102.24 | -285.84 |
| 2026-08-15 | 17374.89 | 160.09 | -125.75 |
| 2026-08-16 | 16979.25 | -395.64 | -521.40 |
| 2026-08-17 | 16885.95 | -93.30 | -614.69 |
| 2026-08-18 | 16794.90 | -91.05 | -705.74 |
| 2026-08-19 | 16848.61 | 53.71 | -652.03 |
| 2026-08-20 | 16812.88 | -35.74 | -687.76 |
| 2026-08-21 | 16853.19 | 40.31 | -647.45 |
| 2026-08-22 | 16945.40 | 92.21 | -555.24 |
| 2026-08-23 | 16660.79 | -284.61 | -839.86 |
| 2026-08-24 | 16661.90 | 1.12 | -838.74 |

</details>

### 4b. Closed-positions equity (alt — critical for buy-only books)

- Final closed equity: **-$844.29**
- Max DD: **-$15,819.00**
- Daily Sharpe (ann.): **-0.162**
- Days: 215

Files: `equity_curve_closed.csv` · `equity_curve_closed.json` (source=`closed_positions`)

<details><summary>Daily closed equity table (full)</summary>

| Date | Equity | Daily PnL | Drawdown |
|---|---:|---:|---:|
| 2026-01-16 | -121.86 | -121.86 | -121.86 |
| 2026-01-17 | 92.88 | 214.74 | 0.00 |
| 2026-01-18 | 13.12 | -79.75 | -79.75 |
| 2026-01-19 | 252.04 | 238.92 | 0.00 |
| 2026-01-20 | -28.23 | -280.27 | -280.27 |
| 2026-01-21 | -127.14 | -98.92 | -379.18 |
| 2026-01-22 | -95.46 | 31.68 | -347.50 |
| 2026-01-23 | 106.59 | 202.05 | -145.45 |
| 2026-01-24 | 39.73 | -66.86 | -212.31 |
| 2026-01-25 | 33.74 | -5.99 | -218.30 |
| 2026-01-26 | -185.53 | -219.27 | -437.57 |
| 2026-01-27 | -180.49 | 5.04 | -432.53 |
| 2026-01-28 | -197.11 | -16.62 | -449.15 |
| 2026-01-29 | -314.92 | -117.81 | -566.96 |
| 2026-01-30 | -308.51 | 6.41 | -560.55 |
| 2026-01-31 | -347.10 | -38.59 | -599.14 |
| 2026-02-01 | -316.02 | 31.09 | -568.06 |
| 2026-02-02 | -155.65 | 160.37 | -407.69 |
| 2026-02-03 | -11.42 | 144.23 | -263.46 |
| 2026-02-04 | 195.23 | 206.66 | -56.81 |
| 2026-02-05 | 353.03 | 157.80 | 0.00 |
| 2026-02-06 | 113.54 | -239.49 | -239.49 |
| 2026-02-07 | 435.51 | 321.97 | 0.00 |
| 2026-02-08 | 873.74 | 438.24 | 0.00 |
| 2026-02-09 | 430.19 | -443.55 | -443.55 |
| 2026-02-10 | 1096.59 | 666.40 | 0.00 |
| 2026-02-11 | 1954.30 | 857.70 | 0.00 |
| 2026-02-12 | 4641.64 | 2687.34 | 0.00 |
| 2026-02-13 | 4264.97 | -376.67 | -376.67 |
| 2026-02-14 | 4730.51 | 465.54 | 0.00 |
| 2026-02-15 | 4781.94 | 51.43 | 0.00 |
| 2026-02-16 | 4893.06 | 111.13 | 0.00 |
| 2026-02-17 | 5219.26 | 326.19 | 0.00 |
| 2026-02-18 | 5024.60 | -194.66 | -194.66 |
| 2026-02-19 | 4128.41 | -896.18 | -1090.84 |
| 2026-02-20 | 3767.16 | -361.25 | -1452.09 |
| 2026-02-21 | 4753.87 | 986.70 | -465.39 |
| 2026-02-22 | 4875.83 | 121.97 | -343.42 |
| 2026-02-23 | 4996.49 | 120.66 | -222.76 |
| 2026-02-24 | 4843.71 | -152.78 | -375.54 |
| 2026-02-25 | 4961.58 | 117.87 | -257.67 |
| 2026-02-26 | 4540.77 | -420.81 | -678.48 |
| 2026-02-27 | 4949.70 | 408.93 | -269.55 |
| 2026-02-28 | 5064.60 | 114.89 | -154.66 |
| 2026-03-01 | 5378.24 | 313.64 | 0.00 |
| 2026-03-02 | 5151.38 | -226.86 | -226.86 |
| 2026-03-03 | 5195.66 | 44.29 | -182.57 |
| 2026-03-04 | 5174.69 | -20.97 | -203.54 |
| 2026-03-05 | 5344.89 | 170.20 | -33.35 |
| 2026-03-06 | 5309.06 | -35.83 | -69.18 |
| 2026-03-07 | 4984.57 | -324.49 | -393.67 |
| 2026-03-08 | 5000.56 | 15.99 | -377.68 |
| 2026-03-09 | 4932.53 | -68.02 | -445.71 |
| 2026-03-10 | 5061.14 | 128.60 | -317.10 |
| 2026-03-11 | 4945.95 | -115.18 | -432.28 |
| 2026-03-12 | 4835.30 | -110.66 | -542.94 |
| 2026-03-13 | 4729.92 | -105.37 | -648.32 |
| 2026-03-14 | 4779.60 | 49.68 | -598.64 |
| 2026-03-15 | 4971.42 | 191.82 | -406.82 |
| 2026-03-16 | 5153.83 | 182.41 | -224.41 |
| 2026-03-17 | 5129.60 | -24.23 | -248.63 |
| 2026-03-18 | 5320.63 | 191.02 | -57.61 |
| 2026-03-19 | 5063.76 | -256.87 | -314.48 |
| 2026-03-20 | 5465.26 | 401.49 | 0.00 |
| 2026-03-21 | 5231.57 | -233.69 | -233.69 |
| 2026-03-22 | 5127.47 | -104.10 | -337.79 |
| 2026-03-23 | 4733.67 | -393.80 | -731.58 |
| 2026-03-25 | 4691.31 | -42.36 | -773.94 |
| 2026-03-26 | 4722.82 | 31.51 | -742.44 |
| 2026-03-27 | 4874.67 | 151.85 | -590.59 |
| 2026-03-28 | 4950.50 | 75.83 | -514.76 |
| 2026-03-29 | 5020.38 | 69.88 | -444.88 |
| 2026-03-30 | 4986.63 | -33.74 | -478.62 |
| 2026-03-31 | 5394.19 | 407.56 | -71.06 |
| 2026-04-01 | 6174.98 | 780.79 | 0.00 |
| 2026-04-02 | 3607.37 | -2567.61 | -2567.61 |
| 2026-04-03 | 3704.41 | 97.04 | -2470.57 |
| 2026-04-04 | 3110.09 | -594.33 | -3064.90 |
| 2026-04-05 | 2712.62 | -397.46 | -3462.36 |
| 2026-04-06 | 2817.93 | 105.31 | -3357.05 |
| 2026-04-07 | 1578.29 | -1239.64 | -4596.69 |
| 2026-04-08 | 1686.02 | 107.72 | -4488.96 |
| 2026-04-09 | 555.92 | -1130.10 | -5619.06 |
| 2026-04-10 | 659.60 | 103.68 | -5515.38 |
| 2026-04-11 | -160.94 | -820.54 | -6335.92 |
| 2026-04-12 | -115.52 | 45.42 | -6290.50 |
| 2026-04-13 | -3217.00 | -3101.48 | -9391.98 |
| 2026-04-14 | -3948.50 | -731.50 | -10123.48 |
| 2026-04-15 | -3933.10 | 15.40 | -10108.08 |
| 2026-04-16 | -3621.62 | 311.48 | -9796.60 |
| 2026-04-17 | -3765.36 | -143.74 | -9940.35 |
| 2026-04-18 | -4298.55 | -533.19 | -10473.54 |
| 2026-04-19 | -4137.08 | 161.47 | -10312.07 |
| 2026-04-20 | -4105.53 | 31.55 | -10280.52 |
| 2026-04-21 | -4508.91 | -403.38 | -10683.90 |
| 2026-04-22 | -5472.11 | -963.20 | -11647.10 |
| 2026-04-23 | -6095.54 | -623.42 | -12270.52 |
| 2026-04-24 | -6675.45 | -579.92 | -12850.44 |
| 2026-04-25 | -7303.83 | -628.38 | -13478.82 |
| 2026-04-26 | -7677.84 | -374.01 | -13852.82 |
| 2026-04-27 | -7390.41 | 287.43 | -13565.40 |
| 2026-04-28 | -8401.71 | -1011.30 | -14576.69 |
| 2026-04-29 | -8356.91 | 44.80 | -14531.89 |
| 2026-04-30 | -8354.47 | 2.44 | -14529.45 |
| 2026-05-01 | -8403.59 | -49.12 | -14578.57 |
| 2026-05-02 | -8351.42 | 52.17 | -14526.41 |
| 2026-05-03 | -8305.28 | 46.14 | -14480.27 |
| 2026-05-04 | -9569.02 | -1263.73 | -15744.00 |
| 2026-05-05 | -9644.01 | -75.00 | -15819.00 |
| 2026-05-06 | -9621.07 | 22.95 | -15796.05 |
| 2026-05-07 | -9525.92 | 95.15 | -15700.90 |
| 2026-05-08 | -9479.78 | 46.14 | -15654.76 |
| 2026-05-09 | -9398.68 | 81.10 | -15573.66 |
| 2026-05-10 | -9400.08 | -1.40 | -15575.06 |
| 2026-05-11 | -9396.69 | 3.38 | -15571.68 |
| 2026-05-12 | -9135.78 | 260.91 | -15310.77 |
| 2026-05-13 | -9084.67 | 51.11 | -15259.66 |
| 2026-05-14 | -9066.93 | 17.74 | -15241.92 |
| 2026-05-18 | -9014.56 | 52.38 | -15189.54 |
| 2026-05-19 | -9138.74 | -124.19 | -15313.73 |
| 2026-05-20 | -9242.86 | -104.12 | -15417.84 |
| 2026-05-21 | -9225.62 | 17.24 | -15400.60 |
| 2026-05-22 | -9114.03 | 111.59 | -15289.01 |
| 2026-05-23 | -9017.18 | 96.85 | -15192.16 |
| 2026-05-24 | -9082.41 | -65.24 | -15257.40 |
| 2026-05-25 | -8603.12 | 479.29 | -14778.10 |
| 2026-05-26 | -8509.43 | 93.69 | -14684.41 |
| 2026-05-27 | -8292.64 | 216.79 | -14467.63 |
| 2026-05-28 | -8188.04 | 104.60 | -14363.02 |
| 2026-05-29 | -7811.90 | 376.14 | -13986.88 |
| 2026-05-30 | -7752.15 | 59.75 | -13927.13 |
| 2026-05-31 | -7597.29 | 154.86 | -13772.27 |
| 2026-06-01 | -7464.40 | 132.89 | -13639.38 |
| 2026-06-02 | -7456.37 | 8.03 | -13631.35 |
| 2026-06-03 | -7471.77 | -15.40 | -13646.75 |
| 2026-06-04 | -7441.00 | 30.77 | -13615.98 |
| 2026-06-05 | -7501.50 | -60.50 | -13676.48 |
| 2026-06-06 | -7493.27 | 8.23 | -13668.25 |
| 2026-06-07 | -7332.61 | 160.66 | -13507.59 |
| 2026-06-08 | -7233.84 | 98.77 | -13408.82 |
| 2026-06-09 | -7252.38 | -18.55 | -13427.37 |
| 2026-06-11 | -7216.31 | 36.07 | -13391.29 |
| 2026-06-12 | -6930.98 | 285.32 | -13105.97 |
| 2026-06-13 | -6945.89 | -14.90 | -13120.87 |
| 2026-06-14 | -6938.03 | 7.86 | -13113.01 |
| 2026-06-15 | -7061.41 | -123.38 | -13236.39 |
| 2026-06-16 | -6999.03 | 62.38 | -13174.01 |
| 2026-06-17 | -6596.90 | 402.13 | -12771.88 |
| 2026-06-18 | -6587.48 | 9.42 | -12762.46 |
| 2026-06-19 | -6343.94 | 243.54 | -12518.92 |
| 2026-06-20 | -6261.59 | 82.34 | -12436.58 |
| 2026-06-21 | -6178.36 | 83.23 | -12353.34 |
| 2026-06-22 | -6178.50 | -0.14 | -12353.48 |
| 2026-06-23 | -5832.82 | 345.67 | -12007.81 |
| 2026-06-24 | -5930.20 | -97.38 | -12105.18 |
| 2026-06-25 | -5522.25 | 407.95 | -11697.24 |
| 2026-06-26 | -5527.51 | -5.26 | -11702.50 |
| 2026-06-27 | -5696.41 | -168.90 | -11871.40 |
| 2026-06-28 | -5815.32 | -118.90 | -11990.30 |
| 2026-06-29 | -5638.71 | 176.61 | -11813.69 |
| 2026-06-30 | -5818.79 | -180.09 | -11993.78 |
| 2026-07-01 | -5603.74 | 215.05 | -11778.73 |
| 2026-07-02 | -5491.68 | 112.06 | -11666.67 |
| 2026-07-03 | -5227.67 | 264.01 | -11402.66 |
| 2026-07-04 | -4659.87 | 567.81 | -10834.85 |
| 2026-07-05 | -4455.76 | 204.10 | -10630.75 |
| 2026-07-06 | -5157.59 | -701.83 | -11332.58 |
| 2026-07-07 | -4256.61 | 900.98 | -10431.60 |
| 2026-07-08 | -4288.62 | -32.00 | -10463.60 |
| 2026-07-09 | -4289.21 | -0.60 | -10464.20 |
| 2026-07-10 | -3829.43 | 459.78 | -10004.42 |
| 2026-07-11 | -3523.54 | 305.89 | -9698.52 |
| 2026-07-12 | -3163.95 | 359.59 | -9338.94 |
| 2026-07-13 | -2846.38 | 317.57 | -9021.37 |
| 2026-07-14 | -2457.29 | 389.09 | -8632.27 |
| 2026-07-15 | -2148.82 | 308.47 | -8323.80 |
| 2026-07-16 | -2142.67 | 6.14 | -8317.66 |
| 2026-07-17 | -2131.68 | 10.99 | -8306.67 |
| 2026-07-18 | -1802.39 | 329.29 | -7977.37 |
| 2026-07-19 | -1697.01 | 105.38 | -7872.00 |
| 2026-07-20 | -1661.70 | 35.31 | -7836.68 |
| 2026-07-21 | -1641.69 | 20.01 | -7816.68 |
| 2026-07-22 | -1377.32 | 264.37 | -7552.31 |
| 2026-07-23 | -1285.99 | 91.34 | -7460.97 |
| 2026-07-24 | -1138.29 | 147.70 | -7313.28 |
| 2026-07-25 | -1140.11 | -1.82 | -7315.09 |
| 2026-07-26 | -1654.01 | -513.90 | -7829.00 |
| 2026-07-27 | -1460.12 | 193.89 | -7635.11 |
| 2026-07-28 | -1387.68 | 72.44 | -7562.66 |
| 2026-07-29 | -1300.36 | 87.32 | -7475.34 |
| 2026-07-30 | -1295.15 | 5.22 | -7470.13 |
| 2026-08-01 | -1232.16 | 62.99 | -7407.14 |
| 2026-08-02 | -1160.54 | 71.62 | -7335.52 |
| 2026-08-03 | -1129.89 | 30.65 | -7304.87 |
| 2026-08-04 | -1045.98 | 83.91 | -7220.96 |
| 2026-08-05 | -926.34 | 119.64 | -7101.32 |
| 2026-08-06 | -978.51 | -52.17 | -7153.49 |
| 2026-08-07 | -897.90 | 80.61 | -7072.88 |
| 2026-08-08 | -771.28 | 126.62 | -6946.26 |
| 2026-08-09 | -1434.06 | -662.78 | -7609.05 |
| 2026-08-10 | -1403.50 | 30.56 | -7578.48 |
| 2026-08-11 | -1397.68 | 5.82 | -7572.66 |
| 2026-08-12 | -1218.66 | 179.02 | -7393.64 |
| 2026-08-13 | -1210.55 | 8.11 | -7385.54 |
| 2026-08-14 | -1180.41 | 30.15 | -7355.39 |
| 2026-08-15 | -1069.44 | 110.97 | -7244.42 |
| 2026-08-16 | -1031.80 | 37.64 | -7206.78 |
| 2026-08-17 | -1300.30 | -268.50 | -7475.28 |
| 2026-08-18 | -1390.77 | -90.47 | -7565.75 |
| 2026-08-19 | -1507.47 | -116.70 | -7682.45 |
| 2026-08-20 | -620.81 | 886.66 | -6795.79 |
| 2026-08-21 | -647.95 | -27.14 | -6822.93 |
| 2026-08-22 | -600.37 | 47.58 | -6775.35 |
| 2026-08-23 | -619.33 | -18.96 | -6794.31 |
| 2026-08-24 | -844.29 | -224.97 | -7019.28 |

</details>

### Top winners / losers contribution

Top10 winners $8,931.07 (17.76% of wins) · Top10 losers -$12,751.24 (24.93% of losses) · PF=0.9845

- WIN $2,507.61 · 42410s · Mavericks vs. Bucks: O/U 218.5
- WIN $1,681.83 · 64888s · ODI Series Bangladesh vs New Zealand: Bangladesh vs New Zealand
- WIN $841.25 · 1322s · Germany vs. Latvia: O/U 5.5
- WIN $700.14 · 3930719s · Atlanta Braves vs. Chicago White Sox: O/U 8.5
- WIN $607.74 · 56072s · Will India win?
- WIN $585.90 · 96s · Spread: Real Madrid CF (-1.5)
- WIN $571.57 · 10830s · T20 World Cup: Namibia vs Netherlands (Game 1)
- WIN $551.84 · 24128s · ODI Series New Zealand vs South Africa Women: New Zealand vs South Africa
- WIN $448.30 · 355s · Switzerland vs. Colombia: O/U 8.5 Total Corners
- WIN $434.89 · 1706s · Team USA Stars vs. Team USA Stripes

- LOSS -$729.97 · 5628s · T20 Series South Africa vs. India, Women: South Africa vs India
- LOSS -$815.00 · 14921s · Indian Premier League: Chennai Super Kings vs Kolkata Knight Riders
- LOSS -$846.30 · 4862s · T20 Series Bangladesh vs Sri Lanka, Women: Bangladesh vs Sri Lanka
- LOSS -$881.33 · 14912s · Indian Premier League: Chennai Super Kings vs Delhi Capitals
- LOSS -$1,100.42 · 17808s · T20 Series Indonesia vs Sweden: Indonesia vs Sweden
- LOSS -$1,267.38 · 19856s · T20 Challenge Trophy, Women: Rwanda vs Nepal
- LOSS -$1,268.29 · 8920s · Indian Premier League: Mumbai Indians vs Lucknow Super Giants
- LOSS -$1,272.23 · 77780s · T20 Series Namibia vs Scotland: Namibia vs Scotland
- LOSS -$2,176.10 · 3356s · Pakistan Super League: Peshawar Zalmi vs Multan Sultans
- LOSS -$2,394.22 · 12024s · Indian Premier League: Kolkata Knight Riders vs Sunrisers Hyderabad

## 5. Trade management deep dive

- Adverse early (>2¢): `{'n_early_adverse': 13, 'avg_pnl': -21.24, 'median_t_first_sell': 92, 'median_hold': 92}`
- Favorable first-sell: `{'n_first_sell_up_2c': 1708, 'avg_pnl': 18.28, 'median_mfe_capture': 1.0, 'mean_mfe_capture': 0.4497}`
- Campaigns: `{'n': 546, 'pct': 19.85, 'avg_entries': 2.53, 'pnl': 5803.69, 'avg_pnl': 10.63, 'win_rate': 0.7051, 'single_n': 2204, 'single_pnl': -6647.98, 'single_avg_pnl': -3.02}`
- Avg-down: `{'n_losers': 960, 'n_losers_with_red_buys': 343, 'pct_losers': 35.73, 'total_delta_if_skipped_on_losers': 3205.97, 'global_fifo_sim': 30483.6, 'global_fifo_never_red_buy': 25044.0, 'global_delta': -5439.6}`
- Resolution behavior: `{'flattened_before_flag_rate': 0.9876, 'hold_to_resolution_style_n': 281, 'redeems_usdc': 1243.869471, 'merges_usdc': 0.0}`
- Latency: `{'time_to_mfe_median': 1124, 'time_to_mfe_p25': 418, 'time_to_mfe_p75': 3351, 'time_to_mfe_p90': 9896, 'mfe_ge_10c_n': 998, 'mfe_ge_10c_within_30s': 5, 'mfe_ge_10c_within_60s': 30, 'pct_big_within_60s': 3.01}`

### What works / fails
- WORKS: Winners capture median spread 0.1 vs losers -0.0484
- WORKS: Both-sides inventory on 10.2% of winning markets (losers 7.4%)
- WORKS: Hold bucket 5-30m: avg PnL $5.27 on 1007 markets (WR 73%)
- WORKS: Hold bucket 12h+: avg PnL $34.03 on 81 markets (WR 79%)
- WORKS: Entry band 0.80-1.00: avg $12.47 across 227 markets
- WORKS: Buy-ladder behavior: fade-into-weakness markets=677, chase-up markets=225
- FAILS: Hold bucket 30m-2h: avg PnL $-5.36 on 777 markets
- FAILS: Hold bucket 2-12h: avg PnL $-14.10 on 387 markets

## 6. Strategy overview (in depth)

# Strategy Dossier: Winnertraders

- **Wallet:** `0x13464aabec792c36b062316f474713e681330448`
- **History span:** 2026-01-16T07:37:14+00:00 → 2026-08-23T03:42:52+00:00 (218.84 days)
- **Trades:** 20,475 (buys 11,909 / sells 8,566)
- **Markets touched:** 2,750
- **Closed positions:** 3,001

## Headline performance

| Metric | Value |
|---|---|
| Realized cashflow (sells − buys + redeems + rebates) | $16,661.90 |
| Core cashflow (ex-rebates) | $16,180.10 |
| Closed-positions realized sum | -$844.29 |
| Win rate (closed) | 65.11% (1952W / 1046L) |
| Profit factor | 0.9845 |
| Gross wins / losses | $53,716.10 / -$54,560.40 |
| Equity max drawdown | -$1,644.51 |
| Polymarket leaderboard (ALL) | $17,578.63 PnL · vol $2,032,708.12 · rank 9026 |

## Source validation

- **MATCH** `polymarket_leaderboard_ALL` pnl: ours=16661.9043 ref=17578.63184561259 diff=-916.7275
- **MATCH** `polydata` realized_pnl: ours=16661.9043 ref=17655.63 diff=-993.7257
- **DRIFT** `polydata` n_trades: ours=20475 ref=16162 diff=4313
- **DRIFT** `polydata` win_rate: ours=0.6511 ref=0.5926 diff=0.0585
- **DRIFT** `internal` cashflow_vs_closed: ours=16661.9043 ref=-844.295 diff=17506.1993

## What kind of trader is this?

**Classification:** `likely_market_maker` (score 65/100)

- Fast round-trips (<2h) in 81% of two-sided markets
- Avg sell > avg buy in 77% of markets (spread capture)
- High-frequency cadence (median gap 100s)
- Heavy concentration in Over/Under sports totals (sports MM niche)

Supporting rates — both-sides markets: 0.0924, fast round-trips: 0.8133, spread-capture rate: 0.7712.

## Exact edge thesis

Winnertraders primarily monetizes **liquidity / short-horizon mean reversion on sports markets**, not long-shot directional political bets. The tape shows repeated buy-then-sell with average exit price above average entry — the classic scalper / spread fingerprint.

See `bot_playbook.md` for the full entry/management/exit autopsy and bot architecture.

## Where the money comes from

- **sports_totals**: $9,253.28 across 1441 closed legs
- **other**: $994.88 across 152 closed legs
- **crypto**: -$294.95 across 33 closed legs
- **sports_match**: -$10,797.51 across 1375 closed legs

## Timing

- Peak UTC hours: 16, 17, 15, 20, 14
- Peak weekdays (0=Mon): [5, 6, 4]
- Median inter-trade gap: 1m 40s

## Sizing

- Median ticket $6.80, mean $22.67, p90 $62.50, max $2,575.00
- Share size median 29.04, mean 99.0755

## Trade-by-trade pattern (representative winners)

These vignettes are reconstructed from fills: average entry, average exit, hold time, and closed realized PnL.

### Mavericks vs. Bucks: O/U 218.5
- Entries ≈ **0.095** · Exits ≈ **0.484** · Spread ≈ **0.390**
- Fills: 14 buys / 3 sells · hold 11h 46m · both-sides=False · realized $2,507.61

### ODI Series Bangladesh vs New Zealand: Bangladesh vs New Zealand
- Entries ≈ **0.379** · Exits ≈ **0.399** · Spread ≈ **0.020**
- Fills: 26 buys / 15 sells · hold 18h 1m · both-sides=True · realized $1,681.83

### Atlanta Braves vs. Chicago White Sox: O/U 8.5
- Entries ≈ **0.103** · Exits ≈ **0.309** · Spread ≈ **0.206**
- Fills: 21 buys / 49 sells · hold 45d 11h · both-sides=True · realized $700.14

### Will India win?
- Entries ≈ **0.124** · Exits ≈ **0.426** · Spread ≈ **0.302**
- Fills: 11 buys / 10 sells · hold 15h 34m · both-sides=True · realized $607.74

### T20 World Cup: Namibia vs Netherlands (Game 1)
- Entries ≈ **0.056** · Exits ≈ **0.156** · Spread ≈ **0.101**
- Fills: 38 buys / 13 sells · hold 3h 0m · both-sides=True · realized $571.57

### ODI Series New Zealand vs South Africa Women: New Zealand vs South Africa
- Entries ≈ **0.190** · Exits ≈ **0.250** · Spread ≈ **0.060**
- Fills: 19 buys / 10 sells · hold 6h 42m · both-sides=False · realized $551.84

### Switzerland vs. Colombia: O/U 8.5 Total Corners
- Entries ≈ **0.359** · Exits ≈ **0.999** · Spread ≈ **0.640**
- Fills: 2 buys / 2 sells · hold 5m 55s · both-sides=False · realized $448.30

### Team USA Stars vs. Team USA Stripes
- Entries ≈ **0.178** · Exits ≈ **0.536** · Spread ≈ **0.359**
- Fills: 10 buys / 15 sells · hold 28m 26s · both-sides=True · realized $434.89

### T20 World Cup: England vs Nepal (Game 1)
- Entries ≈ **0.024** · Exits ≈ **0.113** · Spread ≈ **0.089**
- Fills: 26 buys / 27 sells · hold 3h 2m · both-sides=True · realized $396.01

### T20 World Cup, Sub Regional Africa, Qualifier A: Kenya vs Rwanda
- Entries ≈ **0.170** · Exits ≈ **0.465** · Spread ≈ **0.294**
- Fills: 14 buys / 25 sells · hold 47m 1s · both-sides=True · realized $391.40

## Top closed winners / losers

**Winners**
- Mavericks vs. Bucks: O/U 218.5: $2,507.61 · bought $607.89 · sold $3,115.47 · hold 11h 46m
- ODI Series Bangladesh vs New Zealand: Bangladesh vs New Zealand: $1,681.83 · bought $467.72 · sold $490.84 · hold 18h 1m
- Germany vs. Latvia: O/U 5.5: $841.25 · bought $48.68 · sold $889.93 · hold 22m 2s
- Atlanta Braves vs. Chicago White Sox: O/U 8.5: $700.14 · bought $349.30 · sold $1,049.72 · hold 45d 11h
- Will India win?: $607.74 · bought $254.82 · sold $876.75 · hold 15h 34m
- Spread: Real Madrid CF (-1.5): $585.90 · bought $141.75 · sold $727.65 · hold 1m 36s
- T20 World Cup: Namibia vs Netherlands (Game 1): $571.57 · bought $316.95 · sold $888.52 · hold 3h 0m
- ODI Series New Zealand vs South Africa Women: New Zealand vs South Africa: $551.84 · bought $345.05 · sold $446.27 · hold 6h 42m
- Switzerland vs. Colombia: O/U 8.5 Total Corners: $448.30 · bought $251.00 · sold $699.29 · hold 5m 55s
- Team USA Stars vs. Team USA Stripes: $434.89 · bought $215.24 · sold $650.13 · hold 28m 26s

**Losers**
- Indian Premier League: Kolkata Knight Riders vs Sunrisers Hyderabad: -$2,394.22 · bought $631.01 · sold $806.98
- Pakistan Super League: Peshawar Zalmi vs Multan Sultans: -$2,176.10 · bought $138.51 · sold $170.45
- T20 Series Namibia vs Scotland: Namibia vs Scotland: -$1,272.23 · bought $276.06 · sold $97.34
- Indian Premier League: Mumbai Indians vs Lucknow Super Giants: -$1,268.29 · bought $146.91 · sold $68.08
- T20 Challenge Trophy, Women: Rwanda vs Nepal: -$1,267.38 · bought $40.45 · sold $245.55
- T20 Series Indonesia vs Sweden: Indonesia vs Sweden: -$1,100.42 · bought $194.85 · sold $768.75
- Indian Premier League: Chennai Super Kings vs Delhi Capitals: -$881.33 · bought $241.53 · sold $153.92
- T20 Series Bangladesh vs Sri Lanka, Women: Bangladesh vs Sri Lanka: -$846.30 · bought $47.99 · sold $189.21
- Indian Premier League: Chennai Super Kings vs Kolkata Knight Riders: -$815.00 · bought $276.98 · sold $316.80
- T20 Series South Africa vs. India, Women: South Africa vs India: -$729.97 · bought $224.88 · sold $85.41

## Replication playbook (how to copy the edge)

1. **Universe:** Focus on liquid sports match + totals (O/U) markets with tight books.
2. **Role:** Quote or take both sides near mid; prioritize markets you can exit before resolution.
3. **Sizing:** Start near their median ticket (~$6.80) and scale only with inventory limits.
4. **Inventory:** Cap net Yes/No (or Over/Under) imbalance; flatten when mid moves through you.
5. **Hold time:** Target minutes–hours, not overnight directional risk, unless hedged via opposite outcome.
6. **Edge source:** Capture spread + mean reversion after flow, not oracle forecasting alpha.
7. **Ops:** Automate via CLOB maker orders; track maker rebates; kill-switch on drawdown.
8. **Do not blindly copy:** Their edge depends on latency, fee tier, and bankroll. Replicate *mechanics*, not wallet follows.

## Cashflow anatomy

- Buys: $224,791.72
- Sells: $239,727.95
- Redeems: $1,243.87
- Maker rebates: $378.60
- Taker rebates: $15.58

_Generated 2026-08-25T16:47:01.145390+00:00_


## 7. Bot / copy playbook

- Difficulty: **6/10** · Ease: **5/10**
- Why: Maker-led entries reduce latency race; still needs solid risk + universe selection.

### Build steps
1. Post-only bids in preferred price bands
2. Work asks above entry for exits (or redeem path if applicable)
3. Focus bands that print positive expectancy (see entry_price_band)
4. Paper trade until markout distribution matches

### Steal
- Maker-led entry style (better for quoting bots)
- Same-market campaign re-entries
- Prioritize hold bucket 5-15m (their PnL engine)

### Avoid
- Averaging down while red on losers

Bot parameters: `{'preferred_entry_price_median': 0.45, 'preferred_entry_price_p25_p75': (0.22, 0.65), 'target_spread_median': 0.1, 'target_spread_p75': 0.1971, 'max_hold_seconds_p75': 4461, 'median_hold_seconds': 1481, 'clip_size_usdc_median': 8.5113, 'clip_size_usdc_p90': 73.95, 'both_sides_on_winners_rate': 0.1025, 'require_exit_above_entry': True, 'flatten_before_resolution': True, 'maker_bias': True}`

# Elite Replication Playbook — Winnertraders

Wallet `0x13464aabec792c36b062316f474713e681330448`. Reverse-engineered from the **full unique fill tape** (20,475 trades · 2,750 markets). This is an implementation spec for a high-end bot, not vibes.

## 0. True strategy identity (read this first)

Classification `likely_market_maker` — mix of spread capture and directional inventory.

Heuristic label from the scanner may still say `likely_market_maker` because of fast round-trips + sell>buy + maker rebates. **Operationally, build a live scalper with optional maker quoting**, not a Yes/No pair inventory bot.

## 1. Performance anchors

| Source / metric | Value |
|---|---|
| Cashflow realized (sells−buys+redeems+rebates) | $16,661.90 |
| Core cashflow (ex-rebates) | $16,180.10 |
| Closed-position legs sum | -$844.29 |
| Leg win rate / profit factor | 65.11% / 0.9845 |
| Polymarket leaderboard ALL | $17,578.63 · vol $2,032,708.12 · rank 9026 |
| polymarket_leaderboard_ALL pnl | ref=17578.63184561259 ours=16661.9043 (MATCH) |
| polydata realized_pnl | ref=17655.63 ours=16661.9043 (MATCH) |
| polydata n_trades | ref=16162 ours=20475 (DRIFT) |
| polydata win_rate | ref=0.5926 ours=0.6511 (DRIFT) |

Notes: Polymarket leaderboard ALL is the primary official PnL check (we match within tolerance). PolyData uses a different event aggregation / trade counting method — expect DRIFT on WR and trade count; use it as a secondary research signal, not the ground truth for fills.

## 2. Universe — where the money is

- **O/U / totals:** 1390 markets · $9,410.53 · avg $6.77 · median hold 17m40s · median spread 0.09
- **Match / other sports:** 1078 markets · -$11,987.46 · avg -$11.12
- **Outcome PnL leaders:**
  - **Under**: $5,390.02
  - **Over**: $3,969.85
  - **New Zealand**: $2,364.86
  - **Punjab Kings**: $599.27
  - **Sport Lisboa e Benfica**: $585.90
  - **Netherlands**: $524.74

### Bot universe rules

1. Only liquid live sports (soccer/football first — their tape is soccer-heavy).
2. Prefer O/U lines with tight books and active in-game trading.
3. Default bias toward **Over** unless your signal says otherwise (their Over PnL dominates).
4. Skip politics/crypto until you have separate evidence.
5. Require enough depth to enter ~median clip and exit within 1–2 minutes.

## 3. ENTRY — exact mechanics

### Style histogram
- `directional_buy_cheap_tail`: 746
- `directional_buy_sub_mid`: 577
- `directional_buy_above_mid`: 512
- `directional_buy_near_mid`: 332
- `directional_buy_expensive_favorite`: 329
- `two_sided_inventory_cheap_tail`: 86
- `two_sided_inventory_sub_mid`: 51
- `two_sided_inventory_above_mid`: 49
- `two_sided_inventory_near_mid`: 43
- `two_sided_inventory_expensive_favorite`: 25

### First-two-fill sequences
- `BUY->BUY`: 1547
- `BUY->SELL`: 1110
- `single_fill`: 93

### Entry price → realized edge

| Avg buy band | Markets | Total PnL | Avg PnL |
|---|---:|---:|---:|
| 0.00-0.20 | 748 | -$2,672.31 | -$3.57 |
| 0.20-0.40 | 671 | -$2,758.27 | -$4.11 |
| 0.40-0.60 | 639 | $1,638.26 | $2.56 |
| 0.60-0.80 | 465 | $117.08 | $0.25 |
| 0.80-1.00 | 227 | $2,830.94 | $12.47 |

**Best band:** 0.40–0.60 (near mid) — highest average PnL. Tails (≤0.20 or ≥0.80) make less per market.

### Entry checklist (bot)

1. Clip **$8.51** median (p90 $73.95).
2. Aim entry price ~**0.45** (IQR (0.22, 0.65)).
3. Trigger = microstructure, not long-term forecast:
   - mid dips / liquidity hole you can buy
   - imminent volatility (attack, corner, shot) where Over can jump
   - resting bid gets lifted? you’re being taken — manage immediately
4. Prefer **maker bids**; take only if the expected jump already started and ask is still inside your edge.
5. Same-second multi-fills are normal (one order, many counterparties) — treat as one decision, many fills.

## 4. MANAGEMENT — what they do after entry

### Styles
- `intraday_swing`: 737
- `single_clip`: 669
- `scalp_sub_15m`: 546
- `scale_in_scale_out`: 382
- `market_make_both_outcomes`: 245
- `multi_hour_position`: 171

### Winners vs losers

| Metric | Winners | Losers |
|---|---:|---:|
| N | 1785 | 960 |
| PnL | $50,301.01 | -$51,145.30 |
| Median hold | 24m41s | 25m14s |
| Median spread | 0.1 | -0.0484 |
| Scale-in rate | 0.558 | 0.7208 |
| Scale-out rate | 0.5697 | 0.4146 |
| Avg fills/market | 7.06 | 8.18 |
| Both-sides rate | 0.1025 | 0.074 |

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

- **Winners** sell above buy (median spread **0.1**). **Losers** often exit worse (median spread **-0.0484**).
- Losers scale-in **more** (0.7208 vs 0.558) — averaging down is how they bleed; the bot should **forbid** revenge scale-ins without a fresh signal.
- Hold edge peaks in **<5m** ({'n': 498, 'pnl': 716.6684, 'avg': 1.4391, 'win_rate': 0.512}) and a strong **30m–2h** bucket for the larger in-game campaigns.

## 5. EXIT — rules that print

- `spread_harvest_sell_above_buy`: 1824
- `adverse_exit_sell_below_buy`: 500
- `hold_to_resolution_or_redeem`: 281
- `mixed_roundtrip`: 145

| Hold bucket | N | Total PnL | Avg | Win rate |
|---|---:|---:|---:|---:|
| <5m | 498 | $716.67 | $1.44 | 51.2% |
| 5-30m | 1007 | $5,305.61 | $5.27 | 73.0% |
| 30m-2h | 777 | -$4,167.19 | -$5.36 | 62.4% |
| 2-12h | 387 | -$5,456.08 | -$14.10 | 63.6% |
| 12h+ | 81 | $2,756.70 | $34.03 | 79.0% |

### Exit engine params

1. **TP / ask distance:** target ≈ **0.1** above avg entry (p75 stretch 0.1971). On live O/U this is often a burst move, not slow grind.
2. **Time stop:** median hold 24m41s; p75 1h14m for the scalps — escalate urgency after that.
3. **Scale-out:** peel into strength (their winners stack sells). Don’t wait for one perfect print.
4. **Stop:** if mid < entry − ~3–5¢ on unhedged inventory with no signal → take the loss (copy losers’ speed, not their hope).
5. **Flatten before resolution** — redeem is residual.
6. Taker exits are fine when the move already happened and maker asks won’t fill.

## 6. What works / what fails

### Works
- Winners capture median spread 0.1 vs losers -0.0484
- Both-sides inventory on 10.2% of winning markets (losers 7.4%)
- Hold bucket 5-30m: avg PnL $5.27 on 1007 markets (WR 73%)
- Hold bucket 12h+: avg PnL $34.03 on 81 markets (WR 79%)
- Entry band 0.80-1.00: avg $12.47 across 227 markets
- Buy-ladder behavior: fade-into-weakness markets=677, chase-up markets=225

### Fails
- Hold bucket 30m-2h: avg PnL $-5.36 on 777 markets
- Hold bucket 2-12h: avg PnL $-14.10 on 387 markets
- Chase vs fade ladders: `{'chase_up': 225, 'fade_down': 677}`

## 7. Fill-by-fill autopsies (copy these patterns)

### Example 1: Mavericks vs. Bucks: O/U 218.5
PnL $2,507.61 · hold 11h46m · 14B/3S · avg entry 0.0945 → exit 0.4845 (spread 0.39) · `scale_in_scale_out`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-02-12T04:47:41+00:00 | BUY | Over | 935.00 | 0.2130 | 199.16 |
| 2026-02-12T07:11:17+00:00 | BUY | Over | 200.00 | 0.1020 | 20.40 |
| 2026-02-12T07:11:39+00:00 | BUY | Over | 1892.50 | 0.1030 | 194.93 |
| 2026-02-12T07:25:05+00:00 | BUY | Over | 2000.00 | 0.0510 | 101.98 |
| 2026-02-12T07:25:39+00:00 | BUY | Over | 1083.83 | 0.0510 | 55.28 |
| 2026-02-12T08:39:51+00:00 | BUY | Over | 30.00 | 0.1192 | 3.58 |
| 2026-02-12T08:40:27+00:00 | BUY | Over | 5.00 | 0.1000 | 0.50 |
| 2026-02-12T08:50:55+00:00 | BUY | Over | 10.00 | 0.1355 | 1.35 |
| 2026-02-12T09:08:27+00:00 | BUY | Over | 87.00 | 0.1290 | 11.22 |
| 2026-02-12T09:10:09+00:00 | BUY | Over | 68.54 | 0.1044 | 7.16 |
| 2026-02-12T09:18:29+00:00 | BUY | Over | 20.50 | 0.1150 | 2.36 |
| 2026-02-12T09:31:43+00:00 | BUY | Over | 49.20 | 0.1020 | 5.02 |
| 2026-02-12T10:02:45+00:00 | BUY | Over | 19.80 | 0.1070 | 2.12 |
| 2026-02-12T10:06:25+00:00 | BUY | Over | 28.45 | 0.1000 | 2.85 |
| 2026-02-12T15:43:09+00:00 | SELL | Over | 20.82 | 0.3100 | 6.45 |
| 2026-02-12T16:34:31+00:00 | SELL | Over | 1409.00 | 0.3790 | 534.01 |
| 2026-02-12T16:34:31+00:00 | SELL | Over | 5000.00 | 0.5150 | 2575.00 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 2: ODI Series New Zealand vs South Africa Women: New Zealand vs South Africa
PnL $551.84 · hold 6h42m · 19B/10S · avg entry 0.1898 → exit 0.2497 (spread 0.0599) · `scale_in_scale_out`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-03-31T22:21:25+00:00 | BUY | New Zealand | 100.00 | 0.5600 | 56.00 |
| 2026-03-31T22:26:11+00:00 | BUY | New Zealand | 100.00 | 0.5500 | 55.00 |
| 2026-03-31T22:38:01+00:00 | SELL | New Zealand | 197.33 | 0.6200 | 122.34 |
| 2026-03-31T23:34:51+00:00 | BUY | New Zealand | 200.00 | 0.4100 | 82.00 |
| 2026-03-31T23:56:35+00:00 | BUY | New Zealand | 250.00 | 0.2100 | 52.50 |
| 2026-04-01T01:20:45+00:00 | BUY | New Zealand | 29.00 | 0.1100 | 3.19 |
| 2026-04-01T01:20:53+00:00 | BUY | New Zealand | 29.00 | 0.1100 | 3.19 |
| 2026-04-01T01:21:59+00:00 | BUY | New Zealand | 30.00 | 0.1100 | 3.30 |
| 2026-04-01T01:28:55+00:00 | BUY | New Zealand | 28.00 | 0.1100 | 3.08 |
| 2026-04-01T01:44:19+00:00 | BUY | New Zealand | 12.00 | 0.1100 | 1.32 |
| 2026-04-01T01:44:29+00:00 | BUY | New Zealand | 16.00 | 0.1100 | 1.76 |
| 2026-04-01T01:44:33+00:00 | BUY | New Zealand | 18.00 | 0.1100 | 1.98 |
| 2026-04-01T02:07:35+00:00 | BUY | New Zealand | 190.00 | 0.1100 | 20.90 |
| 2026-04-01T02:26:19+00:00 | BUY | New Zealand | 103.17 | 0.0900 | 9.29 |
| 2026-04-01T03:17:49+00:00 | BUY | New Zealand | 286.00 | 0.0800 | 22.88 |
| 2026-04-01T03:22:35+00:00 | BUY | New Zealand | 50.00 | 0.0700 | 3.50 |
| 2026-04-01T03:27:41+00:00 | BUY | New Zealand | 176.94 | 0.0600 | 10.62 |
| 2026-04-01T03:37:15+00:00 | BUY | New Zealand | 100.00 | 0.0400 | 4.00 |
| 2026-04-01T03:39:21+00:00 | BUY | New Zealand | 50.00 | 0.0400 | 2.00 |
| 2026-04-01T04:04:49+00:00 | SELL | New Zealand | 940.89 | 0.1010 | 95.06 |
| 2026-04-01T04:08:29+00:00 | SELL | New Zealand | 100.00 | 0.1600 | 16.00 |
| 2026-04-01T04:09:03+00:00 | SELL | New Zealand | 100.00 | 0.1900 | 19.00 |
| 2026-04-01T04:16:55+00:00 | SELL | New Zealand | 100.00 | 0.2400 | 24.00 |
| 2026-04-01T04:21:19+00:00 | SELL | New Zealand | 100.00 | 0.4100 | 41.00 |
| 2026-04-01T04:23:35+00:00 | SELL | New Zealand | 50.00 | 0.5500 | 27.50 |
| 2026-04-01T04:24:55+00:00 | SELL | New Zealand | 50.00 | 0.5700 | 28.50 |
| 2026-04-01T04:39:49+00:00 | SELL | New Zealand | 100.00 | 0.4800 | 48.00 |
| 2026-04-01T04:56:45+00:00 | BUY | New Zealand | 50.00 | 0.1711 | 8.55 |
| 2026-04-01T05:03:33+00:00 | SELL | New Zealand | 48.76 | 0.5100 | 24.87 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 3: Switzerland vs. Colombia: O/U 8.5 Total Corners
PnL $448.30 · hold 5m55s · 2B/2S · avg entry 0.3586 → exit 0.999 (spread 0.6404) · `scalp_sub_15m`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-07-07T21:58:34+00:00 | BUY | Under | 200.00 | 0.7300 | 146.00 |
| 2026-07-07T21:58:34+00:00 | BUY | Under | 500.00 | 0.2100 | 105.00 |
| 2026-07-07T22:03:43+00:00 | SELL | Under | 90.09 | 0.9990 | 90.00 |
| 2026-07-07T22:04:29+00:00 | SELL | Under | 609.90 | 0.9990 | 609.29 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 4: Argentina vs. Cabo Verde: O/U 7.5 Total Corners
PnL $319.97 · hold 14m02s · 4B/9S · avg entry 0.3364 → exit 0.94 (spread 0.6036) · `scale_in_scale_out`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-07-03T23:45:05+00:00 | BUY | Under | 296.13 | 0.3500 | 103.65 |
| 2026-07-03T23:47:32+00:00 | BUY | Under | 149.25 | 0.3500 | 52.24 |
| 2026-07-03T23:47:34+00:00 | BUY | Under | 54.62 | 0.3500 | 19.12 |
| 2026-07-03T23:48:26+00:00 | BUY | Under | 30.08 | 0.1100 | 3.31 |
| 2026-07-03T23:58:35+00:00 | SELL | Under | 29.11 | 0.9400 | 27.36 |
| 2026-07-03T23:59:04+00:00 | SELL | Under | 10.64 | 0.9400 | 10.00 |
| 2026-07-03T23:59:05+00:00 | SELL | Under | 26.04 | 0.9400 | 24.48 |
| 2026-07-03T23:59:05+00:00 | SELL | Under | 26.04 | 0.9400 | 24.48 |
| 2026-07-03T23:59:05+00:00 | SELL | Under | 17.44 | 0.9400 | 16.39 |
| 2026-07-03T23:59:05+00:00 | SELL | Under | 26.04 | 0.9400 | 24.48 |
| 2026-07-03T23:59:05+00:00 | SELL | Under | 26.04 | 0.9400 | 24.48 |
| 2026-07-03T23:59:05+00:00 | SELL | Under | 26.04 | 0.9400 | 24.48 |
| 2026-07-03T23:59:07+00:00 | SELL | Under | 342.68 | 0.9400 | 322.12 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 5: France vs. England: 1st Half O/U 4.5 Total Corners
PnL $281.86 · hold 6m34s · 3B/3S · avg entry 0.0977 → exit 0.49 (spread 0.3923) · `scale_in_scale_out`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-07-18T21:27:06+00:00 | BUY | Under | 100.00 | 0.3944 | 39.44 |
| 2026-07-18T21:29:24+00:00 | BUY | Under | 4.59 | 0.0500 | 0.23 |
| 2026-07-18T21:30:24+00:00 | BUY | Under | 617.00 | 0.0500 | 30.85 |
| 2026-07-18T21:32:52+00:00 | SELL | Under | 200.00 | 0.4900 | 98.00 |
| 2026-07-18T21:33:21+00:00 | SELL | Under | 94.96 | 0.4900 | 46.53 |
| 2026-07-18T21:33:40+00:00 | SELL | Under | 426.62 | 0.4900 | 209.04 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 6: United States vs. Belgium: O/U 11.5 Total Corners
PnL $223.86 · hold 3m35s · 1B/3S · avg entry 0.21 → exit 0.6577 (spread 0.4477) · `scalp_sub_15m`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-07-07T00:04:53+00:00 | BUY | Under | 500.00 | 0.2100 | 105.00 |
| 2026-07-07T00:06:32+00:00 | SELL | Under | 16.34 | 0.5900 | 9.64 |
| 2026-07-07T00:08:08+00:00 | SELL | Under | 59.30 | 0.6600 | 39.14 |
| 2026-07-07T00:08:28+00:00 | SELL | Under | 424.35 | 0.6600 | 280.07 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

## 8. Failure modes (do not bot these)

1. **Indian Premier League: Kolkata Knight Riders vs Sunrisers Hyderabad** -$2,394.22 · hold 3h20m · entry 0.0644 → exit 0.1802 · `market_make_both_outcomes` / `spread_harvest_sell_above_buy`
2. **Pakistan Super League: Peshawar Zalmi vs Multan Sultans** -$2,176.10 · hold 55m56s · entry 0.3853 → exit 0.4766 · `market_make_both_outcomes` / `spread_harvest_sell_above_buy`
3. **T20 Series Namibia vs Scotland: Namibia vs Scotland** -$1,272.23 · hold 21h36m · entry 0.0832 → exit 0.0294 · `market_make_both_outcomes` / `adverse_exit_sell_below_buy`
4. **Indian Premier League: Mumbai Indians vs Lucknow Super Giants** -$1,268.29 · hold 2h28m · entry 0.1078 → exit 0.0499 · `scale_in_scale_out` / `adverse_exit_sell_below_buy`
5. **T20 Challenge Trophy, Women: Rwanda vs Nepal** -$1,267.38 · hold 5h30m · entry 0.0122 → exit 0.0744 · `market_make_both_outcomes` / `spread_harvest_sell_above_buy`
6. **T20 Series Indonesia vs Sweden: Indonesia vs Sweden** -$1,100.42 · hold 4h56m · entry 0.0583 → exit 0.2307 · `scale_in_scale_out` / `spread_harvest_sell_above_buy`
7. **Indian Premier League: Chennai Super Kings vs Delhi Capitals** -$881.33 · hold 4h08m · entry 0.105 → exit 0.3447 · `scale_in_scale_out` / `spread_harvest_sell_above_buy`
8. **T20 Series Bangladesh vs Sri Lanka, Women: Bangladesh vs Sri Lanka** -$846.30 · hold 1h21m · entry 0.0077 → exit 0.0304 · `scale_in_scale_out` / `spread_harvest_sell_above_buy`
9. **Indian Premier League: Chennai Super Kings vs Kolkata Knight Riders** -$815.00 · hold 4h08m · entry 0.1135 → exit 0.1301 · `market_make_both_outcomes` / `spread_harvest_sell_above_buy`
10. **T20 Series South Africa vs. India, Women: South Africa vs India** -$729.97 · hold 1h33m · entry 0.1578 → exit 0.06 · `intraday_swing` / `adverse_exit_sell_below_buy`

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
   - default post-only bids/asks; clip $8.51
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
template: Winnertraders
mode: one_sided_live_scalper  # not classic two-sided MM
preferred_outcome_bias: Over
clip_usdc_median: 8.5113
clip_usdc_p90: 73.95
entry_price_median: 0.45
entry_price_iqr: (0.22, 0.65)
target_spread: 0.1
target_spread_p75: 0.1971
median_hold_seconds: 1481
max_hold_seconds_p75: 4461
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

_Generated 2026-08-25T16:47:01.145867+00:00_


## 8. Structured autopsy (A–G)

# Deep Trader Autopsy — Winnertraders

- Wallet: `0x13464aabec792c36b062316f474713e681330448`
- Identity: **`hybrid_liquidity_scalper`**
- Primary focus: **sports_totals**
- Span: 2026-01-16T07:37:14+00:00 → 2026-08-23T03:42:52+00:00 (218.84 days)
- Generated: 2026-08-25T16:47:01.145115+00:00

## A. Data integrity / reconciliation

| Source | PnL | Trades / notes |
|---|---:|---|
| Our cashflow realized | $16,661.90 | trades=20,475 |
| Our core cashflow | $16,180.10 | buys=11,909 sells=8,566 |
| Our closed-legs sum | -$844.29 | closed=3,001 WR=65.1% |
| Polymarket leaderboard ALL | $17,578.63 | vol=$2,032,708.12 rank=9026 |
| PolyData | $17,655.63 | trades=16162 WR=0.5926 |

- **MATCH** `polymarket_leaderboard_ALL` pnl: ours=16661.9043 ref=17578.63184561259 diff=-916.7275
- **MATCH** `polydata` realized_pnl: ours=16661.9043 ref=17655.63 diff=-993.7257
- **DRIFT** `polydata` n_trades: ours=20475 ref=16162 diff=4313
- **DRIFT** `polydata` win_rate: ours=0.6511 ref=0.5926 diff=0.0585
- **DRIFT** `internal` cashflow_vs_closed: ours=16661.9043 ref=-844.295 diff=17506.1993

## B. Core identity

- Scanner MM label: `likely_market_maker` (score 65)
- Fast round-trips (<2h) in 81% of two-sided markets
- Avg sell > avg buy in 77% of markets (spread capture)
- High-frequency cadence (median gap 100s)
- Heavy concentration in Over/Under sports totals (sports MM niche)
- Both-sides inventory: 254 markets (9.24%)
- Clip USDC median/p90/max: $6.80 / $62.50 / $2,575.00
- Sport categories: `{'sports_totals': 9253.28, 'other': 994.88, 'crypto': -294.95, 'sports_match': -10797.51}`
- Slug tokens: [('nba', 288), ('ucl', 143), ('lal', 139), ('bun', 78), ('atp', 34), ('mlb', 27), ('nhl', 26), ('ten', 21), ('wta', 11), ('mma', 5)]

### Maker vs Taker

| Leg | Maker % | Taker % | Maker fills | Taker fills |
|---|---:|---:|---:|---:|
| Entry | 62.15% | 37.85% | 8,836 | 3,073 |
| Exit | 69.16% | 30.84% | 6,640 | 1,926 |

- `enter_maker_exit_maker`: 1011
- `enter_taker_exit_maker`: 649
- `enter_maker_exit_taker`: 513
- `enter_taker_exit_taker`: 296

### Price bands

| Band | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| 0-20¢ | 748 | 51.3% | -$2,672.31 | -$3.57 |
| 20-40¢ | 671 | 58.3% | -$2,758.27 | -$4.11 |
| 40-60¢ | 639 | 70.3% | $1,638.26 | $2.56 |
| 60-80¢ | 465 | 78.2% | $117.08 | $0.25 |
| 80-100¢ | 227 | 88.1% | $2,830.94 | $12.47 |

## C. Equity & risk

- Final cashflow equity: $16,661.90
- Max drawdown: -$1,436.31 (-321.5% of peak)
- Longest drawdown: 15 days
- Daily Sharpe (ann.): 4.732
- Profit factor: 0.9845
- Top 10 winners: $8,931.07 (17.76% of win PnL)
- Top 10 losers: -$12,751.24 (24.93% of loss PnL)
- Max inventory shares: 50000.0

### Top winners
- $2,507.61 · 11h46m · Mavericks vs. Bucks: O/U 218.5
- $1,681.83 · 18h01m · ODI Series Bangladesh vs New Zealand: Bangladesh vs New Zealand
- $841.25 · 22m02s · Germany vs. Latvia: O/U 5.5
- $700.14 · 45d · Atlanta Braves vs. Chicago White Sox: O/U 8.5
- $607.74 · 15h34m · Will India win?
- $585.90 · 1m36s · Spread: Real Madrid CF (-1.5)
- $571.57 · 3h00m · T20 World Cup: Namibia vs Netherlands (Game 1)
- $551.84 · 6h42m · ODI Series New Zealand vs South Africa Women: New Zealand vs South Africa
- $448.30 · 5m55s · Switzerland vs. Colombia: O/U 8.5 Total Corners
- $434.89 · 28m26s · Team USA Stars vs. Team USA Stripes

### Top losers
- -$729.97 · 1h33m · T20 Series South Africa vs. India, Women: South Africa vs India
- -$815.00 · 4h08m · Indian Premier League: Chennai Super Kings vs Kolkata Knight Riders
- -$846.30 · 1h21m · T20 Series Bangladesh vs Sri Lanka, Women: Bangladesh vs Sri Lanka
- -$881.33 · 4h08m · Indian Premier League: Chennai Super Kings vs Delhi Capitals
- -$1,100.42 · 4h56m · T20 Series Indonesia vs Sweden: Indonesia vs Sweden
- -$1,267.38 · 5h30m · T20 Challenge Trophy, Women: Rwanda vs Nepal
- -$1,268.29 · 2h28m · Indian Premier League: Mumbai Indians vs Lucknow Super Giants
- -$1,272.23 · 21h36m · T20 Series Namibia vs Scotland: Namibia vs Scotland
- -$2,176.10 · 55m56s · Pakistan Super League: Peshawar Zalmi vs Multan Sultans
- -$2,394.22 · 3h20m · Indian Premier League: Kolkata Knight Riders vs Sunrisers Hyderabad

## D. Trade management

### Hold-time buckets

| Bucket | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| <30s | 139 | 8.0% | -$2,304.51 | -$16.58 |
| 30s-2m | 130 | 65.4% | $1,668.70 | $12.84 |
| 2-5m | 229 | 69.7% | $1,352.47 | $5.91 |
| 5-15m | 574 | 74.6% | $2,338.79 | $4.07 |
| 15m+ | 1678 | 65.8% | -$3,899.76 | -$2.32 |

- After early adverse (>2¢ vs entry within 2m): n=13, avg PnL -$21.24, median first-sell 1m32s, median hold 1m32s
- After favorable first sell (+2¢): n=1708, avg PnL $18.28, median MFE capture 1.0
- Campaigns (re-entry after flat): 546 (19.85%), avg entries 2.53, PnL $5,803.69, avg $10.63, WR 70.5%
- Single-entry: n=2204, PnL -$6,647.98, avg -$3.02
- Flatten-before-resolution flag rate: 0.9876; hold-to-resolution style n=281; redeems $1,243.87; merges $0.00
- Avg-down while MTM-red on losers: 343/960 (35.73%); Δ if skipped on those $3,205.97; global never-red-buy Δ -$5,439.60

### Family mix

| Family | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| Over/Under | 1379 | 68.7% | $9,359.87 | $6.79 |
| Other | 835 | 62.9% | -$10,758.69 | -$12.88 |
| Yes/No moneyline | 536 | 58.8% | $554.53 | $1.03 |

## E. Edge diagnosis

- Time to MFE (winners): median 18m44s, p25 6m58s, p75 55m51s, p90 2h44m
- Big MFE ≥10¢: n=998; within 30s=5; within 60s=30 (3.01% of big moves)

**Edge thesis:** Hybrid / mixed — inspect maker-taker mix, hold buckets, and redeem share above.

## F. vs polika72

| Metric | This trader | polika72 |
|---|---:|---:|
| identity | hybrid_liquidity_scalper | one_sided_informed_scalper |
| trades | 20475 | 19978 |
| cashflow_pnl | 16661.9043 | 58204.9839 |
| win_rate | 0.6511 | 0.8008 |
| entry_taker_pct | 37.85 | 61.62 |
| both_sides_rate | 0.0924 | 0.0068 |
| median_clip | 6.8027 | 11.29 |
| campaign_pct | 19.85 | 5.85 |
| max_dd | -1436.3132 | -601.1817 |
| time_to_mfe_med | 1124 | 64 |

### Steal / avoid

- **Steal:** maker-led entries (better for quoting stack on Kalshi).
- **Steal:** same-market campaign re-entry after flat.
- **Avoid:** their drawdown profile — size down vs polika72 risk.
- **Avoid:** averaging down while red.

## G. Kalshi two-sided informed MM relevance

Moderate relevance — extract risk limits and hold-time discipline; do not assume their edge transfers without Kalshi-specific microstructure testing.


## 9. Hour / DOW volume (UTC)

| Hour | USDC volume |
|---:|---:|
| 0 | 6868.62 |
| 1 | 7638.35 |
| 2 | 15030.69 |
| 3 | 15428.94 |
| 4 | 16974.96 |
| 5 | 16556.02 |
| 6 | 13498.79 |
| 7 | 20950.97 |
| 8 | 15486.7 |
| 9 | 14666.8 |
| 10 | 17538.3 |
| 11 | 16348.16 |
| 12 | 23126.22 |
| 13 | 18618.91 |
| 14 | 25012.86 |
| 15 | 29381.95 |
| 16 | 33744.67 |
| 17 | 28551.08 |
| 18 | 26564.27 |
| 19 | 28431.92 |
| 20 | 31490.49 |
| 21 | 22303.8 |
| 22 | 13254.52 |
| 23 | 6747.26 |

| DOW (0=Mon) | USDC volume |
|---:|---:|
| 0 | 55928.13 |
| 1 | 67052.49 |
| 2 | 65467.68 |
| 3 | 57346.37 |
| 4 | 61491.17 |
| 5 | 77329.65 |
| 6 | 79599.78 |

## 10. Bot schema pointer

Parse `MASTER.json` keys: `reconciliation`, `identity`, `performance`, `extras`, `copyability`, `equity_curve_daily`, `deep_dive_highlights`.
