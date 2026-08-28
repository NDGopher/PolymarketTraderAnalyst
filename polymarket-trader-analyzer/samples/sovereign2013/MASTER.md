# MASTER AUTOPSY — sovereign2013

> Single file for humans **and** bots. Machine-readable twin: `MASTER.json` · Equity: `equity_curve.csv`.

- Wallet: `0xee613b3fc183ee44f9da9c05f53e2da107e3debf`
- Generated: `2026-08-28T15:08:29.765614+00:00`
- Identity class: **`two_sided_inventory_mm`**

## 0. Executive verdict

This trader is classified as **two_sided_inventory_mm** with primary focus **sports_match**. Preferred PnL (**closed_positions_sum**) **$2,198,738.71** (leaderboard ALL $3,588,720.22; REVIEW). Unique trades **119,316**. Copy difficulty **7/10** · ease **4/10**. Needs quoting stack, inventory skew, cancel/replace; closer to classic MM.

**Exit mechanics:** `sell_secondary_market`
**Kalshi two-sided MM fit:** HIGH — closest to two-sided informed MM DNA
**Preferred PnL note:** Cashflow usually tracks leaderboard for buy+sell scalpers.

## 1. Reconciliation (mandatory)

| Source | PnL | Extra |
|---|---:|---|
| **Preferred (closed_positions_sum)** | **$2,198,738.71** | vs LB diff=-1389981.51 |
| Ours cashflow realized | -$4,392,612.28 | trades=119,316 buy_only=False |
| Ours core (ex-rebate) | -$4,392,657.34 | WR legs=51.15% |
| Ours closed-legs sum | $2,198,738.71 | PF=1.0414 |
| Polymarket leaderboard ALL | $3,588,720.22 | vol=$402,071,822.94 rank=38 |
| PolyData | $3,588,720.22 | trades=1047862 WR=0.5174 |

- DRIFT: `polymarket_leaderboard_ALL` pnl ours=2198738.7126 field=closed_positions_sum ref=3588720.2180176293 diff=-1389981.5054
- DRIFT: `polydata` realized_pnl ours=2198738.7126 field=closed_positions_sum ref=3588720.22 diff=-1389981.5074
- DRIFT: `polydata` n_trades ours=119316 field=None ref=1047862 diff=-928546
- MATCH: `polydata` win_rate ours=0.5115 field=None ref=0.5174 diff=-0.0059
- DRIFT: `internal` cashflow_vs_closed ours=-4392612.2757 field=None ref=2198738.7126 diff=-6591350.9883

## 2. Identity & microstructure

- Both-sides rate: 61.71% (5516 markets)
- Clip median/p90/max: $19.64 / $655.00 / $7,212.70
- Category PnL: `{'sports_match': 371550.43, 'sports_totals': 20617.95, 'crypto': 3.3}`
- Start BUY first: 8938 · SELL first: 0
- Entry maker/taker: 75.54% / 24.46% (106,487/12,818 fills)
- Exit maker/taker: 1.73% / 98.27% (1/10 fills)
- Patterns: `{'enter_maker_exit_taker': 4, 'enter_taker_exit_taker': 5}`

### Outcome volume (top)

| Outcome | Buy USDC | Sell USDC | Sell−Buy |
|---|---:|---:|---:|
| Under | $4,987,844.23 | $0.00 | -$4,987,844.23 |
| Over | $4,550,792.54 | $0.00 | -$4,550,792.54 |
| Lakers | $435,174.72 | $0.00 | -$435,174.72 |
| Pistons | $392,333.45 | $0.00 | -$392,333.45 |
| 76ers | $378,348.24 | $0.00 | -$378,348.24 |
| Clippers | $369,732.30 | $0.00 | -$369,732.30 |
| Raptors | $366,893.66 | $0.00 | -$366,893.66 |
| Bucks | $356,593.04 | $0.00 | -$356,593.04 |
| Thunder | $353,662.29 | $0.00 | -$353,662.29 |
| Celtics | $350,747.35 | $0.00 | -$350,747.35 |
| Cavaliers | $343,533.62 | $0.00 | -$343,533.62 |
| Mavericks | $337,941.48 | $0.00 | -$337,941.48 |

## 3. Performance metrics (kitchen sink)

- Expectancy / market: $43.89
- Avg win / avg loss: $1,645.88 / -$1,666.34 · ratio=0.9877
- PnL / day: -$38,229.87 · trades/day=1038.43 · markets/day=77.79
- PnL concentration HHI: 0.000834 (higher=more concentrated)
- Notional sum: $30,420,318.48 · median ticket $19.64
- Buy price median: 0.49 · Sell price median: 0.51
- Activity types: `{'DEPOSIT': 38, 'TRADE': 119316, 'REDEEM': 8866, 'WITHDRAWAL': 6, 'MERGE': 1900, 'REWARD': 3}`
- Open risk: `{'n': 1, 'cash_pnl': -84.45, 'current_value': 0.0, 'redeemable': 1}`

### Hold-time engine

| Bucket | N | WR | Total PnL | Avg | Median |
|---|---:|---:|---:|---:|---:|
| <30s | 1696 | 51.65% | $1,617.95 | $0.95 | $1.00 |
| 30s-2m | 90 | 57.78% | $7,188.75 | $79.88 | $10.11 |
| 2-5m | 82 | 54.32% | $8,926.03 | $108.85 | $1.75 |
| 5-15m | 205 | 45.85% | -$96,688.51 | -$471.65 | -$6.52 |
| 15m+ | 6865 | 51.69% | $471,127.45 | $68.63 | $7.50 |

### Entry price bands

| Band | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| 0-20¢ | 79 | 10.13% | -$25,220.90 | -$319.25 |
| 20-40¢ | 423 | 28.61% | $159,801.53 | $377.78 |
| 40-60¢ | 7858 | 51.22% | $133,059.22 | $16.93 |
| 60-80¢ | 434 | 78.11% | $100,054.11 | $230.54 |
| 80-100¢ | 144 | 84.72% | $24,477.71 | $169.98 |

### Family

| Family | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| Other | 5059 | 51.79% | $277,429.20 | $54.84 |
| Over/Under | 3875 | 51.41% | $114,731.37 | $29.61 |
| Yes/No moneyline | 4 | 75.00% | $11.10 | $2.78 |

## 4. Equity curve (critical)

### 4a. Cashflow activity equity

- Final equity (cashflow): **$364,775.31**
- Max DD: **-$808,384.30** (-65700.37% of peak)
- Longest DD: **0 days**
- Daily Sharpe (ann.): **0.449**
- Days: 80

Files: `equity_curve.csv` · `equity_curve.json` (source=`cashflow_activity`)

<details><summary>Daily cashflow equity table (full)</summary>

| Date | Equity | Daily PnL | Drawdown |
|---|---:|---:|---:|
| 2025-07-25 | 0.00 | 0.00 | 0.00 |
| 2025-08-07 | -36.75 | -36.75 | -36.75 |
| 2025-08-08 | -17.96 | 18.79 | -17.96 |
| 2025-08-11 | -7.96 | 10.00 | -7.96 |
| 2025-08-12 | -8.77 | -0.81 | -8.77 |
| 2025-08-13 | -25.77 | -17.00 | -25.77 |
| 2025-08-20 | -74.27 | -48.50 | -74.27 |
| 2025-08-21 | -62.37 | 11.90 | -62.37 |
| 2025-08-29 | -62.37 | 0.00 | -62.37 |
| 2025-09-09 | -867.86 | -805.50 | -867.86 |
| 2025-09-10 | -3873.78 | -3005.91 | -3873.78 |
| 2025-09-11 | -6244.12 | -2370.34 | -6244.12 |
| 2025-09-12 | 865.92 | 7110.04 | 0.00 |
| 2025-09-16 | 827.84 | -38.08 | -38.08 |
| 2025-09-17 | 837.84 | 10.00 | -28.08 |
| 2025-09-19 | 819.08 | -18.76 | -46.84 |
| 2025-09-25 | -4176.80 | -4995.88 | -5042.73 |
| 2025-09-26 | -9779.47 | -5602.67 | -10645.40 |
| 2025-09-27 | -17605.51 | -7826.04 | -18471.43 |
| 2025-09-28 | -18636.26 | -1030.75 | -19502.18 |
| 2025-10-01 | 1096.32 | 19732.58 | 0.00 |
| 2025-10-02 | 1046.32 | -50.00 | -50.00 |
| 2025-10-03 | 276.49 | -769.83 | -819.83 |
| 2025-10-05 | -82.18 | -358.67 | -1178.50 |
| 2025-10-06 | 362.75 | 444.93 | -733.57 |
| 2025-10-07 | -4124.70 | -4487.45 | -5221.02 |
| 2025-10-08 | -57847.96 | -53723.26 | -58944.28 |
| 2025-10-09 | -120004.70 | -62156.74 | -121101.02 |
| 2025-10-10 | -65512.08 | 54492.62 | -66608.40 |
| 2025-10-11 | -195022.33 | -129510.25 | -196118.65 |
| 2025-10-12 | -21734.15 | 173288.18 | -22830.47 |
| 2025-10-13 | -179092.07 | -157357.92 | -180188.39 |
| 2025-10-14 | -391645.69 | -212553.62 | -392742.01 |
| 2025-10-15 | -196470.00 | 195175.69 | -197566.32 |
| 2025-10-16 | -243916.45 | -47446.45 | -245012.77 |
| 2025-10-17 | -119993.03 | 123923.42 | -121089.35 |
| 2025-10-18 | -442205.39 | -322212.35 | -443301.71 |
| 2025-10-19 | -82633.10 | 359572.28 | -83729.42 |
| 2025-10-20 | -56229.37 | 26403.73 | -57325.69 |
| 2025-10-21 | -116256.13 | -60026.76 | -117352.45 |
| 2025-10-22 | -164067.83 | -47811.70 | -165164.15 |
| 2025-10-23 | -109870.65 | 54197.18 | -110966.97 |
| 2025-10-24 | -276346.35 | -166475.70 | -277442.67 |
| 2025-10-25 | -196771.48 | 79574.87 | -197867.80 |
| 2025-10-26 | -217565.27 | -20793.79 | -218661.59 |
| 2025-10-27 | -214027.77 | 3537.50 | -215124.10 |
| 2025-10-28 | -107089.16 | 106938.61 | -108185.48 |
| 2025-10-29 | -200884.97 | -93795.81 | -201981.30 |
| 2025-10-30 | -224959.55 | -24074.58 | -226055.87 |
| 2025-10-31 | -331989.96 | -107030.41 | -333086.28 |
| 2025-11-01 | -391654.05 | -59664.10 | -392750.38 |
| 2025-11-02 | -329665.10 | 61988.96 | -330761.42 |
| 2025-11-03 | -16925.87 | 312739.23 | -18022.19 |
| 2025-11-04 | -222636.54 | -205710.67 | -223732.86 |
| 2025-11-05 | -353260.81 | -130624.27 | -354357.13 |
| 2025-11-06 | -7418.94 | 345841.88 | -8515.26 |
| 2025-11-07 | -184098.06 | -176679.13 | -185194.38 |
| 2025-11-08 | -719190.65 | -535092.58 | -720286.97 |
| 2025-11-09 | -140257.66 | 578932.99 | -141353.98 |
| 2025-11-10 | 19806.57 | 160064.23 | 0.00 |
| 2025-11-11 | -10012.75 | -29819.32 | -29819.32 |
| 2025-11-12 | -273402.78 | -263390.03 | -293209.35 |
| 2025-11-13 | -25935.17 | 247467.61 | -45741.74 |
| 2025-11-14 | -11875.49 | 14059.68 | -31682.06 |
| 2025-11-15 | -468025.18 | -456149.70 | -487831.76 |
| 2025-11-16 | -92020.48 | 376004.71 | -111827.05 |
| 2025-11-17 | 14708.56 | 106729.03 | -5098.02 |
| 2025-11-18 | 76956.35 | 62247.79 | 0.00 |
| 2025-11-19 | 29098.34 | -47858.01 | -47858.01 |
| 2025-11-20 | 313822.30 | 284723.95 | 0.00 |
| 2025-11-21 | 97527.15 | -216295.15 | -216295.15 |
| 2025-11-22 | -494562.00 | -592089.15 | -808384.30 |
| 2025-11-23 | -343556.47 | 151005.54 | -657378.76 |
| 2025-11-24 | -192379.95 | 151176.52 | -506202.25 |
| 2025-11-25 | 61409.63 | 253789.58 | -252412.67 |
| 2025-11-26 | -63275.91 | -124685.54 | -377098.21 |
| 2025-11-27 | 314981.70 | 378257.61 | 0.00 |
| 2025-11-28 | 115.83 | -314865.87 | -314865.87 |
| 2025-11-29 | -84183.62 | -84299.44 | -399165.32 |
| 2025-11-30 | 364775.31 | 448958.93 | 0.00 |

</details>

### 4b. Closed-positions equity (alt — critical for buy-only books)

- Final closed equity: **$2,198,738.71**
- Max DD: **-$1,476,686.34**
- Daily Sharpe (ann.): **1.646**
- Days: 218

Files: `equity_curve_closed.csv` · `equity_curve_closed.json` (source=`closed_positions`)

<details><summary>Daily closed equity table (full)</summary>

| Date | Equity | Daily PnL | Drawdown |
|---|---:|---:|---:|
| 2025-08-07 | 0.60 | 0.60 | 0.00 |
| 2025-08-08 | 5.93 | 5.33 | 0.00 |
| 2025-08-09 | -7.96 | -13.89 | -13.89 |
| 2025-08-13 | -7.47 | 0.49 | -13.40 |
| 2025-08-14 | -24.47 | -17.00 | -30.40 |
| 2025-08-20 | -52.49 | -28.02 | -58.41 |
| 2025-08-21 | -62.37 | -9.88 | -68.29 |
| 2025-09-10 | 71.62 | 133.99 | 0.00 |
| 2025-09-11 | 1158.59 | 1086.97 | 0.00 |
| 2025-09-12 | 876.31 | -282.28 | -282.28 |
| 2025-09-13 | 876.36 | 0.05 | -282.23 |
| 2025-09-16 | 890.96 | 14.60 | -267.63 |
| 2025-09-17 | 897.86 | 6.90 | -260.73 |
| 2025-09-20 | 888.86 | -9.00 | -269.73 |
| 2025-09-21 | 895.10 | 6.24 | -263.49 |
| 2025-09-25 | 1513.22 | 618.12 | 0.00 |
| 2025-09-26 | 1081.77 | -431.46 | -431.46 |
| 2025-09-27 | 648.30 | -433.46 | -864.92 |
| 2025-09-28 | 911.58 | 263.27 | -601.64 |
| 2025-09-29 | 1142.05 | 230.47 | -371.18 |
| 2025-10-03 | 1091.10 | -50.95 | -422.12 |
| 2025-10-04 | 778.52 | -312.58 | -734.70 |
| 2025-10-05 | 685.10 | -93.42 | -828.12 |
| 2025-10-06 | 564.57 | -120.53 | -948.65 |
| 2025-10-07 | 360.46 | -204.11 | -1152.76 |
| 2025-10-08 | -1948.22 | -2308.69 | -3461.45 |
| 2025-10-09 | -8316.23 | -6368.00 | -9829.45 |
| 2025-10-10 | 34969.93 | 43286.15 | 0.00 |
| 2025-10-11 | 17389.38 | -17580.54 | -17580.54 |
| 2025-10-12 | 54974.61 | 37585.22 | 0.00 |
| 2025-10-13 | 67777.13 | 12802.53 | 0.00 |
| 2025-10-14 | 28833.91 | -38943.22 | -38943.22 |
| 2025-10-15 | 37569.71 | 8735.80 | -30207.43 |
| 2025-10-16 | 32089.72 | -5479.98 | -35687.41 |
| 2025-10-17 | 12878.18 | -19211.55 | -54898.96 |
| 2025-10-18 | 17390.70 | 4512.53 | -50386.43 |
| 2025-10-19 | 26867.93 | 9477.23 | -40909.20 |
| 2025-10-20 | 39531.41 | 12663.48 | -28245.72 |
| 2025-10-21 | 49310.28 | 9778.87 | -18466.85 |
| 2025-10-22 | 48020.35 | -1289.93 | -19756.78 |
| 2025-10-23 | 66455.27 | 18434.91 | -1321.87 |
| 2025-10-24 | 78018.94 | 11563.67 | 0.00 |
| 2025-10-25 | 97079.41 | 19060.47 | 0.00 |
| 2025-10-26 | 111415.96 | 14336.55 | 0.00 |
| 2025-10-27 | 131806.49 | 20390.54 | 0.00 |
| 2025-10-28 | 152495.72 | 20689.23 | 0.00 |
| 2025-10-29 | 153181.81 | 686.10 | 0.00 |
| 2025-10-30 | 114499.05 | -38682.77 | -38682.77 |
| 2025-10-31 | 125409.06 | 10910.01 | -27772.76 |
| 2025-11-01 | 219123.99 | 93714.94 | 0.00 |
| 2025-11-02 | 160724.06 | -58399.94 | -58399.94 |
| 2025-11-03 | 324489.35 | 163765.29 | 0.00 |
| 2025-11-04 | 281217.83 | -43271.52 | -43271.52 |
| 2025-11-05 | 224018.57 | -57199.26 | -100470.78 |
| 2025-11-06 | 163955.48 | -60063.09 | -160533.86 |
| 2025-11-07 | 250665.57 | 86710.09 | -73823.78 |
| 2025-11-08 | 284038.30 | 33372.74 | -40451.04 |
| 2025-11-09 | 422725.17 | 138686.87 | 0.00 |
| 2025-11-10 | 423619.48 | 894.31 | 0.00 |
| 2025-11-11 | 346601.36 | -77018.12 | -77018.12 |
| 2025-11-12 | 357470.27 | 10868.92 | -66149.21 |
| 2025-11-13 | 308348.42 | -49121.85 | -115271.06 |
| 2025-11-14 | 284463.00 | -23885.42 | -139156.48 |
| 2025-11-15 | 365500.09 | 81037.09 | -58119.39 |
| 2025-11-16 | 373458.79 | 7958.70 | -50160.69 |
| 2025-11-17 | 322154.47 | -51304.31 | -101465.01 |
| 2025-11-18 | 291250.73 | -30903.74 | -132368.75 |
| 2025-11-19 | 338491.11 | 47240.38 | -85128.37 |
| 2025-11-20 | 526690.47 | 188199.36 | 0.00 |
| 2025-11-21 | 488790.38 | -37900.09 | -37900.09 |
| 2025-11-22 | 132902.66 | -355887.73 | -393787.82 |
| 2025-11-23 | 134905.14 | 2002.48 | -391785.34 |
| 2025-11-24 | 256133.15 | 121228.01 | -270557.32 |
| 2025-11-25 | 325633.32 | 69500.16 | -201057.16 |
| 2025-11-26 | 272209.97 | -53423.35 | -254480.51 |
| 2025-11-27 | 389705.18 | 117495.21 | -136985.30 |
| 2025-11-28 | 428031.32 | 38326.14 | -98659.16 |
| 2025-11-29 | 446501.79 | 18470.47 | -80188.69 |
| 2025-11-30 | 428083.62 | -18418.17 | -98606.85 |
| 2025-12-01 | 380041.69 | -48041.93 | -146648.78 |
| 2025-12-02 | 465771.45 | 85729.76 | -60919.02 |
| 2025-12-03 | 455868.16 | -9903.29 | -70822.32 |
| 2025-12-04 | 492100.36 | 36232.20 | -34590.12 |
| 2025-12-05 | 564353.47 | 72253.11 | 0.00 |
| 2025-12-06 | 554657.86 | -9695.61 | -9695.61 |
| 2025-12-07 | 538566.63 | -16091.23 | -25786.84 |
| 2025-12-08 | 534227.41 | -4339.22 | -30126.06 |
| 2025-12-09 | 430659.35 | -103568.06 | -133694.12 |
| 2025-12-10 | 418317.08 | -12342.27 | -146036.38 |
| 2025-12-11 | 438142.47 | 19825.38 | -126211.00 |
| 2025-12-12 | 397984.49 | -40157.98 | -166368.98 |
| 2025-12-13 | 391317.80 | -6666.70 | -173035.67 |
| 2025-12-14 | 495087.02 | 103769.22 | -69266.45 |
| 2025-12-15 | 442368.18 | -52718.84 | -121985.29 |
| 2025-12-16 | 399353.33 | -43014.85 | -165000.14 |
| 2025-12-17 | 378809.54 | -20543.80 | -185543.93 |
| 2025-12-18 | 346800.80 | -32008.74 | -217552.67 |
| 2025-12-19 | 334081.06 | -12719.74 | -230272.40 |
| 2025-12-20 | 327840.24 | -6240.82 | -236513.23 |
| 2025-12-21 | 389064.38 | 61224.14 | -175289.09 |
| 2025-12-22 | 359562.59 | -29501.79 | -204790.88 |
| 2025-12-23 | 309630.72 | -49931.87 | -254722.75 |
| 2025-12-24 | 228190.52 | -81440.20 | -336162.94 |
| 2025-12-25 | 251838.01 | 23647.49 | -312515.46 |
| 2025-12-26 | 325168.43 | 73330.42 | -239185.04 |
| 2025-12-27 | 441217.03 | 116048.60 | -123136.44 |
| 2025-12-28 | 511816.36 | 70599.33 | -52537.11 |
| 2025-12-29 | 617270.32 | 105453.96 | 0.00 |
| 2025-12-30 | 720621.99 | 103351.67 | 0.00 |
| 2025-12-31 | 648560.02 | -72061.97 | -72061.97 |
| 2026-01-01 | 699659.47 | 51099.44 | -20962.52 |
| 2026-01-02 | 748053.13 | 48393.67 | 0.00 |
| 2026-01-03 | 775166.89 | 27113.76 | 0.00 |
| 2026-01-04 | 751315.23 | -23851.66 | -23851.66 |
| 2026-01-05 | 749418.84 | -1896.39 | -25748.05 |
| 2026-01-06 | 694752.30 | -54666.54 | -80414.59 |
| 2026-01-07 | 657777.00 | -36975.30 | -117389.90 |
| 2026-01-08 | 705685.36 | 47908.36 | -69481.53 |
| 2026-01-09 | 659700.52 | -45984.84 | -115466.37 |
| 2026-01-10 | 802264.59 | 142564.06 | 0.00 |
| 2026-01-11 | 934848.60 | 132584.01 | 0.00 |
| 2026-01-12 | 952942.45 | 18093.85 | 0.00 |
| 2026-01-13 | 982784.99 | 29842.54 | 0.00 |
| 2026-01-14 | 1076980.82 | 94195.84 | 0.00 |
| 2026-01-15 | 1121778.02 | 44797.20 | 0.00 |
| 2026-01-16 | 1165753.95 | 43975.93 | 0.00 |
| 2026-01-17 | 1255153.03 | 89399.08 | 0.00 |
| 2026-01-18 | 1269896.23 | 14743.20 | 0.00 |
| 2026-01-19 | 1321373.05 | 51476.81 | 0.00 |
| 2026-01-20 | 1319942.59 | -1430.46 | -1430.46 |
| 2026-01-21 | 1222541.82 | -97400.77 | -98831.23 |
| 2026-01-22 | 1386946.81 | 164404.99 | 0.00 |
| 2026-01-23 | 1317678.52 | -69268.29 | -69268.29 |
| 2026-01-24 | 1081598.35 | -236080.17 | -305348.46 |
| 2026-01-25 | 1299879.59 | 218281.24 | -87067.22 |
| 2026-01-26 | 1288738.32 | -11141.28 | -98208.49 |
| 2026-01-27 | 1395218.98 | 106480.67 | 0.00 |
| 2026-01-28 | 1360549.14 | -34669.85 | -34669.85 |
| 2026-01-29 | 1405968.41 | 45419.27 | 0.00 |
| 2026-01-30 | 1411667.39 | 5698.99 | 0.00 |
| 2026-01-31 | 1344146.18 | -67521.21 | -67521.21 |
| 2026-02-01 | 1368530.22 | 24384.04 | -43137.17 |
| 2026-02-02 | 1470447.67 | 101917.45 | 0.00 |
| 2026-02-03 | 1492527.58 | 22079.91 | 0.00 |
| 2026-02-04 | 1633522.27 | 140994.69 | 0.00 |
| 2026-02-05 | 1567865.25 | -65657.02 | -65657.02 |
| 2026-02-06 | 1672687.24 | 104821.99 | 0.00 |
| 2026-02-07 | 1710985.03 | 38297.78 | 0.00 |
| 2026-02-08 | 1991311.27 | 280326.24 | 0.00 |
| 2026-02-09 | 2014190.42 | 22879.15 | 0.00 |
| 2026-02-10 | 1903699.58 | -110490.84 | -110490.84 |
| 2026-02-11 | 1687763.95 | -215935.63 | -326426.47 |
| 2026-02-12 | 1614477.11 | -73286.84 | -399713.31 |
| 2026-02-13 | 1572933.59 | -41543.52 | -441256.83 |
| 2026-02-14 | 1533171.15 | -39762.43 | -481019.27 |
| 2026-02-15 | 1562207.18 | 29036.02 | -451983.24 |
| 2026-02-16 | 1597239.29 | 35032.12 | -416951.13 |
| 2026-02-17 | 1527010.71 | -70228.58 | -487179.71 |
| 2026-02-18 | 1537374.86 | 10364.16 | -476815.56 |
| 2026-02-19 | 1466411.64 | -70963.23 | -547778.78 |
| 2026-02-20 | 1573500.58 | 107088.94 | -440689.84 |
| 2026-02-21 | 1620857.85 | 47357.27 | -393332.57 |
| 2026-02-22 | 1509968.25 | -110889.60 | -504222.17 |
| 2026-02-23 | 1526397.21 | 16428.95 | -487793.21 |
| 2026-02-24 | 1533293.36 | 6896.16 | -480897.06 |
| 2026-02-25 | 1512356.58 | -20936.79 | -501833.84 |
| 2026-02-26 | 1510650.30 | -1706.28 | -503540.12 |
| 2026-02-27 | 1519120.10 | 8469.80 | -495070.32 |
| 2026-03-02 | 1520173.50 | 1053.40 | -494016.92 |
| 2026-03-03 | 1626094.62 | 105921.11 | -388095.80 |
| 2026-03-04 | 1659580.79 | 33486.17 | -354609.63 |
| 2026-03-05 | 1725613.78 | 66032.99 | -288576.64 |
| 2026-03-06 | 1694695.48 | -30918.29 | -319494.94 |
| 2026-03-07 | 1762760.89 | 68065.40 | -251429.54 |
| 2026-03-08 | 1666262.02 | -96498.87 | -347928.40 |
| 2026-03-09 | 1643094.92 | -23167.10 | -371095.50 |
| 2026-03-10 | 1769482.35 | 126387.43 | -244708.07 |
| 2026-03-11 | 1800637.64 | 31155.30 | -213552.78 |
| 2026-03-12 | 1708200.22 | -92437.42 | -305990.20 |
| 2026-03-13 | 1612682.28 | -95517.94 | -401508.14 |
| 2026-03-14 | 1763370.69 | 150688.42 | -250819.73 |
| 2026-03-15 | 1852504.06 | 89133.36 | -161686.36 |
| 2026-03-16 | 1831399.03 | -21105.02 | -182791.39 |
| 2026-03-17 | 1927381.50 | 95982.46 | -86808.92 |
| 2026-03-18 | 2008416.52 | 81035.02 | -5773.90 |
| 2026-03-19 | 2165122.35 | 156705.83 | 0.00 |
| 2026-03-20 | 2227753.84 | 62631.49 | 0.00 |
| 2026-03-21 | 2180693.06 | -47060.78 | -47060.78 |
| 2026-03-22 | 2025517.68 | -155175.38 | -202236.16 |
| 2026-03-23 | 3164120.12 | 1138602.44 | 0.00 |
| 2026-03-24 | 3161265.18 | -2854.94 | -2854.94 |
| 2026-03-25 | 3209515.39 | 48250.21 | 0.00 |
| 2026-03-28 | 3402596.36 | 193080.97 | 0.00 |
| 2026-04-01 | 3514887.18 | 112290.82 | 0.00 |
| 2026-04-02 | 3372171.60 | -142715.58 | -142715.58 |
| 2026-04-03 | 3624770.48 | 252598.88 | 0.00 |
| 2026-04-04 | 3455707.41 | -169063.07 | -169063.07 |
| 2026-04-05 | 3239098.28 | -216609.12 | -385672.19 |
| 2026-04-06 | 3278033.00 | 38934.72 | -346737.47 |
| 2026-04-07 | 3242082.28 | -35950.73 | -382688.20 |
| 2026-04-08 | 3132532.50 | -109549.77 | -492237.98 |
| 2026-04-09 | 2959478.61 | -173053.89 | -665291.86 |
| 2026-04-10 | 2381687.74 | -577790.87 | -1243082.73 |
| 2026-04-11 | 2431448.60 | 49760.85 | -1193321.88 |
| 2026-04-12 | 2348834.96 | -82613.64 | -1275935.52 |
| 2026-04-13 | 2307201.98 | -41632.98 | -1317568.50 |
| 2026-04-14 | 2344054.90 | 36852.92 | -1280715.57 |
| 2026-04-15 | 2187034.03 | -157020.88 | -1437736.45 |
| 2026-04-16 | 2267238.54 | 80204.51 | -1357531.94 |
| 2026-04-17 | 2205273.67 | -61964.87 | -1419496.81 |
| 2026-04-18 | 2159257.31 | -46016.35 | -1465513.16 |
| 2026-04-19 | 2148084.14 | -11173.18 | -1476686.34 |
| 2026-04-20 | 2175295.61 | 27211.48 | -1449474.86 |
| 2026-04-21 | 2224263.68 | 48968.07 | -1400506.79 |
| 2026-04-22 | 2250938.12 | 26674.43 | -1373832.36 |
| 2026-04-23 | 2173454.70 | -77483.41 | -1451315.77 |
| 2026-04-24 | 2198775.03 | 25320.32 | -1425995.45 |
| 2026-04-30 | 2198738.71 | -36.31 | -1426031.77 |

</details>

### Top winners / losers contribution

Top10 winners $600,512.29 (7.91% of wins) · Top10 losers -$543,562.91 (7.55% of losses) · PF=1.0414

- WIN $113,953.16 · 40666s · Spread: Utah State Aggies (-10.5)
- WIN $85,597.66 · 34546s · Tulane vs. Temple
- WIN $71,389.74 · 19372s · Heat vs. Lakers: O/U 232.5
- WIN $64,009.54 · 74775s · Nuggets vs. Trail Blazers
- WIN $54,499.31 · 60250s · Spread: Broncos (-8.5)
- WIN $45,994.41 · 23852s · Spread: Knicks (-8.5)
- WIN $45,108.24 · 68322s · Buccaneers vs. Rams: O/U 49.5
- WIN $43,701.95 · 30179s · Texas State vs. Southern Miss
- WIN $38,261.32 · 39816s · Hawks vs. Cavaliers: O/U 231.5
- WIN $37,996.97 · 62638s · Spread: Central Michigan (-9.5)

- LOSS -$30,622.12 · 20428s · UAB Blazers vs. Rice
- LOSS -$36,742.02 · 74322s · Nets vs. Celtics
- LOSS -$36,894.01 · 50310s · Missouri vs. Oklahoma
- LOSS -$37,034.38 · 27094s · Chiefs vs. Bills: O/U 50.5
- LOSS -$51,257.30 · 4532s · Army vs. Air Force
- LOSS -$55,214.96 · 76832s · Bills vs. Texans: O/U 44.5
- LOSS -$55,520.54 · 73382s · Spread: Rockets (-7.5)
- LOSS -$70,979.38 · 57132s · Spread: Florida State (-6.5)
- LOSS -$70,992.09 · 2798s · Spread: Thunder (-8.5)
- LOSS -$98,306.11 · 386s · Spread: Virginia Cavaliers (-3.5)

## 5. Trade management deep dive

- Adverse early (>2¢): `{'n_early_adverse': 0, 'avg_pnl': None, 'median_t_first_sell': None, 'median_hold': None}`
- Favorable first-sell: `{'n_first_sell_up_2c': 0, 'avg_pnl': None, 'median_mfe_capture': 1.0, 'mean_mfe_capture': 1.0}`
- Campaigns: `{'n': 4, 'pct': 0.04, 'avg_entries': 2.25, 'pnl': 5.1, 'avg_pnl': 1.27, 'win_rate': 0.75, 'single_n': 8934, 'single_pnl': 392166.58, 'single_avg_pnl': 43.9}`
- Avg-down: `{'n_losers': 4322, 'n_losers_with_red_buys': 2166, 'pct_losers': 50.12, 'total_delta_if_skipped_on_losers': 0.0, 'global_fifo_sim': -1.13, 'global_fifo_never_red_buy': -1.08, 'global_delta': 0.05}`
- Resolution behavior: `{'flattened_before_flag_rate': 0.948, 'hold_to_resolution_style_n': 8929, 'redeems_usdc': 26027412.51340092, 'merges_usdc': 4757387.59}`
- Latency: `{'time_to_mfe_median': 47346, 'time_to_mfe_p25': None, 'time_to_mfe_p75': None, 'time_to_mfe_p90': 47346, 'mfe_ge_10c_n': 0, 'mfe_ge_10c_within_30s': 0, 'mfe_ge_10c_within_60s': 0, 'pct_big_within_60s': 0.0}`

### What works / fails
- WORKS: Winners capture median spread -0.0037 vs losers -0.01
- WORKS: Both-sides inventory on 61.3% of winning markets (losers 62.2%)
- WORKS: Hold bucket <5m: avg PnL $9.49 on 1868 markets (WR 52%)
- WORKS: Hold bucket 2-12h: avg PnL $176.70 on 3155 markets (WR 52%)
- WORKS: Entry band 0.20-0.40: avg $375.85 across 425 markets
- WORKS: Entry band 0.40-0.60: avg $16.95 across 7856 markets
- WORKS: Entry band 0.60-0.80: avg $230.54 across 434 markets
- WORKS: Entry band 0.80-1.00: avg $169.98 across 144 markets
- WORKS: Buy-ladder behavior: fade-into-weakness markets=1727, chase-up markets=1672
- FAILS: Hold bucket 5-30m: avg PnL $-154.58 on 408 markets
- FAILS: Hold bucket 30m-2h: avg PnL $-47.81 on 807 markets
- FAILS: Hold bucket 12h+: avg PnL $-30.15 on 2700 markets
- FAILS: Entry band 0.00-0.20: avg $-319.25 across 79 markets — avoid or tighten risk

## 6. Strategy overview (in depth)

# Strategy Dossier: sovereign2013

- **Wallet:** `0xee613b3fc183ee44f9da9c05f53e2da107e3debf`
- **History span:** 2025-08-07T14:54:45+00:00 → 2025-11-30T12:27:58+00:00 (114.9 days)
- **Trades:** 119,316 (buys 119,305 / sells 11)
- **Markets touched:** 8,938
- **Closed positions:** 71,299

## Headline performance

| Metric | Value |
|---|---|
| Realized cashflow (sells − buys + redeems + rebates) | -$4,392,612.28 |
| Core cashflow (ex-rebates) | -$4,392,657.34 |
| Closed-positions realized sum | $2,198,738.71 |
| Win rate (closed) | 51.15% (36470W / 34826L) |
| Profit factor | 1.0414 |
| Gross wins / losses | $55,310,486.44 / -$53,111,747.73 |
| Equity max drawdown | -$1,069,973.31 |
| Polymarket leaderboard (ALL) | $3,588,720.22 PnL · vol $402,071,822.94 · rank 38 |

## Source validation

- **DRIFT** `polymarket_leaderboard_ALL` pnl: ours=2198738.7126 ref=3588720.2180176293 diff=-1389981.5054
- **DRIFT** `polydata` realized_pnl: ours=2198738.7126 ref=3588720.22 diff=-1389981.5074
- **DRIFT** `polydata` n_trades: ours=119316 ref=1047862 diff=-928546
- **MATCH** `polydata` win_rate: ours=0.5115 ref=0.5174 diff=-0.0059
- **DRIFT** `internal` cashflow_vs_closed: ours=-4392612.2757 ref=2198738.7126 diff=-6591350.9883

## What kind of trader is this?

**Classification:** `likely_market_maker` (score 65/100)

- Trades both outcomes in 62% of markets (inventory/MM signature)
- Fast round-trips (<2h) in 56% of two-sided markets
- High-frequency cadence (median gap 16s)
- Heavy concentration in Over/Under sports totals (sports MM niche)

Supporting rates — both-sides markets: 0.6171, fast round-trips: 0.5556, spread-capture rate: 0.3333.

## Exact edge thesis

sovereign2013 primarily monetizes **liquidity / short-horizon mean reversion on sports markets**, not long-shot directional political bets. The tape shows repeated buy-then-sell with average exit price above average entry — the classic scalper / spread fingerprint.

See `bot_playbook.md` for the full entry/management/exit autopsy and bot architecture.

## Where the money comes from

- **sports_match**: $1,451,954.61 across 39774 closed legs
- **sports_totals**: $722,608.02 across 31519 closed legs
- **other**: $24,172.77 across 1 closed legs
- **crypto**: $3.30 across 5 closed legs

## Timing

- Peak UTC hours: 15, 16, 14, 23, 17
- Peak weekdays (0=Mon): [5, 2, 4]
- Median inter-trade gap: 16s

## Sizing

- Median ticket $19.64, mean $254.96, p90 $655.00, max $7,212.70
- Share size median 42.9375, mean 515.6948

## Trade-by-trade pattern (representative winners)

These vignettes are reconstructed from fills: average entry, average exit, hold time, and closed realized PnL.

## Top closed winners / losers

**Winners**
- Spread: Utah State Aggies (-10.5): $113,953.16 · bought $77,395.51 · sold $0.00 · hold 11h 17m
- Tulane vs. Temple: $85,597.66 · bought $95,327.85 · sold $0.00 · hold 9h 35m
- Heat vs. Lakers: O/U 232.5: $71,389.74 · bought $65,817.70 · sold $0.00 · hold 5h 22m
- Nuggets vs. Trail Blazers: $64,009.54 · bought $35,456.91 · sold $0.00 · hold 20h 46m
- Spread: Broncos (-8.5): $54,499.31 · bought $82,727.50 · sold $0.00 · hold 16h 44m
- Spread: Knicks (-8.5): $45,994.41 · bought $43,423.12 · sold $0.00 · hold 6h 37m
- Buccaneers vs. Rams: O/U 49.5: $45,108.24 · bought $39,814.99 · sold $0.00 · hold 18h 58m
- Texas State vs. Southern Miss: $43,701.95 · bought $28,673.72 · sold $0.00 · hold 8h 22m
- Hawks vs. Cavaliers: O/U 231.5: $38,261.32 · bought $39,404.98 · sold $0.00 · hold 11h 3m
- Spread: Central Michigan (-9.5): $37,996.97 · bought $32,551.07 · sold $0.00 · hold 17h 23m

**Losers**
- Spread: Virginia Cavaliers (-3.5): -$98,306.11 · bought $112,210.33 · sold $0.00
- Spread: Thunder (-8.5): -$70,992.09 · bought $100,087.15 · sold $0.00
- Spread: Florida State (-6.5): -$70,979.38 · bought $126,011.56 · sold $0.00
- Spread: Rockets (-7.5): -$55,520.54 · bought $61,039.67 · sold $0.00
- Bills vs. Texans: O/U 44.5: -$55,214.96 · bought $59,207.38 · sold $0.00
- Army vs. Air Force: -$51,257.30 · bought $51,257.99 · sold $0.00
- Chiefs vs. Bills: O/U 50.5: -$37,034.38 · bought $39,260.72 · sold $0.00
- Missouri vs. Oklahoma: -$36,894.01 · bought $73,553.95 · sold $0.00
- Nets vs. Celtics: -$36,742.02 · bought $48,757.89 · sold $0.00
- UAB Blazers vs. Rice: -$30,622.12 · bought $52,247.43 · sold $0.00

## Replication playbook (how to copy the edge)

1. **Universe:** Focus on liquid sports match + totals (O/U) markets with tight books.
2. **Role:** Quote or take both sides near mid; prioritize markets you can exit before resolution.
3. **Sizing:** Start near their median ticket (~$19.64) and scale only with inventory limits.
4. **Inventory:** Cap net Yes/No (or Over/Under) imbalance; flatten when mid moves through you.
5. **Hold time:** Target minutes–hours, not overnight directional risk, unless hedged via opposite outcome.
6. **Edge source:** Capture spread + mean reversion after flow, not oracle forecasting alpha.
7. **Ops:** Automate via CLOB maker orders; track maker rebates; kill-switch on drawdown.
8. **Do not blindly copy:** Their edge depends on latency, fee tier, and bankroll. Replicate *mechanics*, not wallet follows.

## Cashflow anatomy

- Buys: $30,420,194.16
- Sells: $124.31
- Redeems: $26,027,412.51
- Maker rebates: $0.00
- Taker rebates: $0.00

_Generated 2026-08-28T15:08:28.306606+00:00_


## 7. Bot / copy playbook

- Difficulty: **7/10** · Ease: **4/10**
- Why: Needs quoting stack, inventory skew, cancel/replace; closer to classic MM.

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
- Prioritize hold bucket 15m+ (their PnL engine)

### Avoid
- Averaging down while red on losers
- Their raw size/drawdown — scale down hard

Bot parameters: `{'preferred_entry_price_median': 0.4981, 'preferred_entry_price_p25_p75': (0.4798, 0.53), 'target_spread_median': -0.0037, 'target_spread_p75': 0.0706, 'max_hold_seconds_p75': 50074, 'median_hold_seconds': 20795, 'clip_size_usdc_median': 20.3077, 'clip_size_usdc_p90': 634.25, 'both_sides_on_winners_rate': 0.6131, 'require_exit_above_entry': True, 'flatten_before_resolution': True, 'maker_bias': False}`

# Elite Replication Playbook — sovereign2013

Wallet `0xee613b3fc183ee44f9da9c05f53e2da107e3debf`. Reverse-engineered from the **full unique fill tape** (119,316 trades · 8,938 markets). This is an implementation spec for a high-end bot, not vibes.

## 0. True strategy identity (read this first)

Classification `likely_market_maker` — mix of spread capture and directional inventory.

Heuristic label from the scanner may still say `likely_market_maker` because of fast round-trips + sell>buy + maker rebates. **Operationally, build a live scalper with optional maker quoting**, not a Yes/No pair inventory bot.

## 1. Performance anchors

| Source / metric | Value |
|---|---|
| Cashflow realized (sells−buys+redeems+rebates) | -$4,392,612.28 |
| Core cashflow (ex-rebates) | -$4,392,657.34 |
| Closed-position legs sum | $2,198,738.71 |
| Leg win rate / profit factor | 51.15% / 1.0414 |
| Polymarket leaderboard ALL | $3,588,720.22 · vol $402,071,822.94 · rank 38 |
| polymarket_leaderboard_ALL pnl | ref=3588720.2180176293 ours=2198738.7126 (DRIFT) |
| polydata realized_pnl | ref=3588720.22 ours=2198738.7126 (DRIFT) |
| polydata n_trades | ref=1047862 ours=119316 (DRIFT) |
| polydata win_rate | ref=0.5174 ours=0.5115 (MATCH) |

Notes: Polymarket leaderboard ALL is the primary official PnL check (we match within tolerance). PolyData uses a different event aggregation / trade counting method — expect DRIFT on WR and trade count; use it as a secondary research signal, not the ground truth for fills.

## 2. Universe — where the money is

- **O/U / totals:** 3875 markets · $114,731.37 · avg $29.61 · median hold 5h23m · median spread None
- **Match / other sports:** 2481 markets · $271,017.02 · avg $109.24
- **Outcome PnL leaders:**
  - **Under**: $264,084.62
  - **Tulane**: $152,581.26
  - **Lakers**: $150,762.22
  - **Utah State Aggies**: $113,758.17
  - **Hawks**: $107,209.88
  - **Trail Blazers**: $88,784.33

### Bot universe rules

1. Only liquid live sports (soccer/football first — their tape is soccer-heavy).
2. Prefer O/U lines with tight books and active in-game trading.
3. Default bias toward **Over** unless your signal says otherwise (their Over PnL dominates).
4. Skip politics/crypto until you have separate evidence.
5. Require enough depth to enter ~median clip and exit within 1–2 minutes.

## 3. ENTRY — exact mechanics

### Style histogram
- `two_sided_inventory_near_mid`: 3514
- `directional_buy_near_mid`: 2134
- `two_sided_inventory_sub_mid`: 949
- `two_sided_inventory_above_mid`: 643
- `directional_buy_sub_mid`: 635
- `directional_buy_above_mid`: 425
- `two_sided_inventory_expensive_favorite`: 230
- `two_sided_inventory_cheap_tail`: 180
- `directional_buy_expensive_favorite`: 144
- `directional_buy_cheap_tail`: 84

### First-two-fill sequences
- `BUY->BUY`: 7346
- `single_fill`: 1586
- `BUY->SELL`: 6

### Entry price → realized edge

| Avg buy band | Markets | Total PnL | Avg PnL |
|---|---:|---:|---:|
| 0.00-0.20 | 79 | -$25,220.90 | -$319.25 |
| 0.20-0.40 | 425 | $159,738.19 | $375.85 |
| 0.40-0.60 | 7856 | $133,122.56 | $16.95 |
| 0.60-0.80 | 434 | $100,054.11 | $230.54 |
| 0.80-1.00 | 144 | $24,477.71 | $169.98 |

**Best band:** 0.40–0.60 (near mid) — highest average PnL. Tails (≤0.20 or ≥0.80) make less per market.

### Entry checklist (bot)

1. Clip **$20.31** median (p90 $634.25).
2. Aim entry price ~**0.4981** (IQR (0.4798, 0.53)).
3. Trigger = microstructure, not long-term forecast:
   - mid dips / liquidity hole you can buy
   - imminent volatility (attack, corner, shot) where Over can jump
   - resting bid gets lifted? you’re being taken — manage immediately
4. Prefer **maker bids**; take only if the expected jump already started and ask is still inside your edge.
5. Same-second multi-fills are normal (one order, many counterparties) — treat as one decision, many fills.

## 4. MANAGEMENT — what they do after entry

### Styles
- `multi_hour_position`: 5405
- `single_clip`: 2651
- `intraday_swing`: 691
- `scalp_sub_15m`: 189
- `market_make_both_outcomes`: 2

### Winners vs losers

| Metric | Winners | Losers |
|---|---:|---:|
| N | 4614 | 4322 |
| PnL | $7,594,109.26 | -$7,201,937.58 |
| Median hold | 5h46m | 6h06m |
| Median spread | -0.0037 | -0.01 |
| Scale-in rate | 0.821 | 0.8232 |
| Scale-out rate | 0.0 | 0.0 |
| Avg fills/market | 13.43 | 13.27 |
| Both-sides rate | 0.6131 | 0.6215 |

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

- **Winners** sell above buy (median spread **-0.0037**). **Losers** often exit worse (median spread **-0.01**).
- Losers scale-in **more** (0.8232 vs 0.821) — averaging down is how they bleed; the bot should **forbid** revenge scale-ins without a fresh signal.
- Hold edge peaks in **<5m** ({'n': 1868, 'pnl': 17732.7304, 'avg': 9.4929, 'win_rate': 0.5203}) and a strong **30m–2h** bucket for the larger in-game campaigns.

## 5. EXIT — rules that print

- `hold_to_resolution_or_redeem`: 8929
- `adverse_exit_sell_below_buy`: 4
- `mixed_roundtrip`: 4
- `spread_harvest_sell_above_buy`: 1

| Hold bucket | N | Total PnL | Avg | Win rate |
|---|---:|---:|---:|---:|
| <5m | 1868 | $17,732.73 | $9.49 | 52.0% |
| 5-30m | 408 | -$63,068.61 | -$154.58 | 48.0% |
| 30m-2h | 807 | -$38,579.83 | -$47.81 | 52.9% |
| 2-12h | 3155 | $557,479.86 | $176.70 | 52.0% |
| 12h+ | 2700 | -$81,392.48 | -$30.15 | 51.0% |

### Exit engine params

1. **TP / ask distance:** target ≈ **-0.0037** above avg entry (p75 stretch 0.0706). On live O/U this is often a burst move, not slow grind.
2. **Time stop:** median hold 5h46m; p75 13h54m for the scalps — escalate urgency after that.
3. **Scale-out:** peel into strength (their winners stack sells). Don’t wait for one perfect print.
4. **Stop:** if mid < entry − ~3–5¢ on unhedged inventory with no signal → take the loss (copy losers’ speed, not their hope).
5. **Flatten before resolution** — redeem is residual.
6. Taker exits are fine when the move already happened and maker asks won’t fill.

## 6. What works / what fails

### Works
- Winners capture median spread -0.0037 vs losers -0.01
- Both-sides inventory on 61.3% of winning markets (losers 62.2%)
- Hold bucket <5m: avg PnL $9.49 on 1868 markets (WR 52%)
- Hold bucket 2-12h: avg PnL $176.70 on 3155 markets (WR 52%)
- Entry band 0.20-0.40: avg $375.85 across 425 markets
- Entry band 0.40-0.60: avg $16.95 across 7856 markets
- Entry band 0.60-0.80: avg $230.54 across 434 markets
- Entry band 0.80-1.00: avg $169.98 across 144 markets
- Buy-ladder behavior: fade-into-weakness markets=1727, chase-up markets=1672

### Fails
- Hold bucket 5-30m: avg PnL $-154.58 on 408 markets
- Hold bucket 30m-2h: avg PnL $-47.81 on 807 markets
- Hold bucket 12h+: avg PnL $-30.15 on 2700 markets
- Entry band 0.00-0.20: avg $-319.25 across 79 markets — avoid or tighten risk
- Chase vs fade ladders: `{'chase_up': 1672, 'fade_down': 1727}`

## 7. Fill-by-fill autopsies (copy these patterns)

## 8. Failure modes (do not bot these)

1. **Spread: Virginia Cavaliers (-3.5)** -$98,306.11 · hold 6m26s · entry 0.409 → exit None · `scalp_sub_15m` / `hold_to_resolution_or_redeem`
2. **Spread: Thunder (-8.5)** -$70,992.09 · hold 46m38s · entry 0.4928 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
3. **Spread: Florida State (-6.5)** -$70,979.38 · hold 15h52m · entry 0.4914 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
4. **Spread: Rockets (-7.5)** -$55,520.54 · hold 20h23m · entry 0.462 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
5. **Bills vs. Texans: O/U 44.5** -$55,214.96 · hold 21h20m · entry 0.4892 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
6. **Army vs. Air Force** -$51,257.30 · hold 1h15m · entry 0.4631 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
7. **Chiefs vs. Bills: O/U 50.5** -$37,034.38 · hold 7h31m · entry 0.559 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
8. **Missouri vs. Oklahoma** -$36,894.01 · hold 13h58m · entry 0.3693 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
9. **Nets vs. Celtics** -$36,742.02 · hold 20h38m · entry 0.7303 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
10. **UAB Blazers vs. Rice** -$30,622.12 · hold 5h40m · entry 0.4741 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`

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
   - default post-only bids/asks; clip $20.31
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
template: sovereign2013
mode: one_sided_live_scalper  # not classic two-sided MM
preferred_outcome_bias: Over
clip_usdc_median: 20.3077
clip_usdc_p90: 634.25
entry_price_median: 0.4981
entry_price_iqr: (0.4798, 0.53)
target_spread: -0.0037
target_spread_p75: 0.0706
median_hold_seconds: 20795
max_hold_seconds_p75: 50074
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

_Generated 2026-08-28T15:08:28.307900+00:00_


## 8. Structured autopsy (A–G)

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


## 9. Hour / DOW volume (UTC)

| Hour | USDC volume |
|---:|---:|
| 0 | 2509723.57 |
| 1 | 1163260.63 |
| 2 | 1108034.74 |
| 3 | 644122.47 |
| 4 | 339169.94 |
| 5 | 368410.65 |
| 6 | 412333.62 |
| 7 | 289145.33 |
| 8 | 280840.1 |
| 9 | 256872.01 |
| 10 | 416679.33 |
| 11 | 540367.45 |
| 12 | 738681.77 |
| 13 | 1345917.03 |
| 14 | 1509146.17 |
| 15 | 1882889.09 |
| 16 | 2111640.32 |
| 17 | 1812325.09 |
| 18 | 1576684.45 |
| 19 | 1800437.38 |
| 20 | 1690544.81 |
| 21 | 1829106.04 |
| 22 | 2419470.81 |
| 23 | 3374515.67 |

| DOW (0=Mon) | USDC volume |
|---:|---:|
| 0 | 3143637.71 |
| 1 | 3309479.95 |
| 2 | 4132545.06 |
| 3 | 3153840.39 |
| 4 | 4027414.87 |
| 5 | 7637418.27 |
| 6 | 5015982.23 |

## 10. Bot schema pointer

Parse `MASTER.json` keys: `reconciliation`, `identity`, `performance`, `extras`, `copyability`, `equity_curve_daily`, `deep_dive_highlights`.
