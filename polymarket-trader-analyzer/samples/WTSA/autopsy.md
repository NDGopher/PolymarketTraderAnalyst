# Deep Trader Autopsy — WTSA

- Wallet: `0x04d5524a0a5af2eca6e39e03defc261d42fe66d8`
- Identity: **`directional_hold_to_resolution`**
- Primary focus: **other**
- Span: 2026-07-16T05:26:52+00:00 → 2026-07-29T16:12:36+00:00 (13.45 days)
- Generated: 2026-08-25T21:55:37.988626+00:00

## A. Data integrity / reconciliation

| Source | PnL | Trades / notes |
|---|---:|---|
| Our cashflow realized | $169,030.34 | trades=17,934 |
| Our core cashflow | $160,372.00 | buys=17,934 sells=0 |
| Our closed-legs sum | $3,581,052.07 | closed=77 WR=98.7% |
| Polymarket leaderboard ALL | $445,687.54 | vol=$14,298,289.84 rank=468 |
| PolyData | $519,173.09 | trades=29173 WR=0.5402 |

- **DRIFT** `polymarket_leaderboard_ALL` pnl: ours=169030.3377 ref=445687.5427547153 diff=-276657.2051
- **DRIFT** `polydata` realized_pnl: ours=169030.3377 ref=519173.09 diff=-350142.7523
- **DRIFT** `polydata` n_trades: ours=17934 ref=29173 diff=-11239
- **DRIFT** `polydata` win_rate: ours=0.987 ref=0.5402 diff=0.4468
- **DRIFT** `internal` cashflow_vs_closed: ours=169030.3377 ref=3581052.072 diff=-3412021.7343

## B. Core identity

- Scanner MM label: `directional_or_unclear` (score 10)
- High-frequency cadence (median gap 2s)
- Both-sides inventory: 1 markets (1.64%)
- Clip USDC median/p90/max: $4.81 / $93.19 / $45,780.00
- Sport categories: `{'other': 799148.23, 'sports_totals': 399961.76, 'sports_match': 111448.19}`
- Slug tokens: []

### Maker vs Taker

| Leg | Maker % | Taker % | Maker fills | Taker fills |
|---|---:|---:|---:|---:|
| Entry | 54.66% | 45.34% | 17,802 | 132 |
| Exit | None% | None% | 0 | 0 |


### Price bands

| Band | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| 20-40¢ | 13 | 100.0% | $182,533.90 | $14,041.07 |
| 40-60¢ | 38 | 100.0% | $1,039,138.45 | $27,345.75 |
| 60-80¢ | 10 | 100.0% | $88,885.82 | $8,888.58 |

## C. Equity & risk

- Final cashflow equity: $169,030.34
- Max drawdown: -$596,843.08 (-441.6% of peak)
- Longest drawdown: 1 days
- Daily Sharpe (ann.): 0.715
- Profit factor: 122.4517
- Top 10 winners: $833,981.93 (63.64% of win PnL)
- Top 10 losers: $0.00 (None% of loss PnL)
- Max inventory shares: 299998.81

### Top winners
- $157,319.67 · 8m27s · Will Inter Miami CF win on 2026-07-25?
- $100,914.54 · 39m07s · CD Guadalajara vs. FC Juárez: O/U 2.5
- $94,438.28 · 4h31m · Will Colorado Rapids SC win on 2026-07-22?
- $85,702.47 · 45m42s · Club Tijuana vs. Club León FC: O/U 2.5
- $85,019.66 · 3h44m · Will CR Flamengo win on 2026-07-29?
- $80,881.53 · 18h02m · Will CF Montréal win on 2026-07-16?
- $71,898.79 · 5h36m · Will Philadelphia Union win on 2026-07-25?
- $55,072.39 · 51m06s · Will Fluminense FC win on 2026-07-17?
- $53,117.48 · 3h58m · Will Athletic Club win on 2026-07-28?
- $49,617.10 · 1m39s · Will CA San Lorenzo de Almagro win on 2026-07-28?

### Top losers
- $0.00 · 51m15s · Will EC Bahia win on 2026-07-26?
- $0.00 · 47m36s · Will Cruzeiro EC win on 2026-07-26?
- $0.00 · 6h13m · Will CA Rosario Central win on 2026-07-28?
- $0.00 · 4h21m · Will EC Juventude win on 2026-07-28?
- $0.00 · 4h00m · Will AA Ponte Preta win on 2026-07-28?
- $0.00 · 3h45m · CA Rosario Central vs. Racing Club: O/U 2.5
- $0.00 · 19m21s · Will CA Banfield win on 2026-07-28?
- $0.00 · 14m25s · AA Ponte Preta vs. Athletic Club: O/U 2.5
- $0.00 · 36s · CA Rosario Central vs. Racing Club: O/U 1.5
- $0.00 · 3h30m · Will SC Internacional win on 2026-07-29?

## D. Trade management

### Hold-time buckets

| Bucket | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| <30s | 2 | 100.0% | $17,684.36 | $8,842.18 |
| 30s-2m | 3 | 100.0% | $49,617.10 | $16,539.03 |
| 2-5m | 4 | 100.0% | $14,490.79 | $3,622.70 |
| 5-15m | 12 | 100.0% | $344,851.76 | $28,737.65 |
| 15m+ | 40 | 100.0% | $883,914.17 | $22,097.85 |

- After early adverse (>2¢ vs entry within 2m): n=0, avg PnL n/a, median first-sell n/a, median hold n/a
- After favorable first sell (+2¢): n=0, avg PnL n/a, median MFE capture None
- Campaigns (re-entry after flat): 0 (0.0%), avg entries None, PnL $0.00, avg n/a, WR None%
- Single-entry: n=61, PnL $1,310,558.18, avg $21,484.56
- Flatten-before-resolution flag rate: 0.4262; hold-to-resolution style n=61; redeems $2,570,194.92; merges $0.00
- Avg-down while MTM-red on losers: 0/0 (0.0%); Δ if skipped on those $0.00; global never-red-buy Δ $0.00

### Family mix

| Family | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| Yes/No moneyline | 38 | 100.0% | $890,430.19 | $23,432.37 |
| Over/Under | 21 | 100.0% | $395,661.76 | $18,841.04 |
| Other | 2 | 100.0% | $24,466.22 | $12,233.11 |

## E. Edge diagnosis

- Time to MFE (winners): median n/a, p25 n/a, p75 n/a, p90 n/a
- Big MFE ≥10¢: n=0; within 30s=0; within 60s=0 (0.0% of big moves)

**Edge thesis:** Directional positioning with significant redeem/merge cashflows — holds risk into resolution more than pure scalpers.

## F. vs polika72

| Metric | This trader | polika72 |
|---|---:|---:|
| identity | directional_hold_to_resolution | one_sided_informed_scalper |
| trades | 17934 | 19978 |
| cashflow_pnl | 169030.3377 | 58204.9839 |
| win_rate | 0.987 | 0.8008 |
| entry_taker_pct | 45.34 | 61.62 |
| both_sides_rate | 0.0164 | 0.0068 |
| median_clip | 4.8064 | 11.29 |
| campaign_pct | 0.0 | 5.85 |
| max_dd | -596843.0806 | -601.1817 |
| time_to_mfe_med | None | 64 |

### Steal / avoid

- **Steal:** maker-led entries (better for quoting stack on Kalshi).
- **Avoid:** their drawdown profile — size down vs polika72 risk.

## G. Kalshi two-sided informed MM relevance

Moderate relevance — extract risk limits and hold-time discipline; do not assume their edge transfers without Kalshi-specific microstructure testing.
