# Deep Trader Autopsy — Winnertraders

- Wallet: `0x13464aabec792c36b062316f474713e681330448`
- Identity: **`hybrid_liquidity_scalper`**
- Primary focus: **sports_totals**
- Span: 2026-01-16T07:37:14+00:00 → 2026-08-23T03:42:52+00:00 (218.84 days)
- Generated: 2026-08-25T21:55:36.205871+00:00

## A. Data integrity / reconciliation

| Source | PnL | Trades / notes |
|---|---:|---|
| Our cashflow realized | $16,661.90 | trades=20,475 |
| Our core cashflow | $16,180.10 | buys=11,909 sells=8,566 |
| Our closed-legs sum | -$844.29 | closed=3,001 WR=65.1% |
| Polymarket leaderboard ALL | $17,578.63 | vol=$2,032,708.12 rank=9024 |
| PolyData | $17,655.63 | trades=16162 WR=0.5926 |

- **MATCH** `polymarket_leaderboard_ALL` pnl: ours=16661.9043 ref=17578.63221507959 diff=-916.7279
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
