# MASTER AUTOPSY — DrPufferfish

> Single file for humans **and** bots. Machine-readable twin: `MASTER.json` · Equity: `equity_curve.csv`.

- Wallet: `0xdb27bf2ac5d428a9c63dbc914611036855a6c56e`
- Generated: `2026-08-28T14:18:32.071453+00:00`
- Identity class: **`hybrid_liquidity_scalper`**

## 0. Executive verdict

This trader is classified as **hybrid_liquidity_scalper** with primary focus **sports_match**. Preferred PnL (**cashflow_core**) **$4,175,613.54** (leaderboard ALL $4,055,413.26; MATCH). Unique trades **64,290**. Copy difficulty **6/10** · ease **5/10**. Maker-led entries reduce latency race; still needs solid risk + universe selection.

**Exit mechanics:** `sell_secondary_market`
**Kalshi two-sided MM fit:** MEDIUM-HIGH — maker entries transfer well; add explicit both-sides module
**Preferred PnL note:** Cashflow usually tracks leaderboard for buy+sell scalpers.

## 1. Reconciliation (mandatory)

| Source | PnL | Extra |
|---|---:|---|
| **Preferred (cashflow_core)** | **$4,175,613.54** | vs LB diff=120200.29 |
| Ours cashflow realized | $4,176,633.54 | trades=64,290 buy_only=False |
| Ours core (ex-rebate) | $4,175,613.54 | WR legs=90.22% |
| Ours closed-legs sum | $46,297,730.97 | PF=21.0256 |
| Polymarket leaderboard ALL | $4,055,413.26 | vol=$248,548,251.18 rank=30 |
| PolyData | $4,055,413.26 | trades=272027 WR=0.481 |

- MATCH: `polymarket_leaderboard_ALL` pnl ours=4175613.5447 field=cashflow_core ref=4055413.259574452 diff=120200.2851
- MATCH: `polydata` realized_pnl ours=4175613.5447 field=cashflow_core ref=4055413.26 diff=120200.2847
- DRIFT: `polydata` n_trades ours=64290 field=None ref=272027 diff=-207737
- DRIFT: `polydata` win_rate ours=0.9022 field=None ref=0.481 diff=0.4212
- DRIFT: `internal` cashflow_vs_closed ours=4176633.543 field=None ref=46297730.9682 diff=-42121097.4252

## 2. Identity & microstructure

- Both-sides rate: 11.27% (81 markets)
- Clip median/p90/max: $1.98 / $108.42 / $248,000.00
- Category PnL: `{'sports_match': 12701974.54, 'sports_totals': 501166.19, 'other': 198386.06, 'crypto': 51128.55}`
- Start BUY first: 697 · SELL first: 22
- Entry maker/taker: 77.64% / 22.36% (60,385/491 fills)
- Exit maker/taker: 80.21% / 19.79% (3,367/47 fills)
- Patterns: `{'enter_maker_exit_maker': 55, 'enter_maker_exit_taker': 17, 'enter_taker_exit_taker': 8, 'enter_taker_exit_maker': 4}`

### Outcome volume (top)

| Outcome | Buy USDC | Sell USDC | Sell−Buy |
|---|---:|---:|---:|
| No | $4,394,917.22 | $253,316.71 | -$4,141,600.50 |
| Yes | $1,508,070.22 | $229,229.10 | -$1,278,841.12 |
| Grizzlies | $1,310,233.89 | $4,117.36 | -$1,306,116.53 |
| Nets | $1,155,583.33 | $153,438.19 | -$1,002,145.15 |
| Hawks | $1,262,832.77 | $38,083.17 | -$1,224,749.60 |
| Celtics | $1,112,036.75 | $0.00 | -$1,112,036.75 |
| Knicks | $846,718.74 | $43,838.77 | -$802,879.97 |
| Heat | $846,818.74 | $2,695.93 | -$844,122.81 |
| 76ers | $687,460.75 | $53,691.95 | -$633,768.80 |
| Hornets | $689,601.91 | $2,420.66 | -$687,181.25 |
| Warriors | $621,835.51 | $4,491.62 | -$617,343.88 |
| Pacers | $495,181.83 | $78,529.52 | -$416,652.32 |

## 3. Performance metrics (kitchen sink)

- Expectancy / market: $33,631.64
- Avg win / avg loss: $41,225.47 / -$26,275.24 · ratio=1.569
- PnL / day: $18,318.57 · trades/day=281.97 · markets/day=3.15
- PnL concentration HHI: 0.009557 (higher=more concentrated)
- Notional sum: $26,713,058.11 · median ticket $1.98
- Buy price median: 0.11 · Sell price median: 0.042
- Activity types: `{'DEPOSIT': 25, 'TRADE': 64290, 'REWARD': 36, 'REDEEM': 380, 'CONVERSION': 4, 'WITHDRAWAL': 35}`
- Open risk: `{'n': 848, 'cash_pnl': -45465201.49, 'current_value': 0.0, 'redeemable': 848}`

### Hold-time engine

| Bucket | N | WR | Total PnL | Avg | Median |
|---|---:|---:|---:|---:|---:|
| <30s | 181 | 89.29% | $2,124,933.99 | $11,739.97 | $42.75 |
| 30s-2m | 37 | 100.00% | $669,395.66 | $18,091.77 | $24.23 |
| 2-5m | 41 | 100.00% | $944,608.13 | $23,039.22 | $894.72 |
| 5-15m | 68 | 89.19% | $847,113.77 | $12,457.56 | $0.00 |
| 15m+ | 392 | 86.12% | $8,866,603.79 | $22,618.89 | $0.00 |

### Entry price bands

| Band | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| 0-20¢ | 127 | 74.19% | $1,108,752.75 | $8,730.34 |
| 20-40¢ | 151 | 89.71% | $4,540,068.24 | $30,066.68 |
| 40-60¢ | 266 | 91.62% | $6,532,097.53 | $24,556.76 |
| 60-80¢ | 113 | 97.67% | $1,356,925.63 | $12,008.19 |
| 80-100¢ | 42 | 97.06% | $144,351.35 | $3,436.94 |

### Family

| Family | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| Yes/No moneyline | 332 | 85.25% | $2,807,111.09 | $8,455.15 |
| Other | 375 | 91.55% | $10,619,619.38 | $28,318.99 |
| Over/Under | 12 | 100.00% | $25,924.87 | $2,160.41 |

## 4. Equity curve (critical)

### 4a. Cashflow activity equity

- Final equity (cashflow): **$4,176,633.54**
- Max DD: **-$1,021,203.64** (-195.04% of peak)
- Longest DD: **0 days**
- Daily Sharpe (ann.): **2.377**
- Days: 112

Files: `equity_curve.csv` · `equity_curve.json` (source=`cashflow_activity`)

<details><summary>Daily cashflow equity table (full)</summary>

| Date | Equity | Daily PnL | Drawdown |
|---|---:|---:|---:|
| 2025-05-29 | -468.15 | -468.15 | -468.15 |
| 2025-05-30 | -24924.76 | -24456.61 | -24924.76 |
| 2025-05-31 | -133933.37 | -109008.61 | -133933.37 |
| 2025-06-01 | -114580.00 | 19353.37 | -114580.00 |
| 2025-06-02 | -114589.69 | -9.69 | -114589.69 |
| 2025-06-03 | -112136.78 | 2452.92 | -112136.78 |
| 2025-06-04 | -112683.58 | -546.80 | -112683.58 |
| 2025-06-05 | -112705.00 | -21.43 | -112705.00 |
| 2025-06-06 | -141716.37 | -29011.37 | -141716.37 |
| 2025-07-22 | -142315.82 | -599.45 | -142315.82 |
| 2025-07-23 | -56386.30 | 85929.52 | -56386.30 |
| 2025-07-25 | -53421.55 | 2964.75 | -53421.55 |
| 2025-07-29 | -311785.05 | -258363.50 | -311785.05 |
| 2025-09-08 | -371778.54 | -59993.49 | -371778.54 |
| 2025-09-09 | -402946.26 | -31167.72 | -402946.26 |
| 2025-09-10 | -249509.77 | 153436.49 | -249509.77 |
| 2025-09-11 | -303550.46 | -54040.69 | -303550.46 |
| 2025-09-12 | -406857.57 | -103307.11 | -406857.57 |
| 2025-09-13 | -129339.07 | 277518.50 | -129339.07 |
| 2025-09-14 | -87277.14 | 42061.93 | -87277.14 |
| 2025-09-15 | -342805.86 | -255528.71 | -342805.86 |
| 2025-09-16 | -559544.00 | -216738.14 | -559544.00 |
| 2025-09-17 | -550391.48 | 9152.52 | -550391.48 |
| 2025-09-18 | -565240.21 | -14848.73 | -565240.21 |
| 2025-09-20 | -580186.13 | -14945.92 | -580186.13 |
| 2025-09-21 | -595079.80 | -14893.67 | -595079.80 |
| 2025-09-25 | -673828.58 | -78748.78 | -673828.58 |
| 2025-09-28 | -669070.80 | 4757.77 | -669070.80 |
| 2025-10-01 | -553515.81 | 115555.00 | -553515.81 |
| 2025-10-06 | -561841.80 | -8325.99 | -561841.80 |
| 2025-10-07 | -572506.50 | -10664.70 | -572506.50 |
| 2025-10-08 | -623043.09 | -50536.59 | -623043.09 |
| 2025-10-09 | -620979.17 | 2063.91 | -620979.17 |
| 2025-10-10 | -721241.81 | -100262.63 | -721241.81 |
| 2025-10-11 | -716912.71 | 4329.10 | -716912.71 |
| 2025-10-12 | -859403.80 | -142491.09 | -859403.80 |
| 2025-10-13 | -751722.37 | 107681.43 | -751722.37 |
| 2025-10-14 | -760292.60 | -8570.23 | -760292.60 |
| 2025-10-15 | -760950.82 | -658.22 | -760950.82 |
| 2025-10-16 | -778530.46 | -17579.64 | -778530.46 |
| 2025-10-17 | -778038.31 | 492.15 | -778038.31 |
| 2025-10-18 | -778050.23 | -11.92 | -778050.23 |
| 2025-10-19 | -856861.89 | -78811.66 | -856861.89 |
| 2025-10-20 | -856860.13 | 1.76 | -856860.13 |
| 2025-10-21 | -859406.80 | -2546.68 | -859406.80 |
| 2025-10-22 | -832381.92 | 27024.89 | -832381.92 |
| 2025-10-23 | -832354.16 | 27.76 | -832354.16 |
| 2025-10-24 | -772865.51 | 59488.65 | -772865.51 |
| 2025-10-25 | -772851.21 | 14.31 | -772851.21 |
| 2025-11-04 | -859406.74 | -86555.54 | -859406.74 |
| 2025-11-05 | -541684.57 | 317722.17 | -541684.57 |
| 2025-11-08 | -711433.24 | -169748.67 | -711433.24 |
| 2025-11-09 | -711128.00 | 305.24 | -711128.00 |
| 2025-11-10 | -711125.75 | 2.25 | -711125.75 |
| 2025-11-11 | -628203.44 | 82922.31 | -628203.44 |
| 2025-11-12 | -692087.30 | -63883.87 | -692087.30 |
| 2025-11-13 | -724545.01 | -32457.71 | -724545.01 |
| 2025-11-14 | -614863.50 | 109681.52 | -614863.50 |
| 2025-11-15 | -651699.14 | -36835.65 | -651699.14 |
| 2025-11-16 | -790824.52 | -139125.38 | -790824.52 |
| 2025-11-17 | -756375.57 | 34448.95 | -756375.57 |
| 2025-11-18 | -628455.03 | 127920.54 | -628455.03 |
| 2025-11-19 | -543395.43 | 85059.61 | -543395.43 |
| 2025-11-20 | -670264.70 | -126869.28 | -670264.70 |
| 2025-11-21 | -530702.96 | 139561.74 | -530702.96 |
| 2025-11-22 | -669855.20 | -139152.24 | -669855.20 |
| 2025-11-23 | -560953.95 | 108901.26 | -560953.95 |
| 2025-11-24 | -561424.95 | -471.01 | -561424.95 |
| 2025-11-25 | -504471.74 | 56953.21 | -504471.74 |
| 2025-12-01 | -418802.07 | 85669.67 | -418802.07 |
| 2025-12-02 | -376013.68 | 42788.39 | -376013.68 |
| 2025-12-03 | -714413.01 | -338399.33 | -714413.01 |
| 2025-12-04 | -371271.25 | 343141.76 | -371271.25 |
| 2025-12-05 | -329861.05 | 41410.19 | -329861.05 |
| 2025-12-06 | -337359.71 | -7498.66 | -337359.71 |
| 2025-12-07 | 43248.16 | 380607.87 | 0.00 |
| 2025-12-08 | 122424.88 | 79176.72 | 0.00 |
| 2025-12-09 | 91854.40 | -30570.48 | -30570.48 |
| 2025-12-10 | -104548.52 | -196402.92 | -226973.40 |
| 2025-12-11 | 390593.91 | 495142.43 | 0.00 |
| 2025-12-12 | 282471.66 | -108122.25 | -108122.25 |
| 2025-12-13 | -74293.88 | -356765.54 | -464887.79 |
| 2025-12-14 | -219902.09 | -145608.21 | -610495.99 |
| 2025-12-15 | -348657.13 | -128755.04 | -739251.03 |
| 2025-12-16 | -254732.26 | 93924.87 | -645326.17 |
| 2025-12-17 | -297970.70 | -43238.44 | -688564.61 |
| 2025-12-18 | -302476.86 | -4506.16 | -693070.76 |
| 2025-12-19 | -371231.65 | -68754.80 | -761825.56 |
| 2025-12-20 | -279063.67 | 92167.98 | -669657.58 |
| 2025-12-21 | 260461.48 | 539525.15 | -130132.42 |
| 2025-12-22 | 142976.78 | -117484.70 | -247617.13 |
| 2025-12-23 | 77836.39 | -65140.39 | -312757.52 |
| 2025-12-24 | 815887.39 | 738051.00 | 0.00 |
| 2025-12-25 | 569639.46 | -246247.93 | -246247.93 |
| 2025-12-26 | 761616.88 | 191977.42 | -54270.51 |
| 2025-12-27 | 904460.04 | 142843.16 | 0.00 |
| 2025-12-28 | 868072.29 | -36387.75 | -36387.75 |
| 2025-12-29 | 865637.87 | -2434.41 | -38822.17 |
| 2025-12-30 | 750026.65 | -115611.22 | -154433.39 |
| 2025-12-31 | 1682357.34 | 932330.68 | 0.00 |
| 2026-01-01 | 2033050.03 | 350692.69 | 0.00 |
| 2026-01-02 | 2392739.28 | 359689.25 | 0.00 |
| 2026-01-03 | 2473620.52 | 80881.24 | 0.00 |
| 2026-01-04 | 2835445.57 | 361825.05 | 0.00 |
| 2026-01-05 | 2445887.64 | -389557.93 | -389557.93 |
| 2026-01-06 | 2745141.70 | 299254.06 | -90303.87 |
| 2026-01-07 | 2158556.05 | -586585.65 | -676889.52 |
| 2026-01-08 | 3088151.66 | 929595.61 | 0.00 |
| 2026-01-09 | 3088930.09 | 778.42 | 0.00 |
| 2026-01-10 | 2615225.54 | -473704.55 | -473704.55 |
| 2026-01-11 | 2067726.44 | -547499.10 | -1021203.64 |
| 2026-01-12 | 4176633.54 | 2108907.10 | 0.00 |

</details>

### 4b. Closed-positions equity (alt — critical for buy-only books)

- Final closed equity: **$46,297,730.97**
- Max DD: **-$274,872.64**
- Daily Sharpe (ann.): **13.682**
- Days: 174

Files: `equity_curve_closed.csv` · `equity_curve_closed.json` (source=`closed_positions`)

<details><summary>Daily closed equity table (full)</summary>

| Date | Equity | Daily PnL | Drawdown |
|---|---:|---:|---:|
| 2025-05-30 | -9239.28 | -9239.28 | -9239.28 |
| 2025-05-31 | -79309.46 | -70070.17 | -79309.46 |
| 2025-06-01 | -68968.49 | 10340.97 | -68968.49 |
| 2025-06-02 | -68979.13 | -10.65 | -68979.13 |
| 2025-06-06 | -68960.13 | 19.00 | -68960.13 |
| 2025-06-08 | -54653.65 | 14306.48 | -54653.65 |
| 2025-07-23 | 42544.72 | 97198.37 | 0.00 |
| 2025-07-25 | 45509.47 | 2964.75 | 0.00 |
| 2025-09-09 | 132422.30 | 86912.83 | 0.00 |
| 2025-09-10 | 133565.23 | 1142.93 | 0.00 |
| 2025-09-12 | 234547.05 | 100981.82 | 0.00 |
| 2025-09-13 | 355170.55 | 120623.50 | 0.00 |
| 2025-09-14 | 585786.52 | 230615.97 | 0.00 |
| 2025-09-15 | 524012.49 | -61774.03 | -61774.03 |
| 2025-09-16 | 549594.53 | 25582.05 | -36191.99 |
| 2025-09-17 | 549944.25 | 349.71 | -35842.27 |
| 2025-09-18 | 633824.54 | 83880.29 | 0.00 |
| 2025-09-19 | 651323.92 | 17499.38 | 0.00 |
| 2025-09-20 | 671310.35 | 19986.43 | 0.00 |
| 2025-09-21 | 683064.57 | 11754.22 | 0.00 |
| 2025-09-25 | 691645.58 | 8581.01 | 0.00 |
| 2025-09-26 | 734438.14 | 42792.56 | 0.00 |
| 2025-09-29 | 787593.43 | 53155.30 | 0.00 |
| 2025-10-08 | 760149.32 | -27444.11 | -27444.11 |
| 2025-10-11 | 512720.79 | -247428.53 | -274872.64 |
| 2025-10-12 | 528652.25 | 15931.46 | -258941.18 |
| 2025-10-13 | 546863.42 | 18211.17 | -240730.02 |
| 2025-10-18 | 546892.45 | 29.03 | -240700.98 |
| 2025-10-19 | 557316.83 | 10424.38 | -230276.61 |
| 2025-10-21 | 527644.91 | -29671.92 | -259948.52 |
| 2025-10-22 | 557690.14 | 30045.23 | -229903.30 |
| 2025-11-02 | 560841.74 | 3151.60 | -226751.70 |
| 2025-11-04 | 673841.37 | 112999.63 | -113752.06 |
| 2025-11-05 | 776539.99 | 102698.62 | -11053.45 |
| 2025-11-08 | 718061.18 | -58478.81 | -69532.25 |
| 2025-11-12 | 772601.31 | 54540.13 | -14992.12 |
| 2025-11-13 | 819127.80 | 46526.49 | 0.00 |
| 2025-11-15 | 823147.82 | 4020.02 | 0.00 |
| 2025-11-16 | 900156.60 | 77008.78 | 0.00 |
| 2025-11-17 | 900198.08 | 41.48 | 0.00 |
| 2025-11-18 | 956803.38 | 56605.31 | 0.00 |
| 2025-11-19 | 1006526.49 | 49723.10 | 0.00 |
| 2025-11-21 | 1101017.19 | 94490.70 | 0.00 |
| 2025-11-22 | 1298622.90 | 197605.71 | 0.00 |
| 2025-11-23 | 1370998.04 | 72375.15 | 0.00 |
| 2025-11-24 | 1483556.70 | 112558.65 | 0.00 |
| 2025-11-26 | 1667224.09 | 183667.39 | 0.00 |
| 2025-12-02 | 1669288.59 | 2064.50 | 0.00 |
| 2025-12-03 | 1671628.50 | 2339.91 | 0.00 |
| 2025-12-04 | 1966391.65 | 294763.15 | 0.00 |
| 2025-12-05 | 2168358.00 | 201966.35 | 0.00 |
| 2025-12-06 | 2365285.11 | 196927.11 | 0.00 |
| 2025-12-07 | 2792862.81 | 427577.70 | 0.00 |
| 2025-12-08 | 2928995.53 | 136132.72 | 0.00 |
| 2025-12-09 | 3064644.55 | 135649.02 | 0.00 |
| 2025-12-10 | 3267843.59 | 203199.04 | 0.00 |
| 2025-12-11 | 3643838.22 | 375994.62 | 0.00 |
| 2025-12-12 | 3753336.20 | 109497.98 | 0.00 |
| 2025-12-13 | 3765599.62 | 12263.42 | 0.00 |
| 2025-12-14 | 3781859.16 | 16259.54 | 0.00 |
| 2025-12-15 | 3784777.88 | 2918.72 | 0.00 |
| 2025-12-16 | 3743538.57 | -41239.31 | -41239.31 |
| 2025-12-18 | 3842166.51 | 98627.94 | 0.00 |
| 2025-12-19 | 3916491.95 | 74325.44 | 0.00 |
| 2025-12-20 | 4077593.12 | 161101.18 | 0.00 |
| 2025-12-21 | 4378117.22 | 300524.09 | 0.00 |
| 2025-12-23 | 4461195.03 | 83077.81 | 0.00 |
| 2025-12-24 | 5086107.81 | 624912.78 | 0.00 |
| 2025-12-25 | 5089132.17 | 3024.36 | 0.00 |
| 2025-12-26 | 5455069.42 | 365937.26 | 0.00 |
| 2025-12-27 | 5776502.92 | 321433.50 | 0.00 |
| 2025-12-28 | 6198621.00 | 422118.07 | 0.00 |
| 2025-12-29 | 6209074.03 | 10453.03 | 0.00 |
| 2025-12-30 | 6673229.92 | 464155.90 | 0.00 |
| 2025-12-31 | 7327508.32 | 654278.39 | 0.00 |
| 2026-01-01 | 7885090.22 | 557581.90 | 0.00 |
| 2026-01-02 | 8341605.14 | 456514.92 | 0.00 |
| 2026-01-03 | 9082367.69 | 740762.55 | 0.00 |
| 2026-01-04 | 9539245.37 | 456877.68 | 0.00 |
| 2026-01-05 | 9708022.93 | 168777.56 | 0.00 |
| 2026-01-06 | 10169335.93 | 461313.00 | 0.00 |
| 2026-01-07 | 10394630.31 | 225294.38 | 0.00 |
| 2026-01-08 | 11144648.29 | 750017.98 | 0.00 |
| 2026-01-09 | 11237626.57 | 92978.27 | 0.00 |
| 2026-01-10 | 11306413.33 | 68786.77 | 0.00 |
| 2026-01-11 | 11476512.41 | 170099.08 | 0.00 |
| 2026-01-12 | 12732569.54 | 1256057.13 | 0.00 |
| 2026-01-14 | 13183368.56 | 450799.02 | 0.00 |
| 2026-01-15 | 13384132.57 | 200764.01 | 0.00 |
| 2026-01-16 | 14059770.06 | 675637.49 | 0.00 |
| 2026-01-17 | 14069292.98 | 9522.92 | 0.00 |
| 2026-01-18 | 14658239.89 | 588946.91 | 0.00 |
| 2026-01-19 | 14742982.68 | 84742.79 | 0.00 |
| 2026-01-20 | 15304585.18 | 561602.50 | 0.00 |
| 2026-01-21 | 16235066.23 | 930481.05 | 0.00 |
| 2026-01-22 | 16344798.06 | 109731.83 | 0.00 |
| 2026-01-23 | 16666954.77 | 322156.71 | 0.00 |
| 2026-01-24 | 16865873.70 | 198918.94 | 0.00 |
| 2026-01-25 | 17293546.06 | 427672.36 | 0.00 |
| 2026-01-26 | 17427771.16 | 134225.09 | 0.00 |
| 2026-01-27 | 17600536.74 | 172765.58 | 0.00 |
| 2026-01-28 | 17888541.83 | 288005.09 | 0.00 |
| 2026-01-29 | 18679639.27 | 791097.44 | 0.00 |
| 2026-01-30 | 18921695.06 | 242055.79 | 0.00 |
| 2026-01-31 | 19852711.41 | 931016.35 | 0.00 |
| 2026-02-01 | 19861341.89 | 8630.48 | 0.00 |
| 2026-02-02 | 20139418.92 | 278077.03 | 0.00 |
| 2026-02-03 | 20513139.88 | 373720.96 | 0.00 |
| 2026-02-04 | 20796227.48 | 283087.60 | 0.00 |
| 2026-02-05 | 20885186.89 | 88959.41 | 0.00 |
| 2026-02-06 | 21154835.75 | 269648.86 | 0.00 |
| 2026-02-09 | 22394441.00 | 1239605.25 | 0.00 |
| 2026-02-10 | 23126264.96 | 731823.96 | 0.00 |
| 2026-02-11 | 24749580.13 | 1623315.17 | 0.00 |
| 2026-02-12 | 25249693.61 | 500113.48 | 0.00 |
| 2026-02-13 | 25287911.64 | 38218.02 | 0.00 |
| 2026-02-14 | 25381356.70 | 93445.07 | 0.00 |
| 2026-02-17 | 25681365.95 | 300009.24 | 0.00 |
| 2026-02-18 | 25718699.15 | 37333.20 | 0.00 |
| 2026-02-20 | 26889502.02 | 1170802.87 | 0.00 |
| 2026-02-21 | 28701365.22 | 1811863.20 | 0.00 |
| 2026-02-22 | 30022501.61 | 1321136.39 | 0.00 |
| 2026-02-23 | 31092439.49 | 1069937.88 | 0.00 |
| 2026-02-24 | 31092915.84 | 476.35 | 0.00 |
| 2026-02-25 | 32399113.68 | 1306197.85 | 0.00 |
| 2026-02-26 | 33017841.39 | 618727.70 | 0.00 |
| 2026-02-27 | 33870203.88 | 852362.49 | 0.00 |
| 2026-02-28 | 33877491.07 | 7287.19 | 0.00 |
| 2026-03-01 | 34089699.42 | 212208.36 | 0.00 |
| 2026-03-02 | 34092511.66 | 2812.24 | 0.00 |
| 2026-03-03 | 34319087.50 | 226575.84 | 0.00 |
| 2026-03-04 | 35732129.47 | 1413041.96 | 0.00 |
| 2026-03-05 | 36029051.06 | 296921.59 | 0.00 |
| 2026-03-06 | 36111050.66 | 81999.60 | 0.00 |
| 2026-03-08 | 37588155.73 | 1477105.07 | 0.00 |
| 2026-03-09 | 39046576.47 | 1458420.74 | 0.00 |
| 2026-03-10 | 39459034.64 | 412458.17 | 0.00 |
| 2026-03-11 | 39987970.20 | 528935.56 | 0.00 |
| 2026-03-16 | 40573912.60 | 585942.40 | 0.00 |
| 2026-03-17 | 40605792.56 | 31879.96 | 0.00 |
| 2026-03-19 | 40894238.32 | 288445.76 | 0.00 |
| 2026-03-21 | 41006571.26 | 112332.94 | 0.00 |
| 2026-03-22 | 41046910.49 | 40339.24 | 0.00 |
| 2026-03-23 | 41362267.82 | 315357.32 | 0.00 |
| 2026-03-24 | 41496169.19 | 133901.37 | 0.00 |
| 2026-03-25 | 41504423.09 | 8253.90 | 0.00 |
| 2026-03-26 | 41894207.56 | 389784.48 | 0.00 |
| 2026-03-27 | 41899070.49 | 4862.93 | 0.00 |
| 2026-03-28 | 41903242.54 | 4172.05 | 0.00 |
| 2026-04-09 | 41986037.50 | 82794.96 | 0.00 |
| 2026-04-11 | 41990669.93 | 4632.43 | 0.00 |
| 2026-04-12 | 41991219.41 | 549.48 | 0.00 |
| 2026-04-13 | 43012345.51 | 1021126.10 | 0.00 |
| 2026-04-14 | 43082831.07 | 70485.56 | 0.00 |
| 2026-04-15 | 43559582.84 | 476751.77 | 0.00 |
| 2026-04-16 | 44143410.15 | 583827.30 | 0.00 |
| 2026-04-18 | 44446837.93 | 303427.78 | 0.00 |
| 2026-04-19 | 44626461.35 | 179623.42 | 0.00 |
| 2026-04-20 | 44628791.15 | 2329.81 | 0.00 |
| 2026-04-22 | 44654551.60 | 25760.44 | 0.00 |
| 2026-04-24 | 44919182.08 | 264630.48 | 0.00 |
| 2026-04-25 | 45080597.38 | 161415.30 | 0.00 |
| 2026-04-26 | 45407391.04 | 326793.66 | 0.00 |
| 2026-04-30 | 45673146.50 | 265755.46 | 0.00 |
| 2026-05-07 | 45696146.45 | 22999.95 | 0.00 |
| 2026-05-11 | 45696402.30 | 255.85 | 0.00 |
| 2026-05-16 | 45696028.36 | -373.95 | -373.95 |
| 2026-06-14 | 46296687.11 | 600658.75 | 0.00 |
| 2026-06-30 | 46297439.23 | 752.12 | 0.00 |
| 2026-07-04 | 46297446.65 | 7.42 | 0.00 |
| 2026-07-06 | 46297447.20 | 0.55 | 0.00 |
| 2026-07-10 | 46297607.66 | 160.46 | 0.00 |
| 2026-07-16 | 46295510.09 | -2097.57 | -2097.57 |
| 2026-07-20 | 46297730.97 | 2220.87 | 0.00 |

</details>

### Top winners / losers contribution

Top10 winners $3,274,310.35 (22.37% of wins) · Top10 losers -$668,286.89 (56.52% of losses) · PF=21.0256

- WIN $600,658.75 · 375476s · Will the New York Knicks win the 2026 NBA Finals?
- WIN $495,581.93 · 35470s · Hawks vs. Knicks
- WIN $315,612.42 · 912s · Hornets vs. Thunder
- WIN $299,232.99 · 1276s · Will Liverpool FC win on 2026-01-01?
- WIN $289,219.21 · 10340s · Nuggets vs. Mavericks
- WIN $270,717.18 · 42838s · Spread: Patriots (-3.5)
- WIN $261,750.14 · 20960s · Spread: Eagles (-4.5)
- WIN $255,573.09 · 80508s · Spurs vs. Lakers
- WIN $252,076.15 · 840s · Spread: Broncos (-13.5)
- WIN $233,888.50 · 0s · Spread: Raptors (-2.5)

- LOSS -$29,143.07 · 57318s · UFC Fight Night: Muhammad vs. Machado Garry (Welterweight, Main Card)
- LOSS -$29,671.92 · 462692s · Will the Seattle Mariners win the 2025 World Series?
- LOSS -$32,532.08 · 0s · Champions League Final: 3+ goals?
- LOSS -$39,793.93 · 3964s · Thunder vs. Jazz
- LOSS -$65,540.87 · 2680s · Eagles vs. Chargers
- LOSS -$67,653.93 · 1804s · Falcons vs. Vikings
- LOSS -$84,368.74 · 1208s · Spread: Thunder (-11.5)
- LOSS -$87,922.18 · 820s · Chiefs vs. Broncos
- LOSS -$108,248.05 · 506s · Spread: Pistons (-9.5)
- LOSS -$123,412.12 · 48760s · Pistons vs. Celtics

## 5. Trade management deep dive

- Adverse early (>2¢): `{'n_early_adverse': 0, 'avg_pnl': None, 'median_t_first_sell': None, 'median_hold': None}`
- Favorable first-sell: `{'n_first_sell_up_2c': 23, 'avg_pnl': 64298.24, 'median_mfe_capture': 1.0, 'mean_mfe_capture': 0.7448}`
- Campaigns: `{'n': 8, 'pct': 1.11, 'avg_entries': 2.25, 'pnl': 130448.55, 'avg_pnl': 16306.07, 'win_rate': 0.625, 'single_n': 711, 'single_pnl': 13322206.78, 'single_avg_pnl': 18737.28}`
- Avg-down: `{'n_losers': 45, 'n_losers_with_red_buys': 9, 'pct_losers': 20.0, 'total_delta_if_skipped_on_losers': -2007.97, 'global_fifo_sim': 64977.34, 'global_fifo_never_red_buy': 46914.89, 'global_delta': -18062.45}`
- Resolution behavior: `{'flattened_before_flag_rate': 0.5396, 'hold_to_resolution_style_n': 615, 'redeems_usdc': 28094127.304343987, 'merges_usdc': 0.0}`
- Latency: `{'time_to_mfe_median': 18729, 'time_to_mfe_p25': 5998, 'time_to_mfe_p75': 66642, 'time_to_mfe_p90': 180256, 'mfe_ge_10c_n': 15, 'mfe_ge_10c_within_30s': 0, 'mfe_ge_10c_within_60s': 0, 'pct_big_within_60s': 0.0}`

### What works / fails
- WORKS: Winners capture median spread 0.0111 vs losers -0.0035
- WORKS: Both-sides inventory on 18.0% of winning markets (losers 37.8%)
- WORKS: Hold bucket <5m: avg PnL $14436.05 on 259 markets (WR 55%)
- WORKS: Hold bucket 5-30m: avg PnL $14954.18 on 119 markets (WR 48%)
- WORKS: Hold bucket 30m-2h: avg PnL $16384.02 on 116 markets (WR 49%)
- WORKS: Hold bucket 2-12h: avg PnL $35934.26 on 133 markets (WR 53%)
- WORKS: Hold bucket 12h+: avg PnL $13634.42 on 92 markets (WR 32%)
- WORKS: Entry band 0.00-0.20: avg $8662.69 across 128 markets
- WORKS: Entry band 0.20-0.40: avg $30266.65 across 150 markets
- WORKS: Entry band 0.40-0.60: avg $24556.76 across 266 markets
- WORKS: Entry band 0.60-0.80: avg $12008.19 across 113 markets
- WORKS: Entry band 0.80-1.00: avg $3436.94 across 42 markets
- WORKS: Buy-ladder behavior: fade-into-weakness markets=50, chase-up markets=46

## 6. Strategy overview (in depth)

# Strategy Dossier: DrPufferfish

- **Wallet:** `0xdb27bf2ac5d428a9c63dbc914611036855a6c56e`
- **History span:** 2025-05-29T20:52:43+00:00 → 2026-01-12T20:49:11+00:00 (228.0 days)
- **Trades:** 64,290 (buys 60,876 / sells 3,414)
- **Markets touched:** 719
- **Closed positions:** 881

## Headline performance

| Metric | Value |
|---|---|
| Realized cashflow (sells − buys + redeems + rebates) | $4,176,633.54 |
| Core cashflow (ex-rebates) | $4,175,613.54 |
| Closed-positions realized sum | $46,297,730.97 |
| Win rate (closed) | 90.22% (793W / 86L) |
| Profit factor | 21.0256 |
| Gross wins / losses | $48,609,653.80 / -$2,311,922.83 |
| Equity max drawdown | -$1,608,581.77 |
| Polymarket leaderboard (ALL) | $4,055,413.26 PnL · vol $248,548,251.18 · rank 30 |

## Source validation

- **MATCH** `polymarket_leaderboard_ALL` pnl: ours=4175613.5447 ref=4055413.259574452 diff=120200.2851
- **MATCH** `polydata` realized_pnl: ours=4175613.5447 ref=4055413.26 diff=120200.2847
- **DRIFT** `polydata` n_trades: ours=64290 ref=272027 diff=-207737
- **DRIFT** `polydata` win_rate: ours=0.9022 ref=0.481 diff=0.4212
- **DRIFT** `internal` cashflow_vs_closed: ours=4176633.543 ref=46297730.9682 diff=-42121097.4252

## What kind of trader is this?

**Classification:** `likely_market_maker` (score 55/100)

- Fast round-trips (<2h) in 30% of two-sided markets
- Avg sell > avg buy in 62% of markets (spread capture)
- High-frequency cadence (median gap 14s)

Supporting rates — both-sides markets: 0.1127, fast round-trips: 0.2976, spread-capture rate: 0.619.

## Exact edge thesis

DrPufferfish primarily monetizes **liquidity / short-horizon mean reversion on sports markets**, not long-shot directional political bets. The tape shows repeated buy-then-sell with average exit price above average entry — the classic scalper / spread fingerprint.

See `bot_playbook.md` for the full entry/management/exit autopsy and bot architecture.

## Where the money comes from

- **sports_match**: $43,141,219.15 across 701 closed legs
- **sports_totals**: $2,456,274.18 across 36 closed legs
- **other**: $647,948.05 across 133 closed legs
- **crypto**: $52,289.58 across 11 closed legs

## Timing

- Peak UTC hours: 19, 18, 0, 23, 21
- Peak weekdays (0=Mon): [5, 0, 6]
- Median inter-trade gap: 14s

## Sizing

- Median ticket $1.98, mean $415.51, p90 $108.42, max $248,000.00
- Share size median 27.0, mean 1043.8585

## Trade-by-trade pattern (representative winners)

These vignettes are reconstructed from fills: average entry, average exit, hold time, and closed realized PnL.

### Spurs vs. Lakers
- Entries ≈ **0.301** · Exits ≈ **0.710** · Spread ≈ **0.409**
- Fills: 334 buys / 104 sells · hold 22h 21m · both-sides=True · realized $255,573.09

### Bucks vs. Bulls
- Entries ≈ **0.441** · Exits ≈ **0.460** · Spread ≈ **0.019**
- Fills: 39 buys / 29 sells · hold 7h 26m · both-sides=False · realized $158,514.04

### Magic vs. Knicks
- Entries ≈ **0.480** · Exits ≈ **0.558** · Spread ≈ **0.078**
- Fills: 10 buys / 53 sells · hold 1h 50m · both-sides=True · realized $138,921.06

### Will Real Madrid win on 2025-11-23?
- Entries ≈ **0.303** · Exits ≈ **0.320** · Spread ≈ **0.017**
- Fills: 162 buys / 2 sells · hold 1h 27m · both-sides=False · realized $117,445.17

### Boxing: Canelo Álvarez vs. Terence Crawford 
- Entries ≈ **0.219** · Exits ≈ **0.445** · Spread ≈ **0.225**
- Fills: 87 buys / 4 sells · hold 9h 25m · both-sides=True · realized $114,649.29

### Pelicans vs. Nets
- Entries ≈ **0.592** · Exits ≈ **0.600** · Spread ≈ **0.009**
- Fills: 28 buys / 17 sells · hold 5h 38m · both-sides=False · realized $102,314.62

### Heat vs. Magic
- Entries ≈ **0.477** · Exits ≈ **0.520** · Spread ≈ **0.043**
- Fills: 360 buys / 7 sells · hold 1d 23h · both-sides=True · realized $90,919.01

### Cardinals vs. Cowboys
- Entries ≈ **0.333** · Exits ≈ **0.896** · Spread ≈ **0.563**
- Fills: 75 buys / 16 sells · hold 2h 44m · both-sides=True · realized $82,072.63

### Rockets vs. Lakers
- Entries ≈ **0.534** · Exits ≈ **0.560** · Spread ≈ **0.026**
- Fills: 195 buys / 79 sells · hold 23h 47m · both-sides=False · realized $75,885.11

### Cavaliers vs. Pacers
- Entries ≈ **0.610** · Exits ≈ **0.630** · Spread ≈ **0.020**
- Fills: 3 buys / 13 sells · hold 13m 0s · both-sides=False · realized $58,668.80

## Top closed winners / losers

**Winners**
- Will the New York Knicks win the 2026 NBA Finals?: $600,658.75 · bought $2,239.04 · sold $0.00 · hold 4d 8h
- Hawks vs. Knicks: $495,581.93 · bought $268,046.98 · sold $175.51 · hold 9h 51m
- Hornets vs. Thunder: $315,612.42 · bought $39,008.28 · sold $0.00 · hold 15m 12s
- Will Liverpool FC win on 2026-01-01?: $299,232.99 · bought $151,877.40 · sold $0.00 · hold 21m 16s
- Nuggets vs. Mavericks: $289,219.21 · bought $127,072.16 · sold $0.00 · hold 2h 52m
- Spread: Patriots (-3.5): $270,717.18 · bought $270,858.73 · sold $0.00 · hold 11h 53m
- Spread: Eagles (-4.5): $261,750.14 · bought $218,805.30 · sold $0.00 · hold 5h 49m
- Spurs vs. Lakers: $255,573.09 · bought $111,321.09 · sold $8,199.48 · hold 22h 21m
- Spread: Broncos (-13.5): $252,076.15 · bought $248,929.31 · sold $0.00 · hold 14m 0s
- Spread: Raptors (-2.5): $233,888.50 · bought $233,888.50 · sold $0.00 · hold 0s

**Losers**
- Pistons vs. Celtics: -$123,412.12 · bought $130,983.15 · sold $7,555.48
- Spread: Pistons (-9.5): -$108,248.05 · bought $108,715.92 · sold $0.00
- Chiefs vs. Broncos: -$87,922.18 · bought $93,485.12 · sold $0.00
- Spread: Thunder (-11.5): -$84,368.74 · bought $124,688.78 · sold $16,320.00
- Falcons vs. Vikings: -$67,653.93 · bought $76,706.61 · sold $0.00
- Eagles vs. Chargers: -$65,540.87 · bought $103,386.95 · sold $0.00
- Thunder vs. Jazz: -$39,793.93 · bought $50,169.65 · sold $0.00
- Champions League Final: 3+ goals?: -$32,532.08 · bought $32,532.08 · sold $0.00
- Will the Seattle Mariners win the 2025 World Series?: -$29,671.92 · bought $7,886.02 · sold $42,955.62
- UFC Fight Night: Muhammad vs. Machado Garry (Welterweight, Main Card): -$29,143.07 · bought $32,589.64 · sold $0.00

## Replication playbook (how to copy the edge)

1. **Universe:** Focus on liquid sports match + totals (O/U) markets with tight books.
2. **Role:** Quote or take both sides near mid; prioritize markets you can exit before resolution.
3. **Sizing:** Start near their median ticket (~$1.98) and scale only with inventory limits.
4. **Inventory:** Cap net Yes/No (or Over/Under) imbalance; flatten when mid moves through you.
5. **Hold time:** Target minutes–hours, not overnight directional risk, unless hedged via opposite outcome.
6. **Edge source:** Capture spread + mean reversion after flow, not oracle forecasting alpha.
7. **Ops:** Automate via CLOB maker orders; track maker rebates; kill-switch on drawdown.
8. **Do not blindly copy:** Their edge depends on latency, fee tier, and bankroll. Replicate *mechanics*, not wallet follows.

## Cashflow anatomy

- Buys: $25,315,785.94
- Sells: $1,397,272.18
- Redeems: $28,094,127.30
- Maker rebates: $0.00
- Taker rebates: $0.00

_Generated 2026-08-28T14:18:31.630397+00:00_


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
- Prioritize hold bucket 15m+ (their PnL engine)

### Avoid
- Averaging down while red on losers
- Their raw size/drawdown — scale down hard
- Fat left-tail single-market blowups — enforce per-market caps

Bot parameters: `{'preferred_entry_price_median': 0.51, 'preferred_entry_price_p25_p75': (0.41, 0.66), 'target_spread_median': 0.0111, 'target_spread_p75': 0.0461, 'max_hold_seconds_p75': 8328, 'median_hold_seconds': 1060, 'clip_size_usdc_median': 3.2, 'clip_size_usdc_p90': 195.0, 'both_sides_on_winners_rate': 0.1803, 'require_exit_above_entry': True, 'flatten_before_resolution': True, 'maker_bias': False}`

# Elite Replication Playbook — DrPufferfish

Wallet `0xdb27bf2ac5d428a9c63dbc914611036855a6c56e`. Reverse-engineered from the **full unique fill tape** (64,290 trades · 719 markets). This is an implementation spec for a high-end bot, not vibes.

## 0. True strategy identity (read this first)

Classification `likely_market_maker` — mix of spread capture and directional inventory.

Heuristic label from the scanner may still say `likely_market_maker` because of fast round-trips + sell>buy + maker rebates. **Operationally, build a live scalper with optional maker quoting**, not a Yes/No pair inventory bot.

## 1. Performance anchors

| Source / metric | Value |
|---|---|
| Cashflow realized (sells−buys+redeems+rebates) | $4,176,633.54 |
| Core cashflow (ex-rebates) | $4,175,613.54 |
| Closed-position legs sum | $46,297,730.97 |
| Leg win rate / profit factor | 90.22% / 21.0256 |
| Polymarket leaderboard ALL | $4,055,413.26 · vol $248,548,251.18 · rank 30 |
| polymarket_leaderboard_ALL pnl | ref=4055413.259574452 ours=4175613.5447 (MATCH) |
| polydata realized_pnl | ref=4055413.26 ours=4175613.5447 (MATCH) |
| polydata n_trades | ref=272027 ours=64290 (DRIFT) |
| polydata win_rate | ref=0.481 ours=0.9022 (DRIFT) |

Notes: Polymarket leaderboard ALL is the primary official PnL check (we match within tolerance). PolyData uses a different event aggregation / trade counting method — expect DRIFT on WR and trade count; use it as a secondary research signal, not the ground truth for fills.

## 2. Universe — where the money is

- **O/U / totals:** 13 markets · $26,160.57 · avg $2,012.35 · median hold 0s · median spread None
- **Match / other sports:** 579 markets · $10,350,373.08 · avg $17,876.29
- **Outcome PnL leaders:**
  - **No**: $2,117,185.42
  - **Nets**: $925,753.04
  - **Hawks**: $877,997.07
  - **Hornets**: $784,687.13
  - **Grizzlies**: $757,904.27
  - **Yes**: $689,925.66

### Bot universe rules

1. Only liquid live sports (soccer/football first — their tape is soccer-heavy).
2. Prefer O/U lines with tight books and active in-game trading.
3. Default bias toward **Over** unless your signal says otherwise (their Over PnL dominates).
4. Skip politics/crypto until you have separate evidence.
5. Require enough depth to enter ~median clip and exit within 1–2 minutes.

## 3. ENTRY — exact mechanics

### Style histogram
- `directional_buy_cheap_tail`: 155
- `directional_buy_sub_mid`: 152
- `directional_buy_near_mid`: 144
- `directional_buy_above_mid`: 114
- `directional_buy_expensive_favorite`: 51
- `two_sided_inventory_sub_mid`: 23
- `sell_first_cheap_tail`: 22
- `two_sided_inventory_above_mid`: 19
- `two_sided_inventory_cheap_tail`: 16
- `two_sided_inventory_near_mid`: 14
- `two_sided_inventory_expensive_favorite`: 9

### First-two-fill sequences
- `BUY->BUY`: 547
- `single_fill`: 148
- `SELL->SELL`: 14
- `BUY->SELL`: 10

### Entry price → realized edge

| Avg buy band | Markets | Total PnL | Avg PnL |
|---|---:|---:|---:|
| 0.00-0.20 | 128 | $1,108,823.86 | $8,662.69 |
| 0.20-0.40 | 150 | $4,539,997.13 | $30,266.65 |
| 0.40-0.60 | 266 | $6,532,097.53 | $24,556.76 |
| 0.60-0.80 | 113 | $1,356,925.63 | $12,008.19 |
| 0.80-1.00 | 42 | $144,351.35 | $3,436.94 |

**Best band:** 0.40–0.60 (near mid) — highest average PnL. Tails (≤0.20 or ≥0.80) make less per market.

### Entry checklist (bot)

1. Clip **$3.20** median (p90 $195.00).
2. Aim entry price ~**0.51** (IQR (0.41, 0.66)).
3. Trigger = microstructure, not long-term forecast:
   - mid dips / liquidity hole you can buy
   - imminent volatility (attack, corner, shot) where Over can jump
   - resting bid gets lifted? you’re being taken — manage immediately
4. Prefer **maker bids**; take only if the expected jump already started and ask is still inside your edge.
5. Same-second multi-fills are normal (one order, many counterparties) — treat as one decision, many fills.

## 4. MANAGEMENT — what they do after entry

### Styles
- `single_clip`: 211
- `multi_hour_position`: 183
- `intraday_swing`: 151
- `scalp_sub_15m`: 130
- `scale_in_scale_out`: 22
- `market_make_both_outcomes`: 22

### Winners vs losers

| Metric | Winners | Losers |
|---|---:|---:|
| N | 355 | 45 |
| PnL | $14,635,040.94 | -$1,182,385.61 |
| Median hold | 17m40s | 50m16s |
| Median spread | 0.0111 | -0.0035 |
| Scale-in rate | 0.7493 | 0.6222 |
| Scale-out rate | 0.0901 | 0.2889 |
| Avg fills/market | 79.03 | 99.4 |
| Both-sides rate | 0.1803 | 0.3778 |

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

- **Winners** sell above buy (median spread **0.0111**). **Losers** often exit worse (median spread **-0.0035**).
- Losers scale-in **more** (0.6222 vs 0.7493) — averaging down is how they bleed; the bot should **forbid** revenge scale-ins without a fresh signal.
- Hold edge peaks in **<5m** ({'n': 259, 'pnl': 3738937.7727, 'avg': 14436.0532, 'win_rate': 0.5483}) and a strong **30m–2h** bucket for the larger in-game campaigns.

## 5. EXIT — rules that print

- `hold_to_resolution_or_redeem`: 615
- `mixed_roundtrip`: 36
- `spread_harvest_sell_above_buy`: 35
- `sell_inventory_only`: 20
- `adverse_exit_sell_below_buy`: 13

| Hold bucket | N | Total PnL | Avg | Win rate |
|---|---:|---:|---:|---:|
| <5m | 259 | $3,738,937.77 | $14,436.05 | 54.8% |
| 5-30m | 119 | $1,779,547.91 | $14,954.18 | 47.9% |
| 30m-2h | 116 | $1,900,546.04 | $16,384.02 | 49.1% |
| 2-12h | 133 | $4,779,257.21 | $35,934.26 | 52.6% |
| 12h+ | 92 | $1,254,366.40 | $13,634.42 | 31.5% |

### Exit engine params

1. **TP / ask distance:** target ≈ **0.0111** above avg entry (p75 stretch 0.0461). On live O/U this is often a burst move, not slow grind.
2. **Time stop:** median hold 17m40s; p75 2h18m for the scalps — escalate urgency after that.
3. **Scale-out:** peel into strength (their winners stack sells). Don’t wait for one perfect print.
4. **Stop:** if mid < entry − ~3–5¢ on unhedged inventory with no signal → take the loss (copy losers’ speed, not their hope).
5. **Flatten before resolution** — redeem is residual.
6. Taker exits are fine when the move already happened and maker asks won’t fill.

## 6. What works / what fails

### Works
- Winners capture median spread 0.0111 vs losers -0.0035
- Both-sides inventory on 18.0% of winning markets (losers 37.8%)
- Hold bucket <5m: avg PnL $14436.05 on 259 markets (WR 55%)
- Hold bucket 5-30m: avg PnL $14954.18 on 119 markets (WR 48%)
- Hold bucket 30m-2h: avg PnL $16384.02 on 116 markets (WR 49%)
- Hold bucket 2-12h: avg PnL $35934.26 on 133 markets (WR 53%)
- Hold bucket 12h+: avg PnL $13634.42 on 92 markets (WR 32%)
- Entry band 0.00-0.20: avg $8662.69 across 128 markets
- Entry band 0.20-0.40: avg $30266.65 across 150 markets
- Entry band 0.40-0.60: avg $24556.76 across 266 markets
- Entry band 0.60-0.80: avg $12008.19 across 113 markets
- Entry band 0.80-1.00: avg $3436.94 across 42 markets
- Buy-ladder behavior: fade-into-weakness markets=50, chase-up markets=46

### Fails
- (no strong negative bucket)
- Chase vs fade ladders: `{'chase_up': 46, 'fade_down': 50}`

## 7. Fill-by-fill autopsies (copy these patterns)

### Example 1: Rockets vs. Lakers
PnL $75,885.11 · hold 23h47m · 195B/79S · avg entry 0.5342 → exit 0.56 (spread 0.0258) · `scale_in_scale_out`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2025-12-25T01:01:33+00:00 | BUY | Rockets | 4095.99 | 0.5499 | 2252.39 |
| 2025-12-25T02:46:41+00:00 | BUY | Rockets | 287.46 | 0.5400 | 155.23 |
| 2025-12-25T02:50:55+00:00 | BUY | Rockets | 89.13 | 0.5400 | 48.13 |
| 2025-12-25T02:51:03+00:00 | BUY | Rockets | 355.24 | 0.5400 | 191.83 |
| 2025-12-25T02:53:53+00:00 | BUY | Rockets | 2.00 | 0.5400 | 1.08 |
| 2025-12-25T03:12:51+00:00 | BUY | Rockets | 1500.00 | 0.5400 | 810.00 |
| 2025-12-25T03:13:21+00:00 | BUY | Rockets | 100.00 | 0.5400 | 54.00 |
| 2025-12-25T03:13:21+00:00 | BUY | Rockets | 400.00 | 0.5400 | 216.00 |
| 2025-12-25T03:18:17+00:00 | BUY | Rockets | 1456.09 | 0.5400 | 786.29 |
| 2025-12-25T03:19:27+00:00 | BUY | Rockets | 3.28 | 0.5400 | 1.77 |
| 2025-12-25T03:19:33+00:00 | BUY | Rockets | 1.89 | 0.5400 | 1.02 |
| 2025-12-25T03:21:07+00:00 | BUY | Rockets | 71.74 | 0.5400 | 38.74 |
| 2025-12-25T03:28:53+00:00 | BUY | Rockets | 2.17 | 0.5400 | 1.17 |
| 2025-12-25T03:33:51+00:00 | BUY | Rockets | 217.39 | 0.5400 | 117.39 |
| 2025-12-25T03:34:23+00:00 | BUY | Rockets | 5.74 | 0.5400 | 3.10 |
| 2025-12-26T00:32:47+00:00 | BUY | Rockets | 1265.89 | 0.5400 | 683.58 |
| 2025-12-26T00:32:47+00:00 | BUY | Rockets | 8.15 | 0.5400 | 4.40 |
| 2025-12-26T00:33:03+00:00 | BUY | Rockets | 217.39 | 0.5400 | 117.39 |
| 2025-12-26T00:33:09+00:00 | BUY | Rockets | 217.39 | 0.5400 | 117.39 |
| 2025-12-26T00:33:37+00:00 | BUY | Rockets | 495.37 | 0.5400 | 267.50 |
| 2025-12-26T00:33:49+00:00 | BUY | Rockets | 30.00 | 0.5400 | 16.20 |
| 2025-12-26T00:40:23+00:00 | BUY | Rockets | 2406.48 | 0.5300 | 1275.43 |
| 2025-12-26T00:41:51+00:00 | BUY | Rockets | 70.00 | 0.5300 | 37.10 |
| 2025-12-26T00:42:01+00:00 | BUY | Rockets | 69.32 | 0.5300 | 36.74 |
| 2025-12-26T00:42:01+00:00 | BUY | Rockets | 11.04 | 0.5300 | 5.85 |
| 2025-12-26T00:42:01+00:00 | BUY | Rockets | 100.00 | 0.5300 | 53.00 |
| 2025-12-26T00:42:29+00:00 | BUY | Rockets | 212.77 | 0.5300 | 112.77 |
| 2025-12-26T00:42:39+00:00 | BUY | Rockets | 182.49 | 0.5300 | 96.72 |
| 2025-12-26T00:42:49+00:00 | BUY | Rockets | 10.00 | 0.5300 | 5.30 |
| 2025-12-26T00:49:15+00:00 | BUY | Rockets | 120270.88 | 0.5300 | 63743.57 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 2: Chris Eubank Jr. vs Conor Benn Nov 15, 2025
PnL $50,078.27 · hold 37m04s · 12B/7S · avg entry 0.3994 → exit 0.42 (spread 0.0206) · `scale_in_scale_out`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2025-11-15T21:20:55+00:00 | BUY | Benn | 158.40 | 0.3800 | 60.19 |
| 2025-11-15T21:35:15+00:00 | BUY | Benn | 5.00 | 0.4000 | 2.00 |
| 2025-11-15T21:36:13+00:00 | BUY | Benn | 333.33 | 0.4000 | 133.33 |
| 2025-11-15T21:37:19+00:00 | BUY | Benn | 74987.00 | 0.4000 | 29994.80 |
| 2025-11-15T21:38:05+00:00 | BUY | Benn | 161.29 | 0.3800 | 61.29 |
| 2025-11-15T21:38:15+00:00 | SELL | Benn | 81.44 | 0.4200 | 34.20 |
| 2025-11-15T21:38:59+00:00 | BUY | Benn | 161.29 | 0.3800 | 61.29 |
| 2025-11-15T21:39:55+00:00 | SELL | Benn | 9.90 | 0.4200 | 4.16 |
| 2025-11-15T21:40:33+00:00 | SELL | Benn | 220.00 | 0.4200 | 92.40 |
| 2025-11-15T21:42:29+00:00 | SELL | Benn | 47.62 | 0.4200 | 20.00 |
| 2025-11-15T21:43:35+00:00 | SELL | Benn | 713.90 | 0.4200 | 299.84 |
| 2025-11-15T21:43:43+00:00 | BUY | Benn | 6.45 | 0.3800 | 2.45 |
| 2025-11-15T21:45:01+00:00 | SELL | Benn | 26.29 | 0.4200 | 11.04 |
| 2025-11-15T21:47:19+00:00 | SELL | Benn | 98.00 | 0.4200 | 41.16 |
| 2025-11-15T21:50:15+00:00 | BUY | Benn | 1687.85 | 0.3800 | 641.38 |
| 2025-11-15T21:50:45+00:00 | BUY | Benn | 161.29 | 0.3800 | 61.29 |
| 2025-11-15T21:53:05+00:00 | BUY | Benn | 105.68 | 0.3800 | 40.16 |
| 2025-11-15T21:53:57+00:00 | BUY | Benn | 6670.00 | 0.4000 | 2668.00 |
| 2025-11-15T21:57:59+00:00 | BUY | Benn | 100.00 | 0.3900 | 39.00 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 3: 76ers vs. Grizzlies
PnL $25,958.35 · hold 5h11m · 98B/11S · avg entry 0.491 → exit 0.54 (spread 0.049) · `scale_in_scale_out`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2025-12-30T19:48:51+00:00 | BUY | 76ers | 191.73 | 0.4900 | 93.95 |
| 2025-12-30T19:52:49+00:00 | BUY | 76ers | 378.05 | 0.4900 | 185.24 |
| 2025-12-30T19:53:01+00:00 | BUY | 76ers | 425.49 | 0.4900 | 208.49 |
| 2025-12-30T19:53:03+00:00 | BUY | 76ers | 2188.24 | 0.4900 | 1072.24 |
| 2025-12-30T19:53:05+00:00 | BUY | 76ers | 431.37 | 0.4900 | 211.37 |
| 2025-12-30T19:53:11+00:00 | BUY | 76ers | 9025.66 | 0.4900 | 4422.57 |
| 2025-12-30T23:57:45+00:00 | BUY | 76ers | 1710.00 | 0.4800 | 820.80 |
| 2025-12-30T23:57:45+00:00 | BUY | 76ers | 442.03 | 0.4800 | 212.17 |
| 2025-12-30T23:57:51+00:00 | BUY | 76ers | 90.00 | 0.4800 | 43.20 |
| 2025-12-30T23:57:55+00:00 | BUY | 76ers | 3.00 | 0.4800 | 1.44 |
| 2025-12-30T23:57:57+00:00 | BUY | 76ers | 2.00 | 0.4800 | 0.96 |
| 2025-12-30T23:58:19+00:00 | BUY | 76ers | 150.00 | 0.4800 | 72.00 |
| 2025-12-30T23:58:43+00:00 | BUY | 76ers | 9.62 | 0.4800 | 4.62 |
| 2025-12-30T23:59:07+00:00 | BUY | 76ers | 9.00 | 0.4800 | 4.32 |
| 2025-12-30T23:59:09+00:00 | BUY | 76ers | 1106.00 | 0.4800 | 530.88 |
| 2025-12-31T00:32:25+00:00 | BUY | 76ers | 10.00 | 0.5000 | 5.00 |
| 2025-12-31T00:32:29+00:00 | BUY | 76ers | 73.00 | 0.5000 | 36.50 |
| 2025-12-31T00:32:33+00:00 | BUY | 76ers | 75.00 | 0.5000 | 37.50 |
| 2025-12-31T00:32:59+00:00 | BUY | 76ers | 10.00 | 0.5000 | 5.00 |
| 2025-12-31T00:35:33+00:00 | SELL | 76ers | 51929.26 | 0.5400 | 28041.80 |
| 2025-12-31T00:46:57+00:00 | SELL | 76ers | 5.56 | 0.5400 | 3.00 |
| 2025-12-31T00:57:43+00:00 | SELL | 76ers | 925.93 | 0.5400 | 500.00 |
| 2025-12-31T00:58:07+00:00 | SELL | 76ers | 7.84 | 0.5400 | 4.23 |
| 2025-12-31T00:58:15+00:00 | SELL | 76ers | 15048.52 | 0.5400 | 8126.20 |
| 2025-12-31T00:58:21+00:00 | SELL | 76ers | 257.41 | 0.5400 | 139.00 |
| 2025-12-31T00:58:27+00:00 | SELL | 76ers | 100.00 | 0.5400 | 54.00 |
| 2025-12-31T00:58:35+00:00 | SELL | 76ers | 8.56 | 0.5400 | 4.62 |
| 2025-12-31T00:59:03+00:00 | SELL | 76ers | 200.00 | 0.5400 | 108.00 |
| 2025-12-31T00:59:17+00:00 | SELL | 76ers | 185.19 | 0.5400 | 100.00 |
| 2025-12-31T00:59:57+00:00 | SELL | 76ers | 2190.00 | 0.5400 | 1182.60 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

## 8. Failure modes (do not bot these)

1. **Pistons vs. Celtics** -$123,412.12 · hold 13h32m · entry 0.5208 → exit 0.47 · `market_make_both_outcomes` / `adverse_exit_sell_below_buy`
2. **Spread: Pistons (-9.5)** -$108,248.05 · hold 8m26s · entry 0.4763 → exit None · `scalp_sub_15m` / `hold_to_resolution_or_redeem`
3. **Chiefs vs. Broncos** -$87,922.18 · hold 13m40s · entry 0.6379 → exit None · `scalp_sub_15m` / `hold_to_resolution_or_redeem`
4. **Spread: Thunder (-11.5)** -$84,368.74 · hold 20m08s · entry 0.4866 → exit 0.48 · `intraday_swing` / `mixed_roundtrip`
5. **Falcons vs. Vikings** -$67,653.93 · hold 30m04s · entry 0.5848 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
6. **Eagles vs. Chargers** -$65,540.87 · hold 44m40s · entry 0.507 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
7. **Thunder vs. Jazz** -$39,793.93 · hold 1h06m · entry 0.1848 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
8. **Champions League Final: 3+ goals?** -$32,532.08 · hold 0s · entry 0.43 → exit None · `single_clip` / `hold_to_resolution_or_redeem`
9. **Will the Seattle Mariners win the 2025 World Series?** -$29,671.92 · hold 5d · entry 0.6043 → exit 0.278 · `market_make_both_outcomes` / `adverse_exit_sell_below_buy`
10. **UFC Fight Night: Muhammad vs. Machado Garry (Welterweight, Main Card)** -$29,143.07 · hold 15h55m · entry 0.2754 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`

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
   - default post-only bids/asks; clip $3.20
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
template: DrPufferfish
mode: one_sided_live_scalper  # not classic two-sided MM
preferred_outcome_bias: Over
clip_usdc_median: 3.2
clip_usdc_p90: 195.0
entry_price_median: 0.51
entry_price_iqr: (0.41, 0.66)
target_spread: 0.0111
target_spread_p75: 0.0461
median_hold_seconds: 1060
max_hold_seconds_p75: 8328
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

_Generated 2026-08-28T14:18:31.630629+00:00_


## 8. Structured autopsy (A–G)

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


## 9. Hour / DOW volume (UTC)

| Hour | USDC volume |
|---:|---:|
| 0 | 4416664.44 |
| 1 | 2176670.59 |
| 2 | 1139411.77 |
| 3 | 289403.83 |
| 4 | 167999.92 |
| 5 | 167735.55 |
| 6 | 95858.4 |
| 7 | 71573.55 |
| 8 | 12422.07 |
| 9 | 38324.16 |
| 10 | 50841.93 |
| 11 | 75834.63 |
| 12 | 196597.25 |
| 13 | 449675.28 |
| 14 | 605034.42 |
| 15 | 562400.1 |
| 16 | 1272988.83 |
| 17 | 2275118.15 |
| 18 | 2001117.48 |
| 19 | 2776251.24 |
| 20 | 841823.62 |
| 21 | 2058610.28 |
| 22 | 1206080.19 |
| 23 | 3764620.42 |

| DOW (0=Mon) | USDC volume |
|---:|---:|
| 0 | 3382787.38 |
| 1 | 3980135.54 |
| 2 | 3430533.96 |
| 3 | 2828845.53 |
| 4 | 3146340.24 |
| 5 | 4859703.48 |
| 6 | 5084711.99 |

## 10. Bot schema pointer

Parse `MASTER.json` keys: `reconciliation`, `identity`, `performance`, `extras`, `copyability`, `equity_curve_daily`, `deep_dive_highlights`.
