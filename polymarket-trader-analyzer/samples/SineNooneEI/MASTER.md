# MASTER AUTOPSY — SineNooneEI

> Single file for humans **and** bots. Machine-readable twin: `MASTER.json` · Equity: `equity_curve.csv`.

- Wallet: `0x38337de21ff0bb0a11a40761507d51e318d633d1`
- Generated: `2026-08-25T21:55:39.454208+00:00`
- Identity class: **`directional_hold_to_resolution`**

## 0. Executive verdict

This trader is classified as **directional_hold_to_resolution** with primary focus **sports_match**. Preferred PnL (**cashflow_realized**) **$541,301.28** (leaderboard ALL $639,212.87; REVIEW). Unique trades **16,603**. Copy difficulty **9/10** · ease **2/10**. Buy-and-hold / resolution harvesting at large notional. Easy mechanically (buy → wait → redeem) but edge is selection + bankroll + path risk, not a simple rule.

**Exit mechanics:** `sell_secondary_market`
**Kalshi two-sided MM fit:** MEDIUM — extract risk + hold rules; re-fit microstructure on Kalshi
**Preferred PnL note:** Cashflow usually tracks leaderboard for buy+sell scalpers.

## 1. Reconciliation (mandatory)

| Source | PnL | Extra |
|---|---:|---|
| **Preferred (cashflow_realized)** | **$541,301.28** | vs LB diff=-97911.59 |
| Ours cashflow realized | $541,301.28 | trades=16,603 buy_only=False |
| Ours core (ex-rebate) | $523,137.79 | WR legs=79.53% |
| Ours closed-legs sum | $3,761,463.08 | PF=1.9658 |
| Polymarket leaderboard ALL | $639,212.87 | vol=$29,168,764.39 rank=318 |
| PolyData | $506,308.10 | trades=14776 WR=0.5312 |

- DRIFT: `polymarket_leaderboard_ALL` pnl ours=541301.2799 field=cashflow_realized ref=639212.8736756515 diff=-97911.5938
- MATCH: `polydata` realized_pnl ours=523137.7892 field=cashflow_core ref=506308.1 diff=16829.6892
- DRIFT: `polydata` n_trades ours=16603 field=None ref=14776 diff=1827
- DRIFT: `polydata` win_rate ours=0.7953 field=None ref=0.5312 diff=0.2641
- DRIFT: `internal` cashflow_vs_closed ours=541301.2799 field=None ref=3761463.0818 diff=-3220161.8019

## 2. Identity & microstructure

- Both-sides rate: 1.01% (16 markets)
- Clip median/p90/max: $29.11 / $2,314.63 / $86,562.02
- Category PnL: `{'sports_match': 3639964.63, 'sports_totals': 94457.53, 'other': 27040.92}`
- Start BUY first: 1580 · SELL first: 0
- Entry maker/taker: 40.59% / 59.41% (14,924/1,675 fills)
- Exit maker/taker: 0.0% / 100.0% (0/4 fills)
- Patterns: `{'enter_maker_exit_taker': 2, 'enter_taker_exit_taker': 2}`

### Outcome volume (top)

| Outcome | Buy USDC | Sell USDC | Sell−Buy |
|---|---:|---:|---:|
| Dplus KIA | $718,854.10 | $0.00 | -$718,854.10 |
| G2 Esports | $679,045.94 | $0.00 | -$679,045.94 |
| Team Liquid | $662,025.87 | $8,628.03 | -$653,397.84 |
| MOUZ | $634,892.86 | $0.00 | -$634,892.86 |
| Karmine Corp | $499,339.83 | $0.00 | -$499,339.83 |
| Team Yandex | $441,258.45 | $0.00 | -$441,258.45 |
| Cloud9 | $416,718.53 | $0.00 | -$416,718.53 |
| Bilibili Gaming | $394,724.24 | $0.00 | -$394,724.24 |
| JD Gaming | $365,058.63 | $0.00 | -$365,058.63 |
| Movistar KOI | $352,470.87 | $0.00 | -$352,470.87 |
| Gen.G | $346,534.86 | $0.00 | -$346,534.86 |
| BetBoom Team | $340,925.11 | $0.00 | -$340,925.11 |

## 3. Performance metrics (kitchen sink)

- Expectancy / market: $3,565.37
- Avg win / avg loss: $8,947.30 / -$18,090.48 · ratio=0.4946
- PnL / day: $2,677.32 · trades/day=82.12 · markets/day=7.81
- PnL concentration HHI: 0.002435 (higher=more concentrated)
- Notional sum: $14,927,265.81 · median ticket $29.11
- Buy price median: 0.49 · Sell price median: 0.4752
- Activity types: `{'DEPOSIT': 4, 'TRADE': 16603, 'REDEEM': 1081, 'REWARD': 41, 'MAKER_REBATE': 106, 'WITHDRAWAL': 3, 'TAKER_REBATE': 65}`
- Open risk: `{'n': 526, 'cash_pnl': -2851007.5, 'current_value': 0.0, 'redeemable': 526}`

### Hold-time engine

| Bucket | N | WR | Total PnL | Avg | Median |
|---|---:|---:|---:|---:|---:|
| <30s | 1000 | 85.33% | $2,659,672.17 | $2,659.67 | $415.32 |
| 30s-2m | 303 | 73.17% | $349,628.85 | $1,153.89 | $0.00 |
| 2-5m | 76 | 70.18% | $12,785.85 | $168.23 | $272.91 |
| 5-15m | 25 | 55.00% | $16,849.11 | $673.96 | $0.00 |
| 15m+ | 176 | 74.66% | $722,527.10 | $4,105.27 | $3,556.02 |

### Entry price bands

| Band | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| 0-20¢ | 29 | 61.54% | $68,889.33 | $2,375.49 |
| 20-40¢ | 382 | 69.91% | $1,219,824.16 | $3,193.26 |
| 40-60¢ | 664 | 75.85% | $994,426.76 | $1,497.63 |
| 60-80¢ | 473 | 90.41% | $1,410,157.89 | $2,981.31 |
| 80-100¢ | 32 | 88.46% | $68,164.95 | $2,130.15 |

### Family

| Family | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| Other | 1568 | 80.23% | $3,759,968.01 | $2,397.94 |
| Over/Under | 7 | 80.00% | $72,156.06 | $10,308.01 |
| Yes/No moneyline | 5 | 33.33% | -$70,660.99 | -$14,132.20 |

## 4. Equity curve (critical)

### 4a. Cashflow activity equity

- Final equity (cashflow): **$541,301.28**
- Max DD: **-$414,391.76** (-631.01% of peak)
- Longest DD: **6 days**
- Daily Sharpe (ann.): **0.853**
- Days: 195

Files: `equity_curve.csv` · `equity_curve.json` (source=`cashflow_activity`)

<details><summary>Daily cashflow equity table (full)</summary>

| Date | Equity | Daily PnL | Drawdown |
|---|---:|---:|---:|
| 2026-02-03 | -92605.88 | -92605.88 | -92605.88 |
| 2026-02-04 | 31784.73 | 124390.61 | 0.00 |
| 2026-02-05 | 10745.76 | -21038.97 | -21038.97 |
| 2026-02-06 | 62506.86 | 51761.10 | 0.00 |
| 2026-02-07 | 65670.87 | 3164.01 | 0.00 |
| 2026-02-08 | -148095.22 | -213766.09 | -213766.09 |
| 2026-02-09 | 24714.84 | 172810.06 | -40956.03 |
| 2026-02-10 | 2067.96 | -22646.88 | -63602.90 |
| 2026-02-11 | -112671.07 | -114739.03 | -178341.94 |
| 2026-02-12 | -117171.89 | -4500.81 | -182842.75 |
| 2026-02-13 | -195422.96 | -78251.07 | -261093.83 |
| 2026-02-14 | -92422.29 | 103000.67 | -158093.16 |
| 2026-02-15 | -348720.89 | -256298.60 | -414391.76 |
| 2026-02-16 | 56022.39 | 404743.28 | -9648.48 |
| 2026-02-17 | 146208.93 | 90186.55 | 0.00 |
| 2026-02-18 | 120042.27 | -26166.66 | -26166.66 |
| 2026-02-19 | 72665.44 | -47376.83 | -73543.49 |
| 2026-02-20 | -14422.60 | -87088.04 | -160631.53 |
| 2026-02-21 | -15244.49 | -821.89 | -161453.42 |
| 2026-02-22 | -33909.21 | -18664.72 | -180118.14 |
| 2026-02-23 | -13723.88 | 20185.32 | -159932.82 |
| 2026-02-24 | -73584.38 | -59860.50 | -219793.31 |
| 2026-02-25 | -147834.89 | -74250.51 | -294043.82 |
| 2026-02-26 | 28294.85 | 176129.74 | -117914.09 |
| 2026-02-27 | -7487.52 | -35782.36 | -153696.45 |
| 2026-02-28 | -59214.59 | -51727.07 | -205423.52 |
| 2026-03-01 | -19880.29 | 39334.29 | -166089.23 |
| 2026-03-02 | 25617.61 | 45497.90 | -120591.32 |
| 2026-03-03 | -70386.05 | -96003.66 | -216594.99 |
| 2026-03-04 | -148532.92 | -78146.87 | -294741.86 |
| 2026-03-05 | -88423.67 | 60109.26 | -234632.60 |
| 2026-03-06 | -67247.62 | 21176.05 | -213456.55 |
| 2026-03-07 | -118131.45 | -50883.83 | -264340.39 |
| 2026-03-08 | -73868.83 | 44262.62 | -220077.76 |
| 2026-03-09 | 3627.90 | 77496.73 | -142581.03 |
| 2026-03-10 | -13956.45 | -17584.35 | -160165.38 |
| 2026-03-11 | -35334.38 | -21377.93 | -181543.31 |
| 2026-03-12 | 8960.89 | 44295.27 | -137248.04 |
| 2026-03-13 | -87359.26 | -96320.15 | -233568.19 |
| 2026-03-14 | -161162.30 | -73803.04 | -307371.23 |
| 2026-03-15 | -108606.24 | 52556.06 | -254815.17 |
| 2026-03-16 | -149197.81 | -40591.57 | -295406.74 |
| 2026-03-17 | -109123.99 | 40073.82 | -255332.92 |
| 2026-03-18 | -119124.07 | -10000.08 | -265333.00 |
| 2026-03-19 | -111885.96 | 7238.12 | -258094.89 |
| 2026-03-20 | -93266.61 | 18619.35 | -239475.54 |
| 2026-03-21 | -85872.92 | 7393.69 | -232081.85 |
| 2026-03-22 | -120813.39 | -34940.47 | -267022.33 |
| 2026-03-23 | -102376.92 | 18436.48 | -248585.85 |
| 2026-03-24 | -113581.99 | -11205.07 | -259790.92 |
| 2026-03-25 | -122173.85 | -8591.86 | -268382.78 |
| 2026-03-26 | -190197.60 | -68023.75 | -336406.53 |
| 2026-03-27 | -138619.88 | 51577.72 | -284828.81 |
| 2026-03-28 | -103296.44 | 35323.44 | -249505.37 |
| 2026-03-29 | -113443.15 | -10146.71 | -259652.08 |
| 2026-03-30 | -72974.78 | 40468.37 | -219183.71 |
| 2026-04-01 | -62974.78 | 9999.99 | -209183.72 |
| 2026-04-02 | -17394.13 | 45580.66 | -163603.06 |
| 2026-04-03 | -37000.82 | -19606.69 | -183209.75 |
| 2026-04-04 | 8800.65 | 45801.46 | -137408.29 |
| 2026-04-05 | -76338.11 | -85138.75 | -222547.04 |
| 2026-04-06 | -28973.11 | 47364.99 | -175182.05 |
| 2026-04-07 | 31057.02 | 60030.13 | -115151.91 |
| 2026-04-08 | -6841.23 | -37898.25 | -153050.16 |
| 2026-04-09 | -20779.61 | -13938.38 | -166988.55 |
| 2026-04-10 | 11034.28 | 31813.89 | -135174.66 |
| 2026-04-11 | -14152.52 | -25186.79 | -160361.45 |
| 2026-04-12 | 31411.17 | 45563.69 | -114797.76 |
| 2026-04-13 | -13132.98 | -44544.15 | -159341.91 |
| 2026-04-14 | 23578.37 | 36711.35 | -122630.56 |
| 2026-04-15 | 10663.04 | -12915.33 | -135545.89 |
| 2026-04-16 | -22725.15 | -33388.19 | -168934.08 |
| 2026-04-17 | -105647.03 | -82921.88 | -251855.96 |
| 2026-04-18 | -197129.99 | -91482.97 | -343338.93 |
| 2026-04-19 | -27788.38 | 169341.62 | -173997.31 |
| 2026-04-20 | 4252.28 | 32040.66 | -141956.65 |
| 2026-04-21 | -35218.54 | -39470.82 | -181427.47 |
| 2026-04-22 | -94695.47 | -59476.93 | -240904.40 |
| 2026-04-23 | -125103.20 | -30407.74 | -271312.14 |
| 2026-04-24 | -127170.87 | -2067.67 | -273379.80 |
| 2026-04-25 | -203824.31 | -76653.44 | -350033.25 |
| 2026-04-26 | -227321.91 | -23497.60 | -373530.84 |
| 2026-04-27 | -143088.21 | 84233.70 | -289297.15 |
| 2026-04-28 | -128324.41 | 14763.80 | -274533.35 |
| 2026-04-29 | -170856.98 | -42532.57 | -317065.91 |
| 2026-04-30 | -222883.12 | -52026.14 | -369092.06 |
| 2026-05-01 | -159952.19 | 62930.93 | -306161.12 |
| 2026-05-02 | -117043.58 | 42908.61 | -263252.51 |
| 2026-05-03 | -128522.16 | -11478.58 | -274731.09 |
| 2026-05-04 | -104138.06 | 24384.10 | -250346.99 |
| 2026-05-05 | -81587.45 | 22550.61 | -227796.38 |
| 2026-05-06 | -53401.96 | 28185.49 | -199610.89 |
| 2026-05-07 | -121073.19 | -67671.24 | -267282.13 |
| 2026-05-08 | -112061.28 | 9011.91 | -258270.21 |
| 2026-05-09 | -106099.36 | 5961.92 | -252308.30 |
| 2026-05-10 | -82546.68 | 23552.68 | -228755.62 |
| 2026-05-11 | -75885.53 | 6661.15 | -222094.46 |
| 2026-05-12 | -119401.99 | -43516.46 | -265610.92 |
| 2026-05-13 | -17492.35 | 101909.63 | -163701.29 |
| 2026-05-14 | -282.42 | 17209.94 | -146491.35 |
| 2026-05-15 | -6369.66 | -6087.25 | -152578.60 |
| 2026-05-16 | -27159.51 | -20789.85 | -173368.45 |
| 2026-05-17 | -766.01 | 26393.51 | -146974.94 |
| 2026-05-18 | 38150.07 | 38916.08 | -108058.86 |
| 2026-05-19 | -25258.49 | -63408.57 | -171467.43 |
| 2026-05-20 | 18726.97 | 43985.46 | -127481.97 |
| 2026-05-21 | -71973.62 | -90700.58 | -218182.55 |
| 2026-05-22 | -4315.85 | 67657.77 | -150524.78 |
| 2026-05-23 | -16307.29 | -11991.44 | -162516.23 |
| 2026-05-24 | 17930.02 | 34237.32 | -128278.91 |
| 2026-05-25 | -1876.61 | -19806.63 | -148085.54 |
| 2026-05-26 | -16368.15 | -14491.54 | -162577.08 |
| 2026-05-27 | 91016.82 | 107384.96 | -55192.12 |
| 2026-05-28 | 104877.81 | 13860.99 | -41331.12 |
| 2026-05-29 | 120665.15 | 15787.34 | -25543.79 |
| 2026-05-30 | 164481.24 | 43816.10 | 0.00 |
| 2026-05-31 | 92499.28 | -71981.96 | -71981.96 |
| 2026-06-01 | 144648.08 | 52148.80 | -19833.16 |
| 2026-06-02 | 284563.20 | 139915.11 | 0.00 |
| 2026-06-03 | 301724.68 | 17161.49 | 0.00 |
| 2026-06-04 | 229487.92 | -72236.76 | -72236.76 |
| 2026-06-05 | 288006.67 | 58518.75 | -13718.01 |
| 2026-06-06 | 373279.72 | 85273.05 | 0.00 |
| 2026-06-07 | 312990.42 | -60289.30 | -60289.30 |
| 2026-06-08 | 263467.71 | -49522.71 | -109812.01 |
| 2026-06-09 | 295999.45 | 32531.75 | -77280.27 |
| 2026-06-10 | 298342.65 | 2343.19 | -74937.07 |
| 2026-06-11 | 284287.92 | -14054.73 | -88991.80 |
| 2026-06-12 | 314500.40 | 30212.48 | -58779.32 |
| 2026-06-13 | 286664.90 | -27835.50 | -86614.82 |
| 2026-06-14 | 302327.07 | 15662.17 | -70952.65 |
| 2026-06-15 | 328343.02 | 26015.95 | -44936.70 |
| 2026-06-16 | 351952.44 | 23609.42 | -21327.28 |
| 2026-06-17 | 352025.18 | 72.73 | -21254.54 |
| 2026-06-19 | 361402.67 | 9377.49 | -11877.05 |
| 2026-06-20 | 350021.55 | -11381.11 | -23258.17 |
| 2026-06-21 | 350041.75 | 20.19 | -23237.97 |
| 2026-06-22 | 350083.88 | 42.13 | -23195.84 |
| 2026-06-23 | 351089.53 | 1005.65 | -22190.19 |
| 2026-06-30 | 325784.97 | -25304.55 | -47494.75 |
| 2026-07-01 | 329070.37 | 3285.39 | -44209.35 |
| 2026-07-02 | 329082.99 | 12.62 | -44196.73 |
| 2026-07-03 | 349987.66 | 20904.67 | -23292.06 |
| 2026-07-04 | 337508.86 | -12478.80 | -35770.86 |
| 2026-07-05 | 319525.05 | -17983.80 | -53754.67 |
| 2026-07-06 | 319562.43 | 37.38 | -53717.29 |
| 2026-07-07 | 314506.88 | -5055.55 | -58772.84 |
| 2026-07-08 | 329169.20 | 14662.32 | -44110.52 |
| 2026-07-09 | 330438.76 | 1269.56 | -42840.96 |
| 2026-07-10 | 317269.26 | -13169.50 | -56010.46 |
| 2026-07-11 | 320328.35 | 3059.10 | -52951.37 |
| 2026-07-12 | 311758.37 | -8569.98 | -61521.35 |
| 2026-07-13 | 311973.24 | 214.87 | -61306.48 |
| 2026-07-14 | 311056.19 | -917.05 | -62223.53 |
| 2026-07-15 | 312084.33 | 1028.14 | -61195.39 |
| 2026-07-16 | 316844.96 | 4760.64 | -56434.76 |
| 2026-07-17 | 409495.50 | 92650.54 | 0.00 |
| 2026-07-18 | 434639.64 | 25144.14 | 0.00 |
| 2026-07-19 | 438412.21 | 3772.57 | 0.00 |
| 2026-07-20 | 438646.03 | 233.83 | 0.00 |
| 2026-07-21 | 432940.06 | -5705.97 | -5705.97 |
| 2026-07-22 | 422783.52 | -10156.55 | -15862.52 |
| 2026-07-23 | 426136.01 | 3352.49 | -12510.02 |
| 2026-07-24 | 448137.32 | 22001.31 | 0.00 |
| 2026-07-25 | 439491.82 | -8645.50 | -8645.50 |
| 2026-07-26 | 417299.75 | -22192.07 | -30837.58 |
| 2026-07-27 | 431190.50 | 13890.75 | -16946.82 |
| 2026-07-29 | 399289.50 | -31901.00 | -48847.82 |
| 2026-07-30 | 401056.25 | 1766.75 | -47081.07 |
| 2026-07-31 | 445528.93 | 44472.68 | -2608.40 |
| 2026-08-01 | 419925.00 | -25603.93 | -28212.32 |
| 2026-08-02 | 411779.27 | -8145.73 | -36358.05 |
| 2026-08-03 | 449843.85 | 38064.58 | 0.00 |
| 2026-08-04 | 477538.04 | 27694.19 | 0.00 |
| 2026-08-05 | 465886.14 | -11651.90 | -11651.90 |
| 2026-08-06 | 453463.95 | -12422.19 | -24074.09 |
| 2026-08-07 | 514312.23 | 60848.28 | 0.00 |
| 2026-08-08 | 453768.63 | -60543.60 | -60543.60 |
| 2026-08-09 | 489628.38 | 35859.75 | -24683.85 |
| 2026-08-10 | 481278.61 | -8349.78 | -33033.63 |
| 2026-08-11 | 481450.77 | 172.17 | -32861.46 |
| 2026-08-12 | 498259.85 | 16809.07 | -16052.39 |
| 2026-08-13 | 513157.81 | 14897.97 | -1154.42 |
| 2026-08-14 | 529984.23 | 16826.42 | 0.00 |
| 2026-08-15 | 609199.31 | 79215.08 | 0.00 |
| 2026-08-16 | 644162.73 | 34963.41 | 0.00 |
| 2026-08-17 | 659070.69 | 14907.96 | 0.00 |
| 2026-08-18 | 659170.87 | 100.19 | 0.00 |
| 2026-08-19 | 645403.06 | -13767.81 | -13767.81 |
| 2026-08-20 | 610152.22 | -35250.84 | -49018.65 |
| 2026-08-21 | 624719.16 | 14566.93 | -34451.72 |
| 2026-08-22 | 607108.21 | -17610.95 | -52062.67 |
| 2026-08-23 | 524397.95 | -82710.26 | -134772.93 |
| 2026-08-24 | 520981.71 | -3416.24 | -138189.17 |
| 2026-08-25 | 541301.28 | 20319.57 | -117869.59 |

</details>

### 4b. Closed-positions equity (alt — critical for buy-only books)

- Final closed equity: **$3,761,463.08**
- Max DD: **-$253,587.02**
- Daily Sharpe (ann.): **8.186**
- Days: 176

Files: `equity_curve_closed.csv` · `equity_curve_closed.json` (source=`closed_positions`)

<details><summary>Daily closed equity table (full)</summary>

| Date | Equity | Daily PnL | Drawdown |
|---|---:|---:|---:|
| 2026-02-03 | 45608.03 | 45608.03 | 0.00 |
| 2026-02-04 | 57009.42 | 11401.39 | 0.00 |
| 2026-02-05 | 47800.99 | -9208.43 | -9208.43 |
| 2026-02-06 | 138832.53 | 91031.54 | 0.00 |
| 2026-02-07 | 133480.87 | -5351.67 | -5351.67 |
| 2026-02-08 | -17951.06 | -151431.93 | -156783.59 |
| 2026-02-09 | 49255.41 | 67206.47 | -89577.12 |
| 2026-02-10 | 48939.43 | -315.98 | -89893.10 |
| 2026-02-11 | -86372.23 | -135311.66 | -225204.76 |
| 2026-02-13 | -15921.70 | 70450.53 | -154754.24 |
| 2026-02-14 | -29953.82 | -14032.12 | -168786.35 |
| 2026-02-15 | -46677.54 | -16723.72 | -185510.08 |
| 2026-02-16 | 97214.80 | 143892.34 | -41617.74 |
| 2026-02-17 | 190059.88 | 92845.09 | 0.00 |
| 2026-02-18 | 196616.21 | 6556.33 | 0.00 |
| 2026-02-19 | 164741.02 | -31875.19 | -31875.19 |
| 2026-02-20 | 156049.46 | -8691.56 | -40566.75 |
| 2026-02-21 | 123088.35 | -32961.11 | -73527.86 |
| 2026-02-22 | 125983.96 | 2895.62 | -70632.24 |
| 2026-02-23 | 115449.09 | -10534.88 | -81167.12 |
| 2026-02-24 | 126334.04 | 10884.95 | -70282.17 |
| 2026-02-25 | 13051.67 | -113282.37 | -183564.54 |
| 2026-02-26 | 201479.99 | 188428.33 | 0.00 |
| 2026-02-27 | 238990.83 | 37510.84 | 0.00 |
| 2026-02-28 | 256876.44 | 17885.60 | 0.00 |
| 2026-03-01 | 321053.54 | 64177.10 | 0.00 |
| 2026-03-02 | 174543.01 | -146510.54 | -146510.54 |
| 2026-03-03 | 92348.02 | -82194.98 | -228705.52 |
| 2026-03-04 | 67466.52 | -24881.51 | -253587.02 |
| 2026-03-05 | 106528.50 | 39061.98 | -214525.04 |
| 2026-03-07 | 150073.44 | 43544.94 | -170980.10 |
| 2026-03-08 | 166610.40 | 16536.96 | -154443.14 |
| 2026-03-09 | 240589.62 | 73979.22 | -80463.92 |
| 2026-03-10 | 260191.15 | 19601.52 | -60862.40 |
| 2026-03-11 | 225239.76 | -34951.38 | -95813.78 |
| 2026-03-12 | 255688.37 | 30448.60 | -65365.17 |
| 2026-03-13 | 263769.96 | 8081.59 | -57283.58 |
| 2026-03-14 | 197241.63 | -66528.33 | -123811.91 |
| 2026-03-15 | 203239.94 | 5998.30 | -117813.60 |
| 2026-03-16 | 230567.74 | 27327.81 | -90485.80 |
| 2026-03-17 | 237533.82 | 6966.07 | -83519.72 |
| 2026-03-18 | 227533.74 | -10000.08 | -93519.80 |
| 2026-03-19 | 207318.86 | -20214.88 | -113734.68 |
| 2026-03-20 | 226838.20 | 19519.34 | -94215.34 |
| 2026-03-21 | 248640.02 | 21801.82 | -72413.52 |
| 2026-03-22 | 236305.93 | -12334.10 | -84747.61 |
| 2026-03-23 | 251465.34 | 15159.41 | -69588.20 |
| 2026-03-24 | 261508.78 | 10043.44 | -59544.76 |
| 2026-03-25 | 268297.49 | 6788.71 | -52756.06 |
| 2026-03-26 | 276973.66 | 8676.17 | -44079.88 |
| 2026-03-27 | 330730.84 | 53757.19 | 0.00 |
| 2026-03-28 | 322691.16 | -8039.68 | -8039.68 |
| 2026-03-29 | 345467.93 | 22776.78 | 0.00 |
| 2026-03-30 | 349205.38 | 3737.45 | 0.00 |
| 2026-04-02 | 417122.05 | 67916.67 | 0.00 |
| 2026-04-03 | 407713.09 | -9408.96 | -9408.96 |
| 2026-04-04 | 485618.89 | 77905.79 | 0.00 |
| 2026-04-05 | 496152.68 | 10533.80 | 0.00 |
| 2026-04-06 | 534448.58 | 38295.90 | 0.00 |
| 2026-04-07 | 551477.42 | 17028.84 | 0.00 |
| 2026-04-08 | 583854.45 | 32377.03 | 0.00 |
| 2026-04-09 | 571684.72 | -12169.72 | -12169.72 |
| 2026-04-10 | 612515.93 | 40831.21 | 0.00 |
| 2026-04-11 | 535421.10 | -77094.83 | -77094.83 |
| 2026-04-12 | 602073.27 | 66652.16 | -10442.67 |
| 2026-04-13 | 887383.39 | 285310.12 | 0.00 |
| 2026-04-14 | 900632.94 | 13249.55 | 0.00 |
| 2026-04-15 | 880260.24 | -20372.70 | -20372.70 |
| 2026-04-16 | 878136.16 | -2124.08 | -22496.78 |
| 2026-04-17 | 757594.57 | -120541.59 | -143038.37 |
| 2026-04-18 | 810113.38 | 52518.81 | -90519.56 |
| 2026-04-19 | 897248.14 | 87134.76 | -3384.80 |
| 2026-04-20 | 1010359.74 | 113111.60 | 0.00 |
| 2026-04-21 | 960929.39 | -49430.35 | -49430.35 |
| 2026-04-22 | 971676.37 | 10746.98 | -38683.37 |
| 2026-04-23 | 929296.14 | -42380.23 | -81063.60 |
| 2026-04-24 | 914001.93 | -15294.21 | -96357.81 |
| 2026-04-25 | 906273.70 | -7728.23 | -104086.04 |
| 2026-04-26 | 915419.99 | 9146.29 | -94939.75 |
| 2026-04-27 | 931093.52 | 15673.52 | -79266.22 |
| 2026-04-28 | 964524.85 | 33431.33 | -45834.89 |
| 2026-04-29 | 979171.89 | 14647.04 | -31187.85 |
| 2026-04-30 | 997438.97 | 18267.08 | -12920.77 |
| 2026-05-01 | 1014623.50 | 17184.53 | 0.00 |
| 2026-05-02 | 1064756.24 | 50132.74 | 0.00 |
| 2026-05-03 | 1064405.06 | -351.18 | -351.18 |
| 2026-05-04 | 1103709.03 | 39303.97 | 0.00 |
| 2026-05-05 | 1110195.78 | 6486.76 | 0.00 |
| 2026-05-06 | 1145817.93 | 35622.14 | 0.00 |
| 2026-05-07 | 1126423.45 | -19394.47 | -19394.47 |
| 2026-05-08 | 1143234.87 | 16811.42 | -2583.06 |
| 2026-05-09 | 1157941.60 | 14706.73 | 0.00 |
| 2026-05-10 | 1163786.65 | 5845.04 | 0.00 |
| 2026-05-11 | 1188087.44 | 24300.80 | 0.00 |
| 2026-05-12 | 1211037.61 | 22950.17 | 0.00 |
| 2026-05-13 | 1251888.23 | 40850.61 | 0.00 |
| 2026-05-14 | 1279314.64 | 27426.41 | 0.00 |
| 2026-05-15 | 1341901.79 | 62587.15 | 0.00 |
| 2026-05-16 | 1359365.97 | 17464.17 | 0.00 |
| 2026-05-17 | 1351920.25 | -7445.72 | -7445.72 |
| 2026-05-18 | 1398139.96 | 46219.71 | 0.00 |
| 2026-05-19 | 1438555.40 | 40415.44 | 0.00 |
| 2026-05-20 | 1408020.24 | -30535.16 | -30535.16 |
| 2026-05-21 | 1438494.58 | 30474.34 | -60.82 |
| 2026-05-22 | 1473582.90 | 35088.32 | 0.00 |
| 2026-05-23 | 1495972.13 | 22389.23 | 0.00 |
| 2026-05-24 | 1495898.13 | -73.99 | -73.99 |
| 2026-05-25 | 1506341.48 | 10443.35 | 0.00 |
| 2026-05-26 | 1520077.24 | 13735.76 | 0.00 |
| 2026-05-27 | 1550439.69 | 30362.45 | 0.00 |
| 2026-05-28 | 1597662.49 | 47222.80 | 0.00 |
| 2026-05-29 | 1627905.03 | 30242.54 | 0.00 |
| 2026-05-30 | 1730778.18 | 102873.15 | 0.00 |
| 2026-05-31 | 1685818.10 | -44960.08 | -44960.08 |
| 2026-06-01 | 1753562.33 | 67744.23 | 0.00 |
| 2026-06-02 | 1866561.17 | 112998.85 | 0.00 |
| 2026-06-03 | 1901173.06 | 34611.88 | 0.00 |
| 2026-06-04 | 1987857.83 | 86684.77 | 0.00 |
| 2026-06-05 | 2017834.58 | 29976.75 | 0.00 |
| 2026-06-06 | 2082967.77 | 65133.19 | 0.00 |
| 2026-06-07 | 2134759.12 | 51791.35 | 0.00 |
| 2026-06-08 | 2166589.56 | 31830.45 | 0.00 |
| 2026-06-09 | 2176648.62 | 10059.05 | 0.00 |
| 2026-06-11 | 2178707.00 | 2058.38 | 0.00 |
| 2026-06-12 | 2235321.42 | 56614.42 | 0.00 |
| 2026-06-13 | 2247387.21 | 12065.79 | 0.00 |
| 2026-06-14 | 2278026.36 | 30639.15 | 0.00 |
| 2026-06-15 | 2305137.34 | 27110.98 | 0.00 |
| 2026-06-16 | 2328729.39 | 23592.05 | 0.00 |
| 2026-06-19 | 2340192.58 | 11463.19 | 0.00 |
| 2026-06-20 | 2360560.76 | 20368.18 | 0.00 |
| 2026-06-21 | 2375397.67 | 14836.90 | 0.00 |
| 2026-06-30 | 2364386.93 | -11010.74 | -11010.74 |
| 2026-07-01 | 2367619.10 | 3232.18 | -7778.57 |
| 2026-07-03 | 2398011.86 | 30392.76 | 0.00 |
| 2026-07-04 | 2420730.67 | 22718.80 | 0.00 |
| 2026-07-07 | 2424292.57 | 3561.91 | 0.00 |
| 2026-07-08 | 2455929.11 | 31636.54 | 0.00 |
| 2026-07-11 | 2465946.78 | 10017.67 | 0.00 |
| 2026-07-12 | 2488615.29 | 22668.50 | 0.00 |
| 2026-07-15 | 2496667.79 | 8052.50 | 0.00 |
| 2026-07-16 | 2535649.83 | 38982.04 | 0.00 |
| 2026-07-17 | 2663382.08 | 127732.25 | 0.00 |
| 2026-07-18 | 2697223.26 | 33841.17 | 0.00 |
| 2026-07-19 | 2725446.35 | 28223.09 | 0.00 |
| 2026-07-22 | 2730886.21 | 5439.86 | 0.00 |
| 2026-07-23 | 2745900.23 | 15014.02 | 0.00 |
| 2026-07-24 | 2807238.37 | 61338.14 | 0.00 |
| 2026-07-25 | 2828157.74 | 20919.37 | 0.00 |
| 2026-07-26 | 2872084.33 | 43926.59 | 0.00 |
| 2026-07-27 | 2877598.90 | 5514.56 | 0.00 |
| 2026-07-29 | 2879258.23 | 1659.34 | 0.00 |
| 2026-07-30 | 2912815.91 | 33557.68 | 0.00 |
| 2026-07-31 | 2957281.15 | 44465.24 | 0.00 |
| 2026-08-01 | 2989323.64 | 32042.49 | 0.00 |
| 2026-08-02 | 3047129.10 | 57805.46 | 0.00 |
| 2026-08-03 | 3067828.15 | 20699.05 | 0.00 |
| 2026-08-04 | 3080257.28 | 12429.13 | 0.00 |
| 2026-08-06 | 3104592.97 | 24335.68 | 0.00 |
| 2026-08-07 | 3190148.29 | 85555.32 | 0.00 |
| 2026-08-08 | 3212644.41 | 22496.12 | 0.00 |
| 2026-08-09 | 3238737.90 | 26093.49 | 0.00 |
| 2026-08-10 | 3251242.90 | 12505.00 | 0.00 |
| 2026-08-12 | 3293328.84 | 42085.94 | 0.00 |
| 2026-08-13 | 3330731.18 | 37402.34 | 0.00 |
| 2026-08-14 | 3372047.96 | 41316.78 | 0.00 |
| 2026-08-15 | 3532442.55 | 160394.59 | 0.00 |
| 2026-08-16 | 3608179.92 | 75737.36 | 0.00 |
| 2026-08-17 | 3626562.85 | 18382.94 | 0.00 |
| 2026-08-19 | 3635369.51 | 8806.66 | 0.00 |
| 2026-08-20 | 3644913.22 | 9543.71 | 0.00 |
| 2026-08-21 | 3673112.10 | 28198.88 | 0.00 |
| 2026-08-22 | 3705977.60 | 32865.50 | 0.00 |
| 2026-08-23 | 3740303.01 | 34325.41 | 0.00 |
| 2026-08-24 | 3752581.97 | 12278.96 | 0.00 |
| 2026-08-25 | 3761463.08 | 8881.11 | 0.00 |

</details>

### Top winners / losers contribution

Top10 winners $815,751.94 (10.79% of wins) · Top10 losers -$679,068.23 (17.87% of losses) · PF=1.9658

- WIN $239,727.93 · 2s · LoL: Fnatic vs SK Gaming - Game 2 Winner
- WIN $129,076.88 · 37238s · Dota 2: Aurora vs MOUZ (BO3) - DreamLeague Stage 2
- WIN $103,788.42 · 14838s · LoL: T1 vs Dplus KIA (BO5) - LCK Cup Playoffs
- WIN $66,004.70 · 0s · LoL: Dplus KIA vs DRX - Game 3 Winner
- WIN $48,354.78 · 3766s · Toronto Blue Jays vs. Baltimore Orioles: O/U 7.5
- WIN $47,048.83 · 11384s · Roland Garros ATP: Jakub Mensik vs Andrey Rublev
- WIN $46,860.92 · 0s · Roland Garros WTA: Marta Kostyuk vs Mirra Andreeva
- WIN $45,702.27 · 7980s · LoL: Cloud9 vs FlyQuest (BO3) - LCS Lock In Group Stage
- WIN $44,785.59 · 48s · LoL: DRX vs OKSavingsBank BRION - Game 2 Winner
- WIN $44,401.63 · 9065s · San Diego Padres vs. Washington Nationals: O/U 7.5

- LOSS -$45,213.06 · 100s · LoL: JD Gaming vs Top Esports - Game 2 Winner
- LOSS -$47,509.46 · 178s · LoL: Dplus KIA vs DN Freecs - Game 3 Winner
- LOSS -$49,989.72 · 30052s · Counter-Strike: Vitality vs MOUZ (BO3) - IEM Krakow Playoffs
- LOSS -$52,198.45 · 10512s · LoL: Cloud9 vs LYON (BO5) - LCS Lock In Playoffs
- LOSS -$59,675.53 · 23200s · Counter-Strike: FURIA vs Vitality (BO5) - IEM Krakow Playoffs
- LOSS -$62,131.89 · 82s · LoL: DRX vs Nongshim Red Force - Game 1 Winner
- LOSS -$69,220.58 · 0s · LoL: Cloud9 vs LYON - Game 2 Winner
- LOSS -$81,935.18 · 116s · Will Chelsea FC win on 2026-03-14?
- LOSS -$84,487.84 · 20s · Counter-Strike: paiN vs Passion UA (BO3) - ESL Pro League Stage 1
- LOSS -$126,706.51 · 14298s · Spread: Pistons (-8.5)

## 5. Trade management deep dive

- Adverse early (>2¢): `{'n_early_adverse': 1, 'avg_pnl': 4415.07, 'median_t_first_sell': 82, 'median_hold': 82}`
- Favorable first-sell: `{'n_first_sell_up_2c': 0, 'avg_pnl': None, 'median_mfe_capture': None, 'mean_mfe_capture': None}`
- Campaigns: `{'n': 1, 'pct': 0.06, 'avg_entries': 2, 'pnl': 1245.03, 'avg_pnl': 1245.03, 'win_rate': 1.0, 'single_n': 1579, 'single_pnl': 3760218.05, 'single_avg_pnl': 2381.39}`
- Avg-down: `{'n_losers': 210, 'n_losers_with_red_buys': 27, 'pct_losers': 12.86, 'total_delta_if_skipped_on_losers': 0.0, 'global_fifo_sim': -1372.56, 'global_fifo_never_red_buy': -1372.56, 'global_delta': 0.0}`
- Resolution behavior: `{'flattened_before_flag_rate': 0.6677, 'hold_to_resolution_style_n': 1576, 'redeems_usdc': 15458740.524645988, 'merges_usdc': 0.0}`
- Latency: `{'time_to_mfe_median': None, 'time_to_mfe_p25': None, 'time_to_mfe_p75': None, 'time_to_mfe_p90': None, 'mfe_ge_10c_n': 0, 'mfe_ge_10c_within_30s': 0, 'mfe_ge_10c_within_60s': 0, 'pct_big_within_60s': 0.0}`

### What works / fails
- WORKS: Both-sides inventory on 1.2% of winning markets (losers 2.9%)
- WORKS: Hold bucket <5m: avg PnL $2191.51 on 1379 markets (WR 53%)
- WORKS: Hold bucket 5-30m: avg PnL $1681.11 on 38 markets (WR 61%)
- WORKS: Hold bucket 30m-2h: avg PnL $3215.29 on 61 markets (WR 54%)
- WORKS: Hold bucket 2-12h: avg PnL $4028.91 on 99 markets (WR 62%)
- WORKS: Entry band 0.20-0.40: avg $3193.26 across 382 markets
- WORKS: Entry band 0.40-0.60: avg $1497.63 across 664 markets
- WORKS: Entry band 0.60-0.80: avg $2974.89 across 476 markets
- WORKS: Buy-ladder behavior: fade-into-weakness markets=16, chase-up markets=47

## 6. Strategy overview (in depth)

# Strategy Dossier: SineNooneEI

- **Wallet:** `0x38337de21ff0bb0a11a40761507d51e318d633d1`
- **History span:** 2026-02-03T12:59:50+00:00 → 2026-08-24T17:11:52+00:00 (202.18 days)
- **Trades:** 16,603 (buys 16,599 / sells 4)
- **Markets touched:** 1,580
- **Closed positions:** 1,070

## Headline performance

| Metric | Value |
|---|---|
| Realized cashflow (sells − buys + redeems + rebates) | $541,301.28 |
| Core cashflow (ex-rebates) | $523,137.79 |
| Closed-positions realized sum | $3,761,463.08 |
| Win rate (closed) | 79.53% (851W / 219L) |
| Profit factor | 1.9658 |
| Gross wins / losses | $7,656,000.80 / -$3,894,537.72 |
| Equity max drawdown | -$470,522.99 |
| Polymarket leaderboard (ALL) | $639,212.87 PnL · vol $29,168,764.39 · rank 318 |

## Source validation

- **DRIFT** `polymarket_leaderboard_ALL` pnl: ours=541301.2799 ref=639212.8736756515 diff=-97911.5938
- **MATCH** `polydata` realized_pnl: ours=523137.7892 ref=506308.1 diff=16829.6892
- **DRIFT** `polydata` n_trades: ours=16603 ref=14776 diff=1827
- **DRIFT** `polydata` win_rate: ours=0.7953 ref=0.5312 diff=0.2641
- **DRIFT** `internal` cashflow_vs_closed: ours=541301.2799 ref=3761463.0818 diff=-3220161.8019

## What kind of trader is this?

**Classification:** `hybrid_mm_directional` (score 30/100)

- Fast round-trips (<2h) in 100% of two-sided markets
- High-frequency cadence (median gap 12s)

Supporting rates — both-sides markets: 0.0101, fast round-trips: 1.0, spread-capture rate: 0.0.

## Exact edge thesis

SineNooneEI looks more **directional**: edges concentrate in being right about outcomes rather than harvesting bid-ask. Study their win rate by category and entry timing relative to kickoff / resolution.

See `bot_playbook.md` for the full entry/management/exit autopsy and bot architecture.

## Where the money comes from

- **sports_match**: $3,639,964.63 across 1053 closed legs
- **sports_totals**: $94,457.53 across 16 closed legs
- **other**: $27,040.92 across 1 closed legs

## Timing

- Peak UTC hours: 9, 8, 11, 10, 16
- Peak weekdays (0=Mon): [6, 5, 4]
- Median inter-trade gap: 12s

## Sizing

- Median ticket $29.11, mean $899.07, p90 $2,314.63, max $86,562.02
- Share size median 56.0, mean 1759.377

## Trade-by-trade pattern (representative winners)

These vignettes are reconstructed from fills: average entry, average exit, hold time, and closed realized PnL.

## Top closed winners / losers

**Winners**
- LoL: Fnatic vs SK Gaming - Game 2 Winner: $239,727.93 · bought $6,306.20 · sold $0.00 · hold 2s
- Dota 2: Aurora vs MOUZ (BO3) - DreamLeague Stage 2: $129,076.88 · bought $37,501.90 · sold $0.00 · hold 10h 20m
- LoL: T1 vs Dplus KIA (BO5) - LCK Cup Playoffs: $103,788.42 · bought $56,917.58 · sold $0.00 · hold 4h 7m
- LoL: Dplus KIA vs DRX - Game 3 Winner: $66,004.70 · bought $33,995.31 · sold $0.00 · hold 0s
- Toronto Blue Jays vs. Baltimore Orioles: O/U 7.5: $48,354.78 · bought $50,390.86 · sold $0.00 · hold 1h 2m
- Roland Garros ATP: Jakub Mensik vs Andrey Rublev: $47,048.83 · bought $39,905.08 · sold $0.00 · hold 3h 9m
- Roland Garros WTA: Marta Kostyuk vs Mirra Andreeva: $46,860.92 · bought $36,850.23 · sold $0.00 · hold 0s
- LoL: Cloud9 vs FlyQuest (BO3) - LCS Lock In Group Stage: $45,702.27 · bought $89,898.87 · sold $0.00 · hold 2h 13m
- LoL: DRX vs OKSavingsBank BRION - Game 2 Winner: $44,785.59 · bought $31,202.28 · sold $0.00 · hold 48s
- San Diego Padres vs. Washington Nationals: O/U 7.5: $44,401.63 · bought $46,298.03 · sold $0.00 · hold 2h 31m

**Losers**
- Spread: Pistons (-8.5): -$126,706.51 · bought $77,472.30 · sold $0.00
- Counter-Strike: paiN vs Passion UA (BO3) - ESL Pro League Stage 1: -$84,487.84 · bought $84,487.84 · sold $0.00
- Will Chelsea FC win on 2026-03-14?: -$81,935.18 · bought $81,938.94 · sold $0.00
- LoL: Cloud9 vs LYON - Game 2 Winner: -$69,220.58 · bought $69,220.67 · sold $0.00
- LoL: DRX vs Nongshim Red Force - Game 1 Winner: -$62,131.89 · bought $62,132.06 · sold $0.00
- Counter-Strike: FURIA vs Vitality (BO5) - IEM Krakow Playoffs: -$59,675.53 · bought $59,683.51 · sold $0.00
- LoL: Cloud9 vs LYON (BO5) - LCS Lock In Playoffs: -$52,198.45 · bought $52,198.51 · sold $0.00
- Counter-Strike: Vitality vs MOUZ (BO3) - IEM Krakow Playoffs: -$49,989.72 · bought $50,002.32 · sold $0.00
- LoL: Dplus KIA vs DN Freecs - Game 3 Winner: -$47,509.46 · bought $47,510.56 · sold $0.00
- LoL: JD Gaming vs Top Esports - Game 2 Winner: -$45,213.06 · bought $45,216.49 · sold $0.00

## Replication playbook (how to copy the edge)

1. Restrict to their top categories by PnL contribution.
2. Mirror entry price percentiles and hold-time distribution rather than exact fills.
3. Enforce risk: their profit factor and max DD define a hard stop template.
4. Recompute weekly — edges decay when others copy the same tape.

## Cashflow anatomy

- Buys: $14,979,368.39
- Sells: $43,765.65
- Redeems: $15,458,740.52
- Maker rebates: $5,659.43
- Taker rebates: $12,275.99

_Generated 2026-08-25T21:55:39.321046+00:00_


## 7. Bot / copy playbook

- Difficulty: **9/10** · Ease: **2/10**
- Why: Buy-and-hold / resolution harvesting at large notional. Easy mechanically (buy → wait → redeem) but edge is selection + bankroll + path risk, not a simple rule.

### Build steps
1. Build a directional edge model (not a tape-copy) for the same market universe
2. Enter via maker when possible to cut fees; allow taker for urgency
3. Exit primarily via REDEEM (and MERGE if pairing YES/NO) — no mid-market sell loop required
4. Hard per-market and portfolio max inventory; expect multi-day underwater mark-to-market
5. Paper the full hold-to-resolution cycle including open-risk volatility

### Steal
- Prioritize hold bucket <30s (their PnL engine)

### Avoid
- Averaging down while red on losers
- Their raw size/drawdown — scale down hard
- Blind hold-to-resolution without edge model

Bot parameters: `{'preferred_entry_price_median': 0.57, 'preferred_entry_price_p25_p75': (0.4374, 0.6689), 'target_spread_median': -0.0342, 'target_spread_p75': -0.0101, 'max_hold_seconds_p75': 73, 'median_hold_seconds': 9, 'clip_size_usdc_median': 35.1481, 'clip_size_usdc_p90': 2878.2108, 'both_sides_on_winners_rate': 0.0118, 'require_exit_above_entry': True, 'flatten_before_resolution': True, 'maker_bias': False}`

# Elite Replication Playbook — SineNooneEI

Wallet `0x38337de21ff0bb0a11a40761507d51e318d633d1`. Reverse-engineered from the **full unique fill tape** (16,603 trades · 1,580 markets). This is an implementation spec for a high-end bot, not vibes.

## 0. True strategy identity (read this first)

Classification `hybrid_mm_directional` — mix of spread capture and directional inventory.

Heuristic label from the scanner may still say `likely_market_maker` because of fast round-trips + sell>buy + maker rebates. **Operationally, build a live scalper with optional maker quoting**, not a Yes/No pair inventory bot.

## 1. Performance anchors

| Source / metric | Value |
|---|---|
| Cashflow realized (sells−buys+redeems+rebates) | $541,301.28 |
| Core cashflow (ex-rebates) | $523,137.79 |
| Closed-position legs sum | $3,761,463.08 |
| Leg win rate / profit factor | 79.53% / 1.9658 |
| Polymarket leaderboard ALL | $639,212.87 · vol $29,168,764.39 · rank 318 |
| polymarket_leaderboard_ALL pnl | ref=639212.8736756515 ours=541301.2799 (DRIFT) |
| polydata realized_pnl | ref=506308.1 ours=523137.7892 (MATCH) |
| polydata n_trades | ref=14776 ours=16603 (DRIFT) |
| polydata win_rate | ref=0.5312 ours=0.7953 (DRIFT) |

Notes: Polymarket leaderboard ALL is the primary official PnL check (we match within tolerance). PolyData uses a different event aggregation / trade counting method — expect DRIFT on WR and trade count; use it as a secondary research signal, not the ground truth for fills.

## 2. Universe — where the money is

- **O/U / totals:** 7 markets · $72,156.06 · avg $10,308.01 · median hold 1m36s · median spread None
- **Match / other sports:** 1572 markets · $3,816,013.53 · avg $2,427.49
- **Outcome PnL leaders:**
  - **SK Gaming**: $261,339.00
  - **Dplus KIA**: $238,098.32
  - **Team Yandex**: $235,504.44
  - **Movistar KOI**: $186,135.02
  - **Team Liquid**: $172,912.47
  - **G2 Esports**: $167,039.68

### Bot universe rules

1. Only liquid live sports (soccer/football first — their tape is soccer-heavy).
2. Prefer O/U lines with tight books and active in-game trading.
3. Default bias toward **Over** unless your signal says otherwise (their Over PnL dominates).
4. Skip politics/crypto until you have separate evidence.
5. Require enough depth to enter ~median clip and exit within 1–2 minutes.

## 3. ENTRY — exact mechanics

### Style histogram
- `directional_buy_above_mid`: 560
- `directional_buy_sub_mid`: 541
- `directional_buy_near_mid`: 300
- `directional_buy_expensive_favorite`: 87
- `directional_buy_cheap_tail`: 76
- `two_sided_inventory_near_mid`: 8
- `two_sided_inventory_sub_mid`: 6
- `two_sided_inventory_above_mid`: 2

### First-two-fill sequences
- `BUY->BUY`: 969
- `single_fill`: 610
- `BUY->SELL`: 1

### Entry price → realized edge

| Avg buy band | Markets | Total PnL | Avg PnL |
|---|---:|---:|---:|
| 0.00-0.20 | 29 | $68,889.33 | $2,375.49 |
| 0.20-0.40 | 382 | $1,219,824.16 | $3,193.26 |
| 0.40-0.60 | 664 | $994,426.76 | $1,497.63 |
| 0.60-0.80 | 476 | $1,416,045.47 | $2,974.89 |
| 0.80-1.00 | 29 | $62,277.37 | $2,147.50 |

**Best band:** 0.40–0.60 (near mid) — highest average PnL. Tails (≤0.20 or ≥0.80) make less per market.

### Entry checklist (bot)

1. Clip **$35.15** median (p90 $2,878.21).
2. Aim entry price ~**0.57** (IQR (0.4374, 0.6689)).
3. Trigger = microstructure, not long-term forecast:
   - mid dips / liquidity hole you can buy
   - imminent volatility (attack, corner, shot) where Over can jump
   - resting bid gets lifted? you’re being taken — manage immediately
4. Prefer **maker bids**; take only if the expected jump already started and ask is still inside your edge.
5. Same-second multi-fills are normal (one order, many counterparties) — treat as one decision, many fills.

## 4. MANAGEMENT — what they do after entry

### Styles
- `single_clip`: 744
- `scalp_sub_15m`: 674
- `multi_hour_position`: 91
- `intraday_swing`: 71

### Winners vs losers

| Metric | Winners | Losers |
|---|---:|---:|
| N | 845 | 210 |
| PnL | $7,560,464.40 | -$3,799,001.32 |
| Median hold | 9s | 53s |
| Median spread | -0.0342 | None |
| Scale-in rate | 0.6225 | 0.7524 |
| Scale-out rate | 0.0 | 0.0 |
| Avg fills/market | 10.07 | 20.71 |
| Both-sides rate | 0.0118 | 0.0286 |

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

- **Winners** sell above buy (median spread **-0.0342**). **Losers** often exit worse (median spread **None**).
- Losers scale-in **more** (0.7524 vs 0.6225) — averaging down is how they bleed; the bot should **forbid** revenge scale-ins without a fresh signal.
- Hold edge peaks in **<5m** ({'n': 1379, 'pnl': 3022086.8724, 'avg': 2191.5061, 'win_rate': 0.5257}) and a strong **30m–2h** bucket for the larger in-game campaigns.

## 5. EXIT — rules that print

- `hold_to_resolution_or_redeem`: 1576
- `adverse_exit_sell_below_buy`: 3
- `mixed_roundtrip`: 1

| Hold bucket | N | Total PnL | Avg | Win rate |
|---|---:|---:|---:|---:|
| <5m | 1379 | $3,022,086.87 | $2,191.51 | 52.6% |
| 5-30m | 38 | $63,882.16 | $1,681.11 | 60.5% |
| 30m-2h | 61 | $196,132.74 | $3,215.29 | 54.1% |
| 2-12h | 99 | $398,861.98 | $4,028.91 | 61.6% |
| 12h+ | 3 | $80,499.33 | $26,833.11 | 100.0% |

### Exit engine params

1. **TP / ask distance:** target ≈ **-0.0342** above avg entry (p75 stretch -0.0101). On live O/U this is often a burst move, not slow grind.
2. **Time stop:** median hold 9s; p75 1m13s for the scalps — escalate urgency after that.
3. **Scale-out:** peel into strength (their winners stack sells). Don’t wait for one perfect print.
4. **Stop:** if mid < entry − ~3–5¢ on unhedged inventory with no signal → take the loss (copy losers’ speed, not their hope).
5. **Flatten before resolution** — redeem is residual.
6. Taker exits are fine when the move already happened and maker asks won’t fill.

## 6. What works / what fails

### Works
- Both-sides inventory on 1.2% of winning markets (losers 2.9%)
- Hold bucket <5m: avg PnL $2191.51 on 1379 markets (WR 53%)
- Hold bucket 5-30m: avg PnL $1681.11 on 38 markets (WR 61%)
- Hold bucket 30m-2h: avg PnL $3215.29 on 61 markets (WR 54%)
- Hold bucket 2-12h: avg PnL $4028.91 on 99 markets (WR 62%)
- Entry band 0.20-0.40: avg $3193.26 across 382 markets
- Entry band 0.40-0.60: avg $1497.63 across 664 markets
- Entry band 0.60-0.80: avg $2974.89 across 476 markets
- Buy-ladder behavior: fade-into-weakness markets=16, chase-up markets=47

### Fails
- (no strong negative bucket)
- Chase vs fade ladders: `{'chase_up': 47, 'fade_down': 16}`

## 7. Fill-by-fill autopsies (copy these patterns)

## 8. Failure modes (do not bot these)

1. **Spread: Pistons (-8.5)** -$126,706.51 · hold 3h58m · entry 0.4964 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
2. **Counter-Strike: paiN vs Passion UA (BO3) - ESL Pro League Stage 1** -$84,487.84 · hold 20s · entry 0.57 → exit None · `single_clip` / `hold_to_resolution_or_redeem`
3. **Will Chelsea FC win on 2026-03-14?** -$81,935.18 · hold 1m56s · entry 0.5672 → exit None · `scalp_sub_15m` / `hold_to_resolution_or_redeem`
4. **LoL: Cloud9 vs LYON - Game 2 Winner** -$69,220.58 · hold 0s · entry 0.6898 → exit None · `single_clip` / `hold_to_resolution_or_redeem`
5. **LoL: DRX vs Nongshim Red Force - Game 1 Winner** -$62,131.89 · hold 1m22s · entry 0.6213 → exit None · `scalp_sub_15m` / `hold_to_resolution_or_redeem`
6. **Counter-Strike: FURIA vs Vitality (BO5) - IEM Krakow Playoffs** -$59,675.53 · hold 6h26m · entry 0.3324 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
7. **LoL: Cloud9 vs LYON (BO5) - LCS Lock In Playoffs** -$52,198.45 · hold 2h55m · entry 0.6989 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
8. **Counter-Strike: Vitality vs MOUZ (BO3) - IEM Krakow Playoffs** -$49,989.72 · hold 8h20m · entry 0.3498 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
9. **LoL: Dplus KIA vs DN Freecs - Game 3 Winner** -$47,509.46 · hold 2m58s · entry 0.5985 → exit None · `scalp_sub_15m` / `hold_to_resolution_or_redeem`
10. **LoL: JD Gaming vs Top Esports - Game 2 Winner** -$45,213.06 · hold 1m40s · entry 0.419 → exit None · `scalp_sub_15m` / `hold_to_resolution_or_redeem`

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
   - default post-only bids/asks; clip $35.15
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
template: SineNooneEI
mode: one_sided_live_scalper  # not classic two-sided MM
preferred_outcome_bias: Over
clip_usdc_median: 35.1481
clip_usdc_p90: 2878.2108
entry_price_median: 0.57
entry_price_iqr: (0.4374, 0.6689)
target_spread: -0.0342
target_spread_p75: -0.0101
median_hold_seconds: 9
max_hold_seconds_p75: 73
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

_Generated 2026-08-25T21:55:39.321164+00:00_


## 8. Structured autopsy (A–G)

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


## 9. Hour / DOW volume (UTC)

| Hour | USDC volume |
|---:|---:|
| 0 | 146759.41 |
| 1 | 3239.41 |
| 2 | 4155.54 |
| 3 | 3916.91 |
| 4 | 19358.82 |
| 5 | 34539.15 |
| 6 | 71059.1 |
| 7 | 909791.06 |
| 8 | 2021891.51 |
| 9 | 1824454.32 |
| 10 | 1410353.33 |
| 11 | 1417132.63 |
| 12 | 1044200.29 |
| 13 | 703634.48 |
| 14 | 717332.58 |
| 15 | 706711.13 |
| 16 | 946431.39 |
| 17 | 830790.81 |
| 18 | 767318.77 |
| 19 | 479680.35 |
| 20 | 338723.49 |
| 21 | 110716.48 |
| 22 | 270494.78 |
| 23 | 144580.06 |

| DOW (0=Mon) | USDC volume |
|---:|---:|
| 0 | 1250293.06 |
| 1 | 1608565.24 |
| 2 | 1426339.81 |
| 3 | 1627213.46 |
| 4 | 2434964.22 |
| 5 | 3003127.02 |
| 6 | 3576763.0 |

## 10. Bot schema pointer

Parse `MASTER.json` keys: `reconciliation`, `identity`, `performance`, `extras`, `copyability`, `equity_curve_daily`, `deep_dive_highlights`.
